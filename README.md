# devops-50-assignments
# Assignment 6 — CI/CD Pipeline with Multi-Stage Docker

## What this pipeline does
[2-3 sentences: what triggers it, the two jobs, what comes out the end]
git push would trigger the pipeline and it has two jobs such as run tests and scan&push the images. and at the end the images built will get settled in GHCR.

## Design decisions
- Multi-stage build: to make the images size come out smaller.
- Non-root user: By default containers run as root, and since containers share the host kernel, a container-escape vulnerability — like the runc CVE from 2019 — can turn root-in-the-container into root-on-the-host. Running as a non-root user breaks that chain: even if the app is compromised, the attacker lands as an unprivileged user, and most escape techniques require root to even attempt. It's defence in depth — one line in the Dockerfile that assumes the app layer will fail and limits the blast radius when it does.
- Image tagged with commit SHA, never :latest: [why:?]
"We tag with the commit SHA so every image is immutable and traceable — given what's in prod, I can name the exact commit. :latest is a moving pointer: it breaks rollback, breaks auditability, and can even leave mixed versions running behind one tag."
- Trivy scan BEFORE push: is necessary to find vulnerabilities in images.
- ignore-unfixed: some vulnerabilities cannot be changed by us. so, we can ignore those by adding ignore-unfixed: true
## The debugging story (6 runs to green)
#1 — PAT lacked workflow scope → learned token scopes and why workflow files are security-fenced
#2 — Dockerfile: no such file → learned runners only have what's in Git
#3 — casing bug → learned Linux is case-sensitive, macOS lied to you
#4 — Trivy: 56 vulns → learned base images carry OS CVEs that aren't your code
#5 — 12 fixable remained → learned base images lag Debian's security repos
#6 — patched at build time → green

## What I'd tell an interviewer in 60 seconds
[one paragraph, spoken-voice, summarizing all of the above]
