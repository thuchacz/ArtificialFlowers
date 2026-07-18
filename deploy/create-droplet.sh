#!/usr/bin/env bash
# Creates the ArtificialFlowers test-site droplet.
# Prerequisite: doctl auth init   (needs a DigitalOcean API token with write scope)
# Usage: ./deploy/create-droplet.sh
set -euo pipefail
cd "$(dirname "$0")/.."

NAME="${DROPLET_NAME:-af-test-site}"
REGION="${DROPLET_REGION:-sfo3}"
SIZE="${DROPLET_SIZE:-s-1vcpu-1gb}"
IMAGE="${DROPLET_IMAGE:-ubuntu-24-04-x64}"
PUBKEY="${SSH_PUBKEY:-$HOME/.ssh/id_ed25519.pub}"

doctl account get >/dev/null || { echo "doctl is not authenticated - run: doctl auth init"; exit 1; }

if doctl compute droplet list --format Name --no-header | grep -qx "$NAME"; then
  echo "Droplet '$NAME' already exists:"
  doctl compute droplet list --format Name,PublicIPv4,Region,Status --no-header | grep "^$NAME"
  exit 0
fi

# ensure the local SSH key is registered with DO
FP=$(ssh-keygen -lf "$PUBKEY" -E md5 | awk '{print $2}' | sed 's/^MD5://')
KEY_ID=$(doctl compute ssh-key list --format ID,FingerPrint --no-header | awk -v fp="$FP" '$2==fp {print $1}')
if [ -z "$KEY_ID" ]; then
  echo "Importing $PUBKEY to DigitalOcean..."
  KEY_ID=$(doctl compute ssh-key import "af-test-$(basename "$PUBKEY" .pub)" --public-key-file "$PUBKEY" --format ID --no-header)
fi

echo "Creating droplet $NAME ($SIZE, $IMAGE, $REGION)..."
doctl compute droplet create "$NAME" \
  --size "$SIZE" --image "$IMAGE" --region "$REGION" \
  --ssh-keys "$KEY_ID" \
  --user-data-file deploy/cloud-init.yml \
  --tag-name af-test \
  --wait

IP=$(doctl compute droplet list --format Name,PublicIPv4 --no-header | awk -v n="$NAME" '$1==n {print $2}')
echo
echo "Droplet ready: $IP"
echo "cloud-init needs a minute or two to install nginx; then run:"
echo "  ./deploy/deploy.sh $IP"
