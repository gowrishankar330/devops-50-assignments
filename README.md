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

Phase 2 — Kubernetes Core (Assignments 7–10)

Assignment 7 — Self-Healing

What you built: crash endpoints, liveness/readiness probes, observed healing live.

Key takeaways:

Container dies → kubelet restarts in-place (same pod, RESTARTS++) vs pod deleted → ReplicaSet creates a new pod (new name). These are two different healing layers with different actors.
PID 1 inside a container is immune to signals from its own children — SIGKILL from a worker can't kill the gunicorn master. Only handled signals (SIGTERM, SIGQUIT) work from inside; the kubelet kills from outside.
Liveness = "restart me if I'm broken." Readiness = "stop sending traffic until I'm ready." Same endpoint, different consequences. Liveness must never check dependencies — a DB outage that kills liveness causes a pod restart storm while the DB is recovering, turning a 30s blip into a 10-minute outage.
CrashLoopBackOff = container dies instantly on boot repeatedly. Almost always bad config, missing env var, or broken startup code. Diagnose with kubectl logs immediately — the error is always there.
The probe path and app route must stay in sync. Change one without the other = pods fail readiness silently.

Assignment 8 — Horizontal Scaling

What you built: metrics-server, HPA, load generator, watched the cluster breed and shrink pods autonomously.

Key takeaways:

HPA reconciles replica count against a condition (CPU%). It's the same reconciliation loop as everything else in Kubernetes — observe, compare, fix.
Requests are the denominator for HPA percentages. No requests = HPA is blind. "70% CPU" means 70% of the requested CPU, not of the node.
HPA-managed deployments must not declare replicas: — a future kubectl apply would stomp whatever the HPA scaled to, potentially slashing pods mid-spike.
Scale-up is fast (users are suffering); scale-down is slow (~5 minutes stabilization window). Asymmetry is deliberate — a spike might return; churning pods is worse than briefly overprovisioning.
--kubelet-insecure-tls skips TLS verification for metrics-server → kubelet connections. Lab-only: in production this enables man-in-the-middle attacks on the metrics stream.
Docker layer caching: COPY requirements.txt + pip install before COPY main.py means code changes don't invalidate the package cache. Order from least-changing to most-changing.

Assignment 9 — RBAC

What you built: namespaces, ServiceAccounts, Roles, RoleBindings, verified with kubectl auth can-i and live Forbidden errors.

Key takeaways:

RBAC = Role + RoleBinding only. Namespaces are scopes; ServiceAccounts are identities. Neither is RBAC.
Two gates: Authentication ("who are you?") → Authorization ("may you do this?"). RBAC is only the second gate.
Everything is deny-by-default. Roles only add permissions, never deny. Cross-namespace isolation is the absence of a binding, not a deny rule.
Binding namespace decides where the grant applies, not the subject's namespace. The classic mistake: binding in the wrong namespace grants access to the wrong territory.
Groups not individuals — 50 people get one RoleBinding via a Group. Offboarding: remove from the identity provider, all cluster access dies instantly. Per-person bindings are an audit and offboarding disaster.
RBAC ≠ NetworkPolicy. RBAC controls the Kubernetes API (kubectl, pod management). NetworkPolicy controls TCP traffic between pods. A pod with zero RBAC can still connect to a database on port 5432 — RBAC won't stop it. You need NetworkPolicy for that.
ClusterRole + RoleBinding = define once, grant per-namespace. The production pattern for shared permission templates.

Assignment 10 — Ingress + TLS

What you built: kind cluster with port mappings, NGINX Ingress via Helm, /etc/hosts DNS override, path-based routing (/ → devopsapp, /data → dataapp), cert-manager, self-signed TLS, HTTP→HTTPS auto-redirect.

Key takeaways:

Ingress = routing rulebook. Ingress Controller (NGINX) = the reverse proxy that reads it. Rules are Kubernetes objects — declarative, in Git.
Host-based routing: nginx reads the Host: header, not the IP. Same port 80, devopsapp.local → app, localhost → 404. One reception desk, fifty apps.
Path-based routing: longer prefix wins. /data must come before / or the catch-all swallows everything.
Nginx passes the full path to the backend unchanged. If your Ingress routes /data to an app that serves /health, the app receives /data/health — not /health. Your app routes must match what nginx forwards, or you rewrite with annotations.
Cross-namespace Ingress: an Ingress object can only reference Services in its own namespace. Two namespaces = two Ingress objects, same host, controller merges them.
TLS trust chain: Certificate Authority signs a cert vouching for a domain. Browser trusts CAs in its bundle. Self-signed = nobody vouches = browser warns. Let's Encrypt = trusted CA = green padlock. Same encryption, different authentication.
cert-manager workflow: annotation on Ingress → cert-manager sees it → creates Certificate object → issues cert → stores as Secret → nginx reads Secret → serves HTTPS. ClusterIssuer is created once per cluster; annotation is added per app. Swap selfsigned for letsencrypt-prod and the whole cluster upgrades.
Service labels vs pod selector: Service's spec.selector routes traffic to pods. Service's metadata.labels is the Service's own identity. ServiceMonitors and Ingress rules select by labels, not selector. Conflating these causes silent failures.
Phase 3 — Observability (Assignment 12)

What you built: kube-prometheus-stack via Helm (Prometheus + Grafana + Node Exporter + kube-state-metrics), ServiceMonitor wiring your app, PrometheusRule for CPU alerting, PromQL queries in both UIs.

Key takeaways:

Metrics vs logs: metrics are numbers over time (CPU%, request rate, error count). Logs are text records of events. Different tools, different questions. Prometheus is for metrics; EFK/Loki is for logs.
Pull model: Prometheus scrapes targets on a schedule. Apps don't push to Prometheus. A target that goes silent is automatically detected as down. Your app has been exposing /metrics since Assignment 6 — Prometheus just found it now.
ServiceMonitor = the discovery contract. It tells the Prometheus Operator "scrape Services matching these labels in these namespaces." The Operator translates it into Prometheus config. You never edit prometheus.yml directly.
release: kube-prometheus label = the frequency dial. Prometheus only picks up ServiceMonitors carrying the label it's configured to watch. Missing label = silently ignored, no error. Debug via Status → Service Discovery.
Service labels vs selector (again, different context): the ServiceMonitor keep rule filters by __meta_kubernetes_service_label_*. If your Service has no labels (only a selector), the keep rule drops every target silently. The dropped state in Service Discovery means a relabeling rule eliminated the target before scraping.
PromQL basics: app_requests_total = raw counter (total since start). rate(app_requests_total[5m]) = requests per second over last 5 minutes. Rate is the important one — SLOs, dashboards, and alerts are almost always built on rates, not raw counters.
Alert states: INACTIVE (condition not met, healthy), PENDING (threshold crossed but for: window hasn't elapsed), FIRING (sustained breach, notification sent). The for: duration prevents alert storms from transient spikes.
Liveness probes must not check dependencies — same principle as before, but now you can see it in the metrics: a liveness rule that checks DB latency would fire during every DB hiccup, restarting pods while the DB recovers, compounding the problem.
values.yaml over --set flags: versionable, readable, reproducible. helm upgrade -f values.yaml is the same command forever regardless of how many settings change.
kube-state-metrics = Kubernetes object metrics (pod restarts, HPA replica counts, deployment status) as queryable time-series. Node Exporter = OS metrics (CPU, memory, disk) from the node itself. Both are DaemonSet or Deployment patterns that ship with the meta-chart.
