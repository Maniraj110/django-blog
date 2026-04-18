# Django Blog - Deployment Guide

Quick setup guide for local and AWS deployment.

## Table of Contents

- [Local Development Setup](#local-development-setup)
- [AWS Production Deployment](#aws-production-deployment)
- [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites

- Python 3.8+
- PostgreSQL (or SQLite for quick start)
- Git
- Virtual Environment

### Step 1: Clone & Setup

```bash
git clone https://github.com/Maniraj/django-blog.git
cd django-blog
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Create .env File

```bash
# Create .env in project root
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here
DB_NAME=django_blog
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 4: Setup Database

```bash
# Create database (PostgreSQL)
psql -U postgres -c "CREATE DATABASE django_blog;"

# Or use SQLite (no setup needed, just run migrations)
```

### Step 5: Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Step 6: Start Development Server

```bash
python manage.py runserver
```

Visit: `http://localhost:8000`  
Admin: `http://localhost:8000/admin`

---

## AWS Production Deployment

### Prerequisites

- AWS Account (Free Tier)
- EC2 instance (Ubuntu 22.04, t2.micro)
- RDS PostgreSQL database
- S3 bucket
- IAM user with S3 access

### Quick Start (5 Steps)

#### Step 1: Create AWS Resources

**RDS Database:**

```bash
# Create database
psql -h your-rds-endpoint -U postgres -c "CREATE DATABASE django_blog;"
```

**S3 Bucket:**

- Go to AWS S3 → Create bucket
- Name: `django-blog-assets-yourname`
- Uncheck "Block all public access"
- Add bucket policy for public read access

**IAM User:**

- Go to IAM → Create user
- Attach `AmazonS3FullAccess` policy
- Create access keys

#### Step 2: Launch EC2 Instance

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git nginx
```

#### Step 3: Deploy Application

```bash
# Clone repository
cd /home/ubuntu
git clone https://github.com/Maniraj/django-blog.git
cd django-blog

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
nano .env
```

**Add to .env:**

```
DEBUG=False
SECRET_KEY=your_generated_secret_key
DB_NAME=django_blog
DB_USER=postgres
DB_PASSWORD=your_rds_password
DB_HOST=your-rds-endpoint.rds.amazonaws.com
ALLOWED_HOSTS=your-ec2-ip,yourdomain.com
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=django-blog-assets-yourname
AWS_S3_REGION_NAME=us-east-1
```

#### Step 4: Setup Services

```bash
# Create Gunicorn service
sudo nano /etc/systemd/system/gunicorn.service
```

**Paste:**

```ini
[Unit]
Description=gunicorn daemon for django-blog
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/django-blog
Environment="PATH=/home/ubuntu/django-blog/venv/bin"
ExecStart=/home/ubuntu/django-blog/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          blog_main.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Enable Gunicorn:**

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

**Configure Nginx:**

```bash
sudo nano /etc/nginx/sites-available/django-blog
```

**Paste:**

```nginx
server {
    listen 80;
    server_name your_ec2_ip;
    client_max_body_size 100M;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

**Enable Nginx:**

```bash
sudo ln -s /etc/nginx/sites-available/django-blog /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```

#### Step 5: Run Migrations & Collect Static Files

```bash
cd /home/ubuntu/django-blog
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### Access Your Application

```
http://your-ec2-public-ip
```

Admin: `http://your-ec2-public-ip/admin`

---

## Deployment Checklist

### Before Going Live

- [ ] Set `DEBUG=False` in .env
- [ ] Generate strong `SECRET_KEY`
- [ ] Update `ALLOWED_HOSTS` with your IP/domain
- [ ] Configure RDS security group (allow port 5432 from EC2)
- [ ] Configure EC2 security group (allow ports 22, 80, 443)
- [ ] Configure S3 bucket policy for public access
- [ ] Create IAM user with S3 permissions
- [ ] Test uploads (images should go to S3)
- [ ] Run migrations on production database
- [ ] Create superuser on production
- [ ] Collect static files to S3

### Monitoring

```bash
# Check Gunicorn status
sudo systemctl status gunicorn

# Check Nginx status
sudo systemctl status nginx

# View Gunicorn logs
sudo journalctl -u gunicorn -n 50

# View Nginx errors
sudo tail -f /var/log/nginx/error.log
```

---

## Quick Restart Commands

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Check status
sudo systemctl status gunicorn
sudo systemctl status nginx
```

---

## Troubleshooting

### 502 Bad Gateway

**Problem:** Nginx can't reach Gunicorn

**Solution:**

```bash
sudo systemctl restart gunicorn
sudo journalctl -u gunicorn -n 20
```

### Permission Denied on Socket

**Problem:** `Permission denied` in Nginx logs

**Solution:**
Update `/etc/systemd/system/gunicorn.service` to use `Group=www-data`

```bash
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

### Database Connection Failed

**Problem:** `Connection timed out` to RDS

**Solution:**

- Check RDS security group allows port 5432
- Add EC2 security group to RDS inbound rules
- Verify credentials in `.env`

### Images Not Uploading

**Problem:** Files not appearing in S3

**Solution:**

- Check IAM user has S3 permissions
- Verify bucket name in `.env`
- Restart Gunicorn: `sudo systemctl restart gunicorn`

### Static Files 404

**Problem:** CSS/JS not loading

**Solution:**

```bash
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

---

## Environment Variables Reference

| Variable        | Local                 | Production            |
| --------------- | --------------------- | --------------------- |
| `DEBUG`         | `True`                | `False`               |
| `SECRET_KEY`    | Development key       | Strong generated key  |
| `DB_HOST`       | `localhost`           | RDS endpoint          |
| `DB_USER`       | `postgres`            | `postgres`            |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Your EC2 IP or domain |
| `AWS_*`         | Not needed            | Required for S3       |

---

## Security Tips

✅ **Do:**

- Keep `.env` out of version control
- Use strong passwords
- Enable HTTPS (use Certbot)
- Restrict security group access
- Regular backups

❌ **Don't:**

- Commit secrets to GitHub
- Use `DEBUG=True` in production
- Leave SSH open to 0.0.0.0/0
- Use default AWS credentials

---

## Deploy Script (for quick redeployment)

Create `/home/ubuntu/deploy.sh`:

```bash
#!/bin/bash
cd /home/ubuntu/django-blog
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart nginx
echo "Deployment complete!"
```

**Usage:**

```bash
chmod +x /home/ubuntu/deploy.sh
./deploy.sh
```

---

## Useful Links

- [Django Docs](https://docs.djangoproject.com/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [Gunicorn Docs](https://gunicorn.org/)
- [Nginx Docs](https://nginx.org/en/docs/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

## Support

- Check logs: `sudo journalctl -u gunicorn -n 50`
- Check Nginx: `sudo tail -f /var/log/nginx/error.log`
- Django shell: `python manage.py shell`
- Test connection: `psql -h rds-endpoint -U postgres -d django_blog`

**Last Updated:** April 18, 2026  
**Version:** 1.0
