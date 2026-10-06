# Shared Lab

A small public collection of selected interactive graphs and calculators.

- Collection: https://fenerax.github.io/shared-lab/
- Revenant comparison: https://fenerax.github.io/shared-lab/rs3/revenants/
- Published files: `docs/`; editable graph source: `src/`.
- GitHub Pages publishes `main`, directory `/docs`.

## Add a graph

Export the selected graph as a self-contained, standalone HTML document. For Codex inline visualizations, use the Visualize skill's `scripts/render.py` exporter, which supplies the browser state bridge.

Import it with Python 3:

```powershell
python scripts/add-artifact.py path/to/export.html --slug category/project --title "Project title" --description "What visitors can explore"
```

Use `--replace` to update an existing project, `--updated YYYY-MM-DD` to set its research date, and `--notes path/to/footer.html` to attach model assumptions and sources. The importer adds a link back to the collection and rebuilds its index. It does not commit or publish anything.

Review the selected content, then commit and push to `main`. Pages deploys it to the same URL. Never import secrets, private notes or artifacts that were not chosen for public sharing. Source in this repository is public too.

The hosted revenant page loads pinned D3 7.9.0 from jsDelivr. Inputs persist locally in each browser; this site has no shared database, account system or analytics.

## Preview locally

```powershell
python -m http.server 8080 --bind 127.0.0.1 --directory docs
```

Use an available port and stop your preview server when done.

## Add login later

GitHub Pages is the initial public host. `wrangler.jsonc` prepares the same `docs/` folder for Cloudflare Workers Static Assets:

```powershell
npx wrangler deploy
```

This requires signing into a Cloudflare account. After migration, Cloudflare Access can protect the production hostname and previews with an email allowlist and email one-time PINs. Enable it on the whole site, including its static assets. Verify that anonymous requests are denied, then disable the public GitHub Pages site; otherwise its old URL remains a public copy. Keep protected content in a private source repository.

No login protection is currently enabled. An unlisted URL is still public.
