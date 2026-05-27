# Deploying jakejoyner.com

The site is a static site served by **Cloudflare Workers** static assets
(see [`wrangler.jsonc`](../wrangler.jsonc): `name: homepage`,
`assets.directory: "."`), deployed by the GitHub Actions workflow at
[`.github/workflows/deploy.yml`](workflows/deploy.yml).

**Push to `main` → it deploys** (`wrangler deploy`). A broken deploy shows up as
a red ✗ on the commit / in the Actions tab, never silently. Repo-only files
(`.git`, `.github`, `.claude`, `nginx.conf`, …) are kept out of the upload by
[`.assetsignore`](../.assetsignore).

## One-time setup

Already done in the repo:
- `CLOUDFLARE_ACCOUNT_ID` repo secret (account `Jakejoyner9@gmail.com`).

Still needed for the GitHub Actions auto-deploy to run green:

1. **Create a Cloudflare API token.** Cloudflare dashboard → My Profile →
   API Tokens → Create Token. Use the **"Edit Cloudflare Workers"** template
   (or a custom token with `Account · Workers Scripts · Edit`), scoped to your
   account. Copy the token (you only see it once).

2. **Store it as a repo secret** (`gh` reads the value from your terminal, so it
   never lands in shell history or a file):
   ```sh
   gh secret set CLOUDFLARE_API_TOKEN -R jakejjoyner/homepage
   # paste the token at the prompt, press Enter
   ```

Until that secret exists, the Actions deploy will fail — deploy locally in the
meantime with `npx wrangler deploy` (uses your logged-in `wrangler`).

## Notes

- The Worker is `homepage`, reachable at `homepage.jakejoyner9.workers.dev`.
  Point `jakejoyner.com` at it via a custom domain on the Worker (Cloudflare
  dashboard → Workers & Pages → `homepage` → Settings → Domains & Routes).
- `nginx.conf` stays in the repo for reference (the retired origin) but is not
  uploaded as an asset.
