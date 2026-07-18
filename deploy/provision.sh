#!/usr/bin/env bash
# Provisions nginx on a droplet that was created WITHOUT deploy/cloud-init.yml
# (e.g. via the DigitalOcean web console). Idempotent - safe to rerun.
# Usage: ./deploy/provision.sh <droplet-ip-or-hostname>
set -euo pipefail

HOST="${1:?usage: provision.sh <droplet-ip-or-hostname>}"
REMOTE="${DEPLOY_USER:-root}@$HOST"

ssh -o StrictHostKeyChecking=accept-new "$REMOTE" 'bash -s' <<'REMOTE_SCRIPT'
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
command -v nginx >/dev/null || { apt-get update -q && apt-get install -y -q nginx; }
mkdir -p /var/www/ArtificialFlowers

cat > /etc/nginx/sites-available/artificialflowers <<'NGINX'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    root /var/www;

    location = / {
        return 302 /ArtificialFlowers/;
    }

    location /ArtificialFlowers/ {
        alias /var/www/ArtificialFlowers/;
        index index.html;
        try_files $uri $uri/ =404;
    }
}
NGINX

rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/artificialflowers /etc/nginx/sites-enabled/artificialflowers
nginx -t
systemctl enable --now nginx
systemctl reload nginx
echo "provisioned OK"
REMOTE_SCRIPT

echo "Done. Next: ./deploy/deploy.sh $HOST"
