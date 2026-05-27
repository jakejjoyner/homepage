# Deploying jakejoyner.com

The site is a static site deployed to **Cloudflare Pages** by the GitHub Actions
workflow at [`.github/workflows/deploy.yml`](workflows/deploy.yml).

**Push to `main` → it deploys.** That's the whole workflow. A broken deploy
shows up as a red ✗ on the commit / in the Actions tab, never silently.

## One-time setup

Already done in the repo:
- `CLOUDFLARE_ACCOUNT_ID` repo secret (account `Jakejoyner9@gmail.com`).

You need to do these once:

1. **Create a Cloudflare API token.** Cloudflare dashboard → My Profile →
   API Tokens → Create Token → *Custom token* with this permission:
   - `Account` · `Cloudflare Pages` · `Edit`

   Scope it to your account. Copy the token (you only see it once).

2. **Store it as a repo secret** (the value never needs to be pasted anywhere
   it's logged — `gh` reads it from your terminal):
   ```sh
   gh secret set CLOUDFLARE_API_TOKEN -R jakejjoyner/homepage
   # paste the token at the prompt, press Enter
   ```

3. **Create the Pages project once** (the CI deploy targets an existing
   project named `jakejoyner`):
   ```sh
   CLOUDFLARE_API_TOKEN=<token> npx wrangler pages project create jakejoyner \
     --production-branch=main
   ```
   (or create it in the dashboard: Workers & Pages → Create → Pages → name it
   `jakejoyner`, production branch `main`.)

## Going live

1. Merge to `main`. The workflow runs and publishes to
   `https://jakejoyner.pages.dev`. **Check that URL looks right.**
2. Cut the domain over: Cloudflare dashboard → Workers & Pages → `jakejoyner`
   → Custom domains → add `jakejoyner.com`. Cloudflare updates DNS
   automatically (apex via CNAME flattening, since the zone is already here).
3. Once the custom domain serves correctly, the old nginx origin can be
   retired. `nginx.conf` stays in the repo for reference but is not deployed
   to Pages (the workflow excludes it).
