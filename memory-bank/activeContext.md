# Active Context

> Current focus: Production Deployment Pipeline

## Current Focus
Establishing a robust CI/CD pipeline using GitHub Actions to build Docker images, push to GHCR, and deploy to the VPS.

## Recent Changes
- Activated Speckit Protocol.
- Configured GitHub Actions workflow `deploy.yml`.
- Created production docker-compose configuration.

## Open Questions
- GHCR image visibility (Private vs Public) - need to ensure VPS can pull.
- Database backups - need a strategy for TimescaleDB data persistence.

## Next Steps
- Verify `deploy.yml` correctly transfers the production compose file.
- Push changes to GitHub to trigger the first full deployment.
