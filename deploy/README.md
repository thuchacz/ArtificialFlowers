# Test-Site Deployment (DigitalOcean droplet)

Stages the `tag-explorer` branch on a droplet so the editors can review the semantic
markup in the live Tag Explorer without merging PR #1.

## One-time setup

1. Authenticate doctl (needs an API token with write scope from
   https://cloud.digitalocean.com/account/api/tokens):

   ```sh
   doctl auth init
   ```

2. Create and provision the droplet (~$6/mo; nginx is installed automatically via
   cloud-init):

   ```sh
   ./deploy/create-droplet.sh
   ```

   Defaults: name `af-test-site`, region `sfo3`, size `s-1vcpu-1gb`, Ubuntu 24.04,
   SSH key `~/.ssh/id_ed25519.pub`. Override via env vars (`DROPLET_NAME`,
   `DROPLET_REGION`, `DROPLET_SIZE`, `SSH_PUBKEY`).

## Deploy (and redeploy after TEI changes)

```sh
./deploy/deploy.sh <droplet-ip>
```

This regenerates the edition data against the droplet's address (the generated
partials/manifest embed an absolute base URL — see "Semantic Tag Filtering" in the
main README), builds the static site, rsyncs `dist/` to the droplet, restores the
production URLs in `public/` so they don't get committed by accident, and smoke-tests
the deployed manifest and tag database.

Viewer URL: `http://<droplet-ip>/ArtificialFlowers/#/ec`

## Teardown

```sh
doctl compute droplet delete af-test-site
```

## Notes

- Plain HTTP on a bare IP — fine for an editors' preview. For HTTPS, point a
  hostname at the droplet, install certbot (`apt install certbot
  python3-certbot-nginx && certbot --nginx`), and redeploy with the hostname so the
  baked base URL matches.
- The droplet serves only static files; Node/npm run locally, never on the server.
