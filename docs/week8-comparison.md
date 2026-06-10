# Week 8 Lab Exercise — On-Premise Docker vs. Cloud Run

## Comparison Table

| Dimension | On-Premise Docker (Weeks 3–5) | Cloud Run (Week 8) |
|---|---|---|
| Infrastructure setup | 3 VMs created, Docker installed on each | No VMs needed — just pushed a Docker image |
| Deployment command | SSH → docker build → docker run | terraform apply or gcloud run deploy |
| TLS / HTTPS | Not configured | Automatic HTTPS — no configuration needed |
| Scaling approach | Manual — redeploy or add VMs | Automatic — scales to zero when idle |
| Port management | Ports 5000/5001/5002 per environment | No port config needed — handled automatically |
| Cost when idle | VM running 24/7 regardless of traffic | Zero cost — scales to zero with no traffic |
| Rollback | Re-deploy previous image manually | Deploy previous image tag |
| Secrets management | GitHub Secrets → env vars in workflow | GitHub Secrets → env vars in workflow |

## Reflection Questions

**Q1: Which approach required more manual steps from push to live URL?**
On-premise Docker required significantly more manual steps. Each deployment required SSHing into the VM, building the image on that machine, and restarting the container. Cloud Run eliminated SSH access, VM management, port configuration, and TLS setup — a single terraform apply handles everything.

**Q2: Audit trail — which version is running?**
With on-premise Docker using latest tags, there is no reliable way to trace a running container back to a specific commit. With Cloud Run and commit SHA tagging, you can run gcloud run services describe and see the exact image tag, then match that SHA to a specific commit in git log. This gives a complete audit trail for every deployment.

**Q3: Security advantage of scale-to-zero**
When no instances are running, there is no attack surface. A VM running 24/7 is constantly exposed with open ports and running processes that can be exploited even when no legitimate traffic is present. A scaled-to-zero Cloud Run service has nothing to attack between requests.

**Q4: Attack surface reduction**
SSH keys are static long-lived credentials that can be stolen or leaked in git history. OIDC tokens are short-lived and tied to a specific workflow run — there is nothing to steal and store. This eliminates the risk of credential exfiltration and removes the need to manage and rotate SSH keys entirely.