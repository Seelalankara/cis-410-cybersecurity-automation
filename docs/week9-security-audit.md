# Week 9 Security Audit — cis410-deploy-sa

**Project:** cis410-saddhamgama
**Date:** 2026-06-10
**Auditor:** saddhamgama seelalankara

---

## 1. IAM Audit Results

### Before — Week 8 Configuration (over-permissioned)

| Role | Scope | Problem |
|---|---|---|
| roles/run.admin | Project | Overly broad — grants ability to delete services and modify IAM, not just deploy |
| roles/storage.admin | Project | Overly broad — grants access to ALL GCS buckets in the project |
| roles/artifactregistry.writer | Project | Acceptable — scoped to push images only |
| roles/viewer | Project | Acceptable — read-only project metadata |
| roles/compute.networkAdmin | Project | Required for network configuration |

### After — Week 9 Least-Privilege Fix

| Role | Scope | Why Sufficient |
|---|---|---|
| roles/run.developer | Project | Deploy only — cannot delete services or modify IAM |
| roles/storage.admin | tfstate bucket only | Scoped to one bucket — not all storage |
| roles/artifactregistry.writer | Project | Unchanged — push images only |
| roles/viewer | Project | Unchanged — read project metadata |
| roles/compute.networkAdmin | Project | Unchanged — required for network configuration |

---

## 2. Secret Manager Migration

- **Secret created:** `flask-app-secret`
- **Replication:** automatic
- **Access granted to:** `cis410-deploy-sa` — roles/secretmanager.secretAccessor on this secret only
- **Access granted to:** `70505545403-compute@developer.gserviceaccount.com` — roles/secretmanager.secretAccessor on this secret only
- **Cloud Run update:** APP_SECRET environment variable mounted from Secret Manager at runtime

---

## 3. Monitoring Configuration

- **Log-based alert:** `cis410-flask-app-alert` — fires on severity>=WARNING for cis410-flask-app
- **Notification channel:** sseelalankara@gmail.com
- **Billing budget:** `cis410-monthly-budget` — $20 limit, alerts at 50% / 90% / 100%

---

## 4. Reflection

**Q1: Why is roles/run.admin inappropriate for a CI/CD pipeline service account?**

roles/run.admin grants excessive permissions beyond what a deployment pipeline needs, including the ability to delete services, modify traffic splits, and change IAM policies on Cloud Run services. A CI/CD pipeline only needs to deploy new revisions, which roles/run.developer provides. Granting run.admin violates the principle of least privilege and creates unnecessary risk if the service account is compromised.

---

**Q2: What is the security difference between storing a secret in GitHub Secrets vs. Google Secret Manager?**

GitHub Secrets are encrypted variables stored in the repository and injected into workflows at deploy time, making them harder to audit and rotate. Google Secret Manager stores secrets in GCP with full audit logging of every access, fine-grained IAM controls, and automatic versioning. With Secret Manager, the application fetches the secret at runtime rather than baking it into the deployment pipeline, reducing the attack surface.

---

**Q3: A coworker says "I will clean up IAM permissions after the project launches. For now I need everything to work fast." What is the risk of this approach?**

Over-permissioned service accounts create a large attack surface — if the account is compromised before cleanup, an attacker has broad access to the entire project. In practice, permission cleanup rarely happens after launch because teams move on to new priorities, leaving the project permanently over-permissioned. It is much safer and faster to apply least privilege from the start rather than retrofitting security controls later.
