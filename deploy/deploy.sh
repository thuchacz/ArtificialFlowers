#!/usr/bin/env bash
# Builds the edition against the test server's address and deploys it.
# Usage: ./deploy/deploy.sh <droplet-ip-or-hostname>
# Rerun after any TEI change to update the test site.
set -euo pipefail
cd "$(dirname "$0")/.."

HOST="${1:?usage: deploy.sh <droplet-ip-or-hostname>}"
BASE_URL="http://$HOST/ArtificialFlowers/"
REMOTE="${DEPLOY_USER:-root}@$HOST"

echo "==> Regenerating edition data against $BASE_URL"
npx editioncrafter process -i artificial_flowers.xml -o public -u "$BASE_URL"
npx editioncrafter database -i artificial_flowers.xml -o public/artificial_flowers.sqlite
sqlite3 public/artificial_flowers.sqlite "PRAGMA wal_checkpoint(TRUNCATE); PRAGMA journal_mode=DELETE;"
rm -f public/artificial_flowers.sqlite-shm public/artificial_flowers.sqlite-wal

echo "==> Building static site"
npm run build

echo "==> Restoring production URLs in public/ (deployed copy lives in dist/)"
git checkout -- public

echo "==> Syncing dist/ to $REMOTE:/var/www/ArtificialFlowers/"
rsync -az --delete -e "ssh -o StrictHostKeyChecking=accept-new" dist/ "$REMOTE:/var/www/ArtificialFlowers/"

echo "==> Smoke tests"
for path in "" "artificial_flowers/iiif/manifest.json" "artificial_flowers.sqlite"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://$HOST/ArtificialFlowers/$path")
  echo "  /$path -> $code"
  [ "$code" = "200" ] || { echo "FAILED: $path returned $code"; exit 1; }
done

echo
echo "Deployed. Viewer: http://$HOST/ArtificialFlowers/#/ec"
