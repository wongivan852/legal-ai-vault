# SSL Certificate Setup

This directory should contain your SSL/TLS certificates for HTTPS.

## Option 1: Let's Encrypt (Recommended)

### Install Certbot

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# RHEL/CentOS
sudo yum install certbot python3-certbot-nginx
```

### Generate Certificate

```bash
# Stop nginx temporarily
docker-compose --profile production stop nginx

# Generate certificate (replace yourdomain.com)
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Certificates will be stored in: /etc/letsencrypt/live/yourdomain.com/
# - fullchain.pem (certificate)
# - privkey.pem (private key)
```

### Update nginx.conf

Edit `/home/user/legal-ai-vault/nginx/nginx.conf`:

```nginx
ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
```

### Update docker-compose.yml

Add volume mount for Let's Encrypt certificates:

```yaml
nginx:
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    - /etc/letsencrypt:/etc/letsencrypt:ro
```

### Auto-Renewal

```bash
# Add cron job for auto-renewal
sudo crontab -e

# Add this line (runs twice daily)
0 0,12 * * * certbot renew --quiet && docker-compose --profile production restart nginx
```

## Option 2: Self-Signed Certificate (Development Only)

### Generate Self-Signed Certificate

```bash
# Generate private key and certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /home/user/legal-ai-vault/nginx/ssl/key.pem \
  -out /home/user/legal-ai-vault/nginx/ssl/cert.pem \
  -subj "/C=HK/ST=HongKong/L=HongKong/O=VaultAI/CN=localhost"
```

### Update nginx.conf

```nginx
ssl_certificate /etc/nginx/ssl/cert.pem;
ssl_certificate_key /etc/nginx/ssl/key.pem;
```

**WARNING**: Self-signed certificates will show security warnings in browsers. Only use for development/testing.

## Option 3: Commercial Certificate

If you purchased an SSL certificate:

1. Upload your certificate files to this directory:
   - `cert.pem` - Your certificate
   - `key.pem` - Your private key
   - `chain.pem` - Certificate chain (optional)

2. Set proper permissions:
```bash
chmod 600 /home/user/legal-ai-vault/nginx/ssl/key.pem
chmod 644 /home/user/legal-ai-vault/nginx/ssl/cert.pem
```

3. Update nginx.conf:
```nginx
ssl_certificate /etc/nginx/ssl/cert.pem;
ssl_certificate_key /etc/nginx/ssl/key.pem;
ssl_trusted_certificate /etc/nginx/ssl/chain.pem;  # if you have it
```

## Verify SSL Configuration

After setting up SSL:

```bash
# Test nginx configuration
docker-compose --profile production exec nginx nginx -t

# Restart nginx
docker-compose --profile production restart nginx

# Check SSL with OpenSSL
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Check SSL rating (online tool)
# https://www.ssllabs.com/ssltest/
```

## Security Best Practices

1. **Keep private keys secure**: Never commit `.pem` files to git
2. **Use strong ciphers**: The nginx.conf includes modern cipher suites
3. **Enable HSTS**: Already configured in nginx.conf
4. **Monitor expiry**: Set up alerts for certificate expiration
5. **Use TLS 1.2+**: Older versions are disabled in config

## Troubleshooting

### Certificate not trusted
- Make sure you're using the full certificate chain
- Check that your domain DNS is properly configured

### Permission denied
```bash
sudo chown -R root:root /home/user/legal-ai-vault/nginx/ssl
sudo chmod 755 /home/user/legal-ai-vault/nginx/ssl
sudo chmod 600 /home/user/legal-ai-vault/nginx/ssl/*.pem
```

### Nginx won't start
```bash
# Check nginx logs
docker-compose --profile production logs nginx

# Verify certificate files exist
ls -la /home/user/legal-ai-vault/nginx/ssl/

# Test nginx config
docker-compose --profile production run --rm nginx nginx -t
```
