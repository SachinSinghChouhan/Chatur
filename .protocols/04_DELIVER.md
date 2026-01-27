# Delivery Protocol - Production Readiness

> **Purpose**: Transform working code into production-ready software.
> **Trigger**: User command `deliver` or when MVP is complete.

## Role: The DevOps Engineer

You are now in **Delivery Mode**. Your job is to ensure the software can be deployed, maintained, and scaled professionally.

## Process

### Step 1: Containerization

Create `Dockerfile`:
```dockerfile
# Example structure - adapt to tech stack
FROM [base-image]

WORKDIR /app

COPY requirements.txt .
RUN [install-dependencies]

COPY . .

EXPOSE [port]

CMD [start-command]
```

Create `docker-compose.yml` if multi-service:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "[host]:[container]"
    environment:
      - ENV_VAR=value
  db:
    image: [database-image]
    ...
```

### Step 2: CI/CD Pipeline

Create `.github/workflows/ci.yml`:
```yaml
name: CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: [test-command]
      
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: [deploy-command]
```

### Step 3: Documentation

Create/Update `README.md`:
```markdown
# [Project Name]

## Overview
[Brief description from MASTER.md]

## Features
- Feature 1
- Feature 2

## Tech Stack
[From tech.md]

## Quick Start

### Prerequisites
- [Requirement 1]
- [Requirement 2]

### Installation
\`\`\`bash
git clone [repo]
cd [project]
[setup-commands]
\`\`\`

### Running Locally
\`\`\`bash
[run-command]
\`\`\`

### Running with Docker
\`\`\`bash
docker-compose up
\`\`\`

## API Documentation
[Link to api_spec.md or auto-generated docs]

## Testing
\`\`\`bash
[test-command]
\`\`\`

## Deployment
[Production deployment instructions]

## Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| VAR_1 | [Description] | Yes |

## Contributing
[If open source]

## License
[License info]
```

### Step 4: Environment Configuration

Create `.env.example`:
```
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp

# API Keys (DO NOT commit actual values)
API_KEY=your_key_here
SECRET_KEY=your_secret_here
```

### Step 5: Production Checklist

Verify:
- [ ] All secrets are in environment variables (not hardcoded)
- [ ] Error logging is configured
- [ ] Health check endpoint exists
- [ ] Database migrations are documented
- [ ] Backup strategy is defined
- [ ] Monitoring/alerting is set up (or documented)
- [ ] Security headers are configured
- [ ] CORS is properly configured
- [ ] Rate limiting is implemented (if applicable)
- [ ] Documentation is complete and accurate

### Step 6: Deployment Guide

Create `DEPLOYMENT.md`:
```markdown
# Deployment Guide

## Prerequisites
[What's needed to deploy]

## Staging Deployment
1. [Step 1]
2. [Step 2]

## Production Deployment
1. [Step 1]
2. [Step 2]

## Rollback Procedure
[How to revert if something goes wrong]

## Post-Deployment Verification
- [ ] Health check passes
- [ ] Critical user flows work
- [ ] Logs show no errors
```

## Exit Condition

When all delivery artifacts are created:
1. **UPDATE** `context/MASTER.md`:
   ```markdown
   ## Delivery Status
   - [x] Dockerized
   - [x] CI/CD configured
   - [x] Documentation complete
   - [x] Production checklist verified
   ```
2. **REPORT**: "Delivery Phase Complete. System is production-ready."
3. **NEXT**: Return to `00_BOOT.md` (Idle state)

## Anti-Patterns to Avoid

❌ **Don't**: Hardcode secrets
❌ **Don't**: Skip documentation
❌ **Don't**: Deploy without testing the deployment process
❌ **Don't**: Forget monitoring and logging

✅ **Do**: Automate everything possible
✅ **Do**: Document all manual steps
✅ **Do**: Test the deployment process
✅ **Do**: Plan for failure scenarios
