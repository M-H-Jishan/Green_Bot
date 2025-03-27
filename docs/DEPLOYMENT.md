# Green Bot Deployment Guide

## Deployment Options

### 1. Docker Deployment (Recommended)

#### Prerequisites
- Docker
- Docker Compose
- Domain name (optional)

#### Steps

1. Build Docker images:
```bash
docker-compose build
```

2. Start services:
```bash
docker-compose up -d
```

3. Initialize database:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

4. Configure Nginx:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /app/static/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

### 2. Traditional Server Deployment

#### Prerequisites
- Python 3.8+
- PostgreSQL
- Nginx
- Supervisor

#### Steps

1. Set up Python environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configure Gunicorn:
```bash
# /etc/supervisor/conf.d/greenbot.conf
[program:greenbot]
command=/path/to/venv/bin/gunicorn ChatbotServer.wsgi:application
directory=/path/to/project
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
```

3. Configure Nginx:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

4. Set up SSL (recommended):
```bash
certbot --nginx -d your-domain.com
```

## Environment Configuration

### Production Settings

1. Update `.env`:
```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DJANGO_SETTINGS_MODULE=ChatbotServer.settings.production
DATABASE_URL=postgres://user:pass@db:5432/greenbot
OPENAI_API_KEY=your-key
```

2. Configure Django settings:
```python
# settings/production.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
```

### Database Setup

1. Create PostgreSQL database:
```sql
CREATE DATABASE greenbot;
CREATE USER greenbot_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE greenbot TO greenbot_user;
```

2. Configure backup:
```bash
# /etc/cron.daily/backup-greenbot
#!/bin/bash
pg_dump greenbot | gzip > /backup/greenbot-$(date +%Y%m%d).sql.gz
```

## Scaling Considerations

### 1. Load Balancing
```nginx
upstream greenbot {
    server web1:8000;
    server web2:8000;
    server web3:8000;
}

server {
    location / {
        proxy_pass http://greenbot;
    }
}
```

### 2. Caching
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
```

### 3. Database Optimization
```sql
CREATE INDEX idx_kb_question ON knowledgebase(question);
CREATE INDEX idx_kb_category ON knowledgebase(category_id);
CREATE INDEX idx_kb_intent ON knowledgebase(intent_id);
```

## Monitoring

### 1. Prometheus Configuration
```yaml
scrape_configs:
  - job_name: 'greenbot'
    static_configs:
      - targets: ['localhost:8000']
```

### 2. Grafana Dashboard
- Request rates
- Response times
- Error rates
- System resources

### 3. Logging
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/greenbot/app.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

## Backup Strategy

### 1. Database Backup
```bash
# Daily backups
0 0 * * * pg_dump greenbot | gzip > /backup/db/greenbot-$(date +%Y%m%d).sql.gz

# Keep last 30 days
find /backup/db/ -mtime +30 -delete
```

### 2. Media Files Backup
```bash
# Weekly backups
0 0 * * 0 tar -czf /backup/media/media-$(date +%Y%m%d).tar.gz /path/to/media/
```

## Security Checklist

- [ ] SSL/TLS enabled
- [ ] Secure headers configured
- [ ] Rate limiting implemented
- [ ] API authentication required
- [ ] Database backups automated
- [ ] Firewall configured
- [ ] Regular security updates
- [ ] Monitoring in place

## Troubleshooting

### Common Issues

1. **502 Bad Gateway**
   - Check Gunicorn status
   - Verify Nginx configuration
   - Check application logs

2. **Slow Response Times**
   - Monitor database queries
   - Check cache hit rates
   - Review system resources

3. **High Memory Usage**
   - Adjust Gunicorn workers
   - Optimize database queries
   - Review memory leaks

## Maintenance

### Regular Tasks
1. Update dependencies
2. Rotate logs
3. Monitor disk space
4. Check backup integrity
5. Review security updates

### Emergency Procedures
1. Database rollback process
2. Quick server restart
3. SSL certificate renewal
4. Error escalation plan
