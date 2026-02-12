# Plan: Robust GitHub Actions Deployment Pipeline

## Summary
We will fix the current GitHub Actions workflow to reliably build, push, and deploy Docker images to the VPS. The core issue is GHCR authentication (403 Forbidden). We will resolve this by generating a specific PAT with `read:packages` scope and configuring it on the VPS. We will also verify the `docker-compose.yml` on the VPS matches the GHCR image paths.

## Technical Context
- **CI/CD**: GitHub Actions (`.github/workflows/deploy.yml`)
- **Registry**: GitHub Container Registry (GHCR)
- **Deployment Target**: Contabo VPS (Ubuntu/Docker)
- **Orchestration**: Docker Compose (remote execution via SSH)

## Project Structure
- `.github/workflows/deploy.yml`: The automation script.
- `docker-compose.yml`: The local development config.
- `docker-compose.prod.yml`: The production config (to be created/verified on VPS).

## Implementation Steps

### Phase 1: Authentication & Permissions
1. **Generate PAT**: Create a GitHub Personal Access Token (PAT) with `read:packages` scope.
2. **Update VPS Secrets**: Store this PAT in GitHub Secrets as `CR_PAT`.
3. **Verify GHCR Visibility**: Ensure the package visibility settings allow access.

### Phase 2: Workflow Enhancement
1. **Update `deploy.yml`**:
   - Add explicit login to GHCR using the PAT (or `GITHUB_TOKEN` if permissions allow).
   - Verify `GITHUB_TOKEN` permissions in the workflow file (`contents: read`, `packages: write`).
   - Add a step to `docker login ghcr.io -u <user> -p <token>` on the VPS via SSH.

### Phase 3: VPS Configuration
1. **Create `docker-compose.prod.yml`**: Define the production services using `image: ghcr.io/a2mus/gold-tracker-dz/...`.
2. **Transfer Config**: Use `scp` or `ssh` to copy this file to `~/production/gold-tracker-dz/docker-compose.yml`.
3. **Environment Variables**: Ensure `.env` exists on VPS with production values.

### Phase 4: Verification
1. **Trigger Manual Deploy**: Push a commit or dispatch workflow.
2. **Verify Logs**: Check GitHub Actions logs for successful push.
3. **Verify VPS**: SSH into VPS and check `docker ps` to see new containers running.

## Complexity Tracking
- **Authentication**: High risk of failure if token scopes are wrong.
- **Network**: SSH connection might fail or timeout.
- **Rollback**: Manual rollback via SSH if deployment breaks.

## Decision Log
- **Decision**: Use `docker-compose.prod.yml` template but copy it as `docker-compose.yml` on VPS for simplicity.
- **Decision**: Authenticate on VPS using `docker login` with a PAT passed as an environment variable or secret, NOT hardcoded.

## Next Steps
- User must generate the PAT.
- I will guide them through the process.
