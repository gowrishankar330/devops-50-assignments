import os
import hashlib
import boto3
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def local_md5(filepath: str) -> str:
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5.update(chunk)
    return md5.hexdigest()


def scan_local(local_dir: str) -> dict:
    result = {}
    for root, dirs, files in os.walk(local_dir):
        for filename in files:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, local_dir)
            result[relative_path] = local_md5(full_path)
    return result


def scan_s3(bucket: str, prefix: str = "") -> dict:
    s3 = boto3.client("s3")
    result = {}
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            result[obj["Key"]] = obj["ETag"]
    return result


def compute_diff(local: dict, remote: dict) -> tuple:
    to_upload = []
    to_delete = []
    for path, md5 in local.items():
        remote_etag = remote.get(path, "").strip('"')
        if md5 != remote_etag:
            to_upload.append(path)
    for key in remote:
        if key not in local:
            to_delete.append(key)
    return to_upload, to_delete


def upload_file(local_dir: str, path: str, bucket: str) -> str:
    s3 = boto3.client("s3")
    local_path = os.path.join(local_dir, path)
    s3.upload_file(local_path, bucket, path)
    return path


def delete_object(bucket: str, key: str) -> str:
    s3 = boto3.client("s3")
    s3.delete_object(Bucket=bucket, Key=key)
    return key


def sync(local_dir: str, bucket: str, delete: bool = False, threads: int = 4):
    print(f"\n📁 Scanning local directory: {local_dir}")
    local = scan_local(local_dir)
    print(f"   Found {len(local)} local files")

    print(f"\n☁️  Scanning S3 bucket: {bucket}")
    remote = scan_s3(bucket)
    print(f"   Found {len(remote)} S3 objects")

    to_upload, to_delete = compute_diff(local, remote)

    print(f"\n📊 Diff result:")
    print(f"   To upload : {len(to_upload)} files")
    print(f"   To delete : {len(to_delete)} objects")
    print(f"   Unchanged : {len(local) - len(to_upload)} files (skipped)")

    if to_upload:
        print(f"\n⬆️  Uploading {len(to_upload)} files with {threads} threads...")
        uploaded = 0
        failed = 0
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(upload_file, local_dir, path, bucket): path
                for path in to_upload
            }
            with tqdm(total=len(to_upload), unit="file") as bar:
                for future in as_completed(futures):
                    path = futures[future]
                    try:
                        future.result()
                        uploaded += 1
                        bar.set_postfix(file=path[-30:])
                    except Exception as e:
                        print(f"\n   ❌ Failed: {path} — {e}")
                        failed += 1
                    bar.update(1)
        print(f"   ✅ Uploaded: {uploaded}  ❌ Failed: {failed}")

    if to_delete and delete:
        print(f"\n🗑️  Deleting {len(to_delete)} removed objects...")
        for key in to_delete:
            try:
                delete_object(bucket, key)
                print(f"   deleted: {key}")
            except Exception as e:
                print(f"   ❌ Failed to delete {key}: {e}")
    elif to_delete and not delete:
        print(f"\n⚠️  {len(to_delete)} objects in S3 not in local (run with --delete to remove)")

    print(f"\n✅ Sync complete.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync a local directory to S3")
    parser.add_argument("local_dir", help="Local directory to sync")
    parser.add_argument("bucket", help="S3 bucket name")
    parser.add_argument("--delete", action="store_true",
                        help="Delete S3 objects not present locally")
    parser.add_argument("--threads", type=int, default=4,
                        help="Number of parallel upload threads (default: 4)")
    args = parser.parse_args()

    sync(args.local_dir, args.bucket, args.delete, args.threads)
