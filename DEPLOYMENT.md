# Deployment Guide

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Git
- AWS account (for staging/production)

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/odoo-enterprise-dev.git
cd odoo-enterprise-dev
```

### 2. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```bash
DB_HOST=postgres
DB_PORT=5432
DB_USER=odoo
DB_PASSWORD=secure_password_here
DB_NAME=odoo

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@example.com
SMTP_PASSWORD=your_smtp_password
SMTP_SSL=True
```

### 3. Start Services

```bash
docker-compose up -d
```

### 4. Access Odoo

- Odoo Web Interface: http://localhost:8069
- Adminer (Database GUI): http://localhost:8080

### 5. Initial Setup

1. Access http://localhost:8069
2. Create a new database
3. Install "Project Management" module from Apps

## Docker Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f odoo
docker-compose logs -f postgres
```

### Rebuild Containers
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Access Container Shell
```bash
docker-compose exec odoo bash
docker-compose exec postgres psql -U odoo
```

## Running Tests

### Local Tests

```bash
# Make script executable
chmod +x scripts/test.sh

# Run tests
./scripts/test.sh
```

### Run Specific Test

```bash
docker-compose exec odoo odoo -d odoo_test --test-enable --stop-after-init -i custom_module
```

## Backup and Restore

### Create Backup

```bash
chmod +x scripts/backup.sh
./scripts/backup.sh
```

Backups are stored in `./backups/` directory.

### Restore Backup

```bash
# List available backups
ls backups/

# Restore specific backup
docker-compose exec postgres pg_restore -C -d odoo backups/odoo_YYYYMMDD_HHMMSS.dump
```

## CI/CD Deployment

### GitHub Actions Setup

1. Go to Repository Settings → Secrets
2. Add these secrets:

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_REGION` | e.g., `us-east-1` |
| `DB_PASSWORD` | Production database password |

### Deploy to Staging

```bash
# Push to staging branch
git checkout staging
git merge main
git push origin staging
```

This triggers:
1. CI workflow (tests, linting)
2. CD workflow (build → push to ECR → deploy to ECS)

### Deploy to Production

```bash
# Create release tag
git tag -a v1.0.0 -m "Production release v1.0.0"
git push origin v1.0.0
```

## AWS ECS Deployment

### Prerequisites

- AWS CLI configured
- ECR repository created
- ECS cluster created
- IAM roles configured

### Manual Deploy

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t odoo-staging .

# Tag and push
docker tag odoo-staging:latest <account>.dkr.ecr.us-east-1.amazonaws.com/odoo-staging:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/odoo-staging:latest

# Update ECS service
aws ecs update-service --cluster odoo-staging --service odoo-service --force-new-deployment
```

## Troubleshooting

### Common Issues

#### Odoo won't start
```bash
# Check logs
docker-compose logs odoo

# Common fix: remove container and rebuild
docker-compose down -v
docker-compose up -d
```

#### Database connection error
```bash
# Check PostgreSQL
docker-compose logs postgres

# Verify credentials in .env
```

#### Port already in use
```bash
# Find process using port
lsof -i :8069

# Kill process or change port in docker-compose.yml
```

### Health Check

```bash
# Check container status
docker-compose ps

# Check Odoo health
curl http://localhost:8069/web/health
```

## Security Checklist

- [ ] Change default admin password
- [ ] Use strong database passwords
- [ ] Enable SSL/HTTPS in production
- [ ] Configure firewall rules
- [ ] Regular backups
- [ ] Rotate secrets periodically

## Maintenance

### Update Odoo Version

```bash
# Update Dockerfile base image
# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

### Clean Up

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Full cleanup
docker system prune -a
```
