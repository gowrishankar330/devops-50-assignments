# Associate DevOps Engineer — 50 Assignment Practice Repo

**Repo:** `devops-50-assignments`
**Thread app:** one small API (Node.js or Python) reused across all assignments.
**Rule:** local (kind/minikube) unless marked `[AWS]`. Destroy AWS resources after every session.
**Per-assignment deliverable:** working code + a short `README.md` in its folder documenting what you built, why, and what broke.

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done

---

## Phase 0 — Setup (do once)
- [ ] Install: Docker, kind, kubectl, helm, terraform, tflint, tfsec, awscli
- [ ] Create the thread app: tiny API with `/health`, `/metrics` (Prometheus format), one CRUD endpoint
- [ ] AWS billing alert at £10, budget alarm email
- [ ] Repo structure:
```
devops-50-assignments/
├── app/                  # the thread app
├── terraform/            # assignments 1-5, 13-15, 21, 27, 30, 32, 36-37, 47
├── kubernetes/           # per-assignment folders
├── cicd/                 # workflow files referenced by .github/workflows/
├── observability/        # 11, 12, 41, 45
├── security/             # 17, 18, 20, 28, 31, 34, 44, 49
├── chaos/                # 14, 38, 43
├── docs/                 # 42 + capstone docs
└── capstone/             # assignment 50
```

---

## Phase 1 — Docker & CI/CD Foundations (local, free)
- [ ] **6. GitHub Actions CI/CD with Multi-Stage Docker** — tests → Trivy scan → build → push to ECR (or GHCR to stay free) → deploy; fail on HIGH+ vulnerabilities
- [ ] **17. Docker Security Hardening** — non-root user, multi-stage build, minimal base image, remove unnecessary packages
- [ ] **39. Docker Image Optimization** — reduce image size by 60%, document the process
- [ ] **16. CI/CD with Manual Approval Gate** — build → scan → staging → manual approval → production
- [ ] **26. CI Pipeline Parallelization** — parallel tests, dependency caching, 40% runtime reduction
- [ ] **44. CI/CD Secrets Management** — prevent secrets being committed, logged, or leaked

## Phase 2 — Kubernetes Core (kind/minikube, free)
- [ ] **7. Self-Healing Kubernetes App** — app crashes randomly, restarts automatically; liveness & readiness probes; logs proving self-healing
- [ ] **8. Horizontal & Vertical Scaling** — CPU-based HPA, VPA if supported, load test to trigger scaling, document behavior
- [ ] **9. Kubernetes RBAC Isolation** — namespace per team, read-only Role, RoleBinding per user, block cross-namespace access
- [ ] **10. Ingress with TLS** — NGINX Ingress Controller, Let's Encrypt cert (use cert-manager + self-signed locally), domain routing, HTTPS redirect
- [ ] **29. Rolling Restart with Zero Downtime** — maintain 100% uptime, monitor availability during restart
- [ ] **40. Kubernetes Resource Optimization** — CPU/memory limits, prevent OOMKilled pods
- [ ] **22. Kubernetes Stateful Application** — MySQL StatefulSet, persistent storage, stable network identity, backup mechanism

## Phase 3 — Observability (local, free)
- [ ] **12. Prometheus Monitoring Stack** — Prometheus, Grafana, Node Exporter, custom app metrics, CPU alert rule
- [ ] **11. Centralized Logging Stack** — EFK (Elasticsearch, Fluentd, Kibana), collect all pod logs, filter by namespace, dashboard
- [ ] **45. Application Observability** — distributed tracing, Prometheus metrics, structured logs
- [ ] **41. Audit Logging** — Kubernetes audit logs, detect unauthorized access

## Phase 4 — Terraform & AWS `[AWS — destroy after each session]`
- [ ] **1. Multi-Environment Terraform Architecture** — modules, separate state per env, S3 + DynamoDB remote backend, workspaces or folder strategy, tagging, env-specific variables
- [ ] **3. Secure VPC Architecture** — public/private subnets, NAT Gateway, bastion, private EC2, restrictive SGs, document traffic flow *(NAT GW costs ~$0.05/hr — destroy same day)*
- [ ] **2. Highly Available Web Tier** — 2 EC2 in different AZs, ALB, ASG, CloudWatch scaling alarms, zero-downtime rolling updates
- [ ] **4. Terraform State Recovery** — simulate state deletion, recover via `terraform import`, handle drift, step-by-step docs
- [ ] **21. Terraform Module Registry** — reusable EC2/SG/EBS module, publish internally
- [ ] **32. Infrastructure CI Validation** — `terraform validate`, tflint, tfsec in pipeline, fail on issues
- [ ] **27. Infrastructure Drift Detection** — scheduled `terraform plan` automation, Slack alert on drift
- [ ] **13. Python S3 Sync Tool (Advanced)** — checksum comparison, resumable uploads, multi-threading, auto-delete removed files
- [ ] **15. Infrastructure Cost Optimization** — identify idle EC2 and unattached volumes, cost report, optimization strategy
- [ ] **30. Automated Backup Strategy** — RDS snapshots, S3 versioning, restore validation

