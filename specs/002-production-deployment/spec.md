# Feature: Robust GitHub Actions Deployment Pipeline

> Ensure reliable, automated deployments from GitHub to Production (VPS) using GitHub Actions and GHCR.

## Problem Statement
The current deployment process is manual and brittle. Images are pushed to GHCR, but the VPS often fails to pull them due to `403 Forbidden` errors (package visibility). Manual intervention (pulling images, restarting containers) is frequent. We need a "push-to-deploy" system that just works.

## Actors
- **Developer (Mus)**: Pushes code to GitHub.
- **GitHub Actions**: Builds Docker images, pushes to GHCR, triggers VPS deployment.
- **VPS (Production)**: Pulls images, restarts containers.
- **End User**: Accesses the updated Gold Tracker website.

## User Stories

### P1: Automated Build & Push
As a **Developer**, I want my code changes automatically built into Docker images and pushed to a secure registry (GHCR) whenever I merge to `main`, so that I don't have to build locally.
- **Acceptance Criteria**:
  - API, Scraper, and Web images are built successfully.
  - Images are tagged with `latest` and `sha`.
  - Images are pushed to `ghcr.io/a2mus/gold-tracker-dz`.
  - Build cache is used to speed up subsequent builds.

### P1: Authorized VPS Pull
As the **System Operator**, I want the VPS to authenticate securely with GHCR to pull private images without `403 Forbidden` errors, so that deployments succeed reliably.
- **Acceptance Criteria**:
  - VPS can `docker pull` images from GHCR without interactive login.
  - Uses a PAT or Deploy Key with `read:packages` scope.
  - Credentials are managed securely (not hardcoded).

### P2: Zero-Downtime Deployment
As an **End User**, I want to access the site without interruption during updates, so that I always see the latest gold prices.
- **Acceptance Criteria**:
  - New containers start before old ones stop (rolling update) OR downtime is < 10s.
  - Database schema migrations run automatically (if needed).
  - Old images are pruned to save disk space.

### P3: Deployment Notification
As a **Developer**, I want to receive a Telegram notification when a deployment succeeds or fails, so I know the status immediately.
- **Acceptance Criteria**:
  - Telegram message sent to private channel.
  - Includes status (Success/Fail), commit hash, and link.

## Requirements

### Functional
- **FR-001**: GitHub Actions workflow must trigger on `push` to `main`.
- **FR-002**: Images must be multi-arch (amd64) compatible with VPS.
- **FR-003**: VPS must execute `docker compose up -d` remotely via SSH.
- **FR-004**: Database data must persist across deployments (volume mapping).

### Non-Functional
- **NFR-001**: Deployment time should be < 5 minutes.
- **NFR-002**: Secrets (SSH keys, tokens) must be stored in GitHub Secrets.
- **NFR-003**: VPS security: SSH access restricted to specific keys.

## Open Questions
- [ ] **Q1**: Do we use `docker-compose.prod.yml` on the VPS, or just override `docker-compose.yml`?
- [ ] **Q2**: Should we use `watchtower` for auto-updates, or stick to explicit SSH commands? (Decision: SSH commands for control).

## Success Metrics
- Deployment success rate > 95%.
- Time from merge to live < 5 mins.
- Zero manual SSH logins required for updates.
