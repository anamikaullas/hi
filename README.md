# Rekhalex Module 1 (Vercel version)

Same enhancement pipeline as the local version, adjusted for Vercel:

- No files are saved. The enhanced image comes back in the same response.
- The browser shrinks large scans to about 2000 px before upload, because
  Vercel limits request and response bodies to 4.5 MB.
- Greyscale results are sent as JPEG, black and white results as PNG.
- `public/` holds the web page. `app.py` holds the Flask `app` that Vercel runs.

## Run locally first

```bash
python -m venv .venv
.venv\Scripts\activate          # Mac/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
python app.py                   # http://127.0.0.1:5000
python -m pytest -q tests
```

## Deploy

See DEPLOY.md.