## Phase 5 — Deployment Strategies & GitOps (mostly local)
- [ ] **23. GitOps with ArgoCD** — manifest repo, ArgoCD sync, auto-rollback on drift
- [ ] **24. Auto-Rollback on Health Failure** — deployment + health probe + automatic rollback
- [ ] **19. Canary Deployment** — 10% traffic to new version, monitor error rate, promote automatically
- [ ] **5. Blue/Green Deployment (AWS + K8s)** `[AWS]` — Node.js app on EKS, ALB, v1/v2, gradual traffic switch, rollback on failure *(consider kind + NGINX ingress weights to avoid EKS cost; do EKS version once, same week as 33)*
- [ ] **37. Blue/Green Infrastructure** `[AWS]` — separate VPC per environment, DNS cutover, rollback validation
- [ ] **36. Multi-Region Deployment** `[AWS]` — two regions, Route53 failover routing, health checks

## Phase 6 — Security Deep-Dive (local, free)
- [ ] **18. Kubernetes Network Policies** — deny-all, allow frontend→backend only, block backend→frontend, verify with curl
- [ ] **28. Pod Security Standards** — restricted policy, block privileged containers and hostPath mounts
- [ ] **25. Rate Limiting at Ingress** — request throttling, IP-based limits, HTTP 429
- [ ] **20. Vault Integration** — HashiCorp Vault, inject secrets into pods securely
- [ ] **34. Centralized Secrets Strategy** — compare K8s secrets vs Vault vs AWS Secrets Manager, implement one securely
- [ ] **31. Container Image Signing** — Cosign signing, verification before deployment
- [ ] **49. DevSecOps Integration** — SAST scan, dependency scan, container scan, infrastructure scan in one pipeline

## Phase 7 — Operations, Chaos & Advanced (local unless marked)
- [ ] **33. Kubernetes Cluster Upgrade** — minor version upgrade, zero downtime, rollback plan *(kind makes this cheap to practice)*
- [ ] **35. Autoscaling on Custom Metrics** — scale on requests-per-second (Prometheus Adapter or KEDA)
- [ ] **14. Disaster Recovery Simulation** — node failure, AZ failure, etcd corruption; recover without downtime
- [ ] **43. Chaos Engineering Test** — pod deletion, node failure, traffic spike; document system response
- [ ] **38. Network Troubleshooting Scenario** — service unreachable; debug with kubectl logs/describe, tcpdump, network policy checks
- [ ] **48. Kubernetes Multi-Tenancy Model** — namespace isolation, resource quotas, network segmentation
- [ ] **46. Custom Kubernetes Operator (Basic)** — watches a CRD, creates pods automatically
- [ ] **47. Infrastructure Performance Benchmark** `[AWS]` — EC2 performance, network latency, disk IO, compare instance types *(use small instances, short-lived)*

## Phase 8 — Capstone
- [ ] **42. Infrastructure Diagram & Documentation** — architecture diagram, network flow, security flow
- [ ] **50. End-to-End Production-Grade Project** — Terraform infra + K8s cluster + CI/CD + monitoring + logging + security + autoscaling + GitOps + DR plan. Documented as a production-ready solution. *This is assembly of Phases 1–7 — do it last, put it on GitHub as your flagship portfolio repo.*

---

## Working method with Claude
1. Start each assignment by asking Claude: "why does this exist / what problem does it solve" — before touching code.
2. Attempt the build yourself first. Bring Claude errors and design questions, not "write it for me".
3. After completing, ask Claude to review the solution like an interviewer and probe weak spots.
4. Write the folder README in your own words — this doubles as interview prep.

## Cost guardrails
- kind/minikube for all Kubernetes assignments except 5 and 33 (do the EKS versions in one concentrated week).
- `terraform destroy` at end of every AWS session — no exceptions.
- NAT Gateway, ALB, EKS control plane, and RDS are the silent money-burners. Never leave them overnight.
