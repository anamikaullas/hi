# Deploy to Vercel

## Option A: through GitHub (easiest, and gives you a redeploy on every push)

1. Make a free account at github.com and vercel.com (sign in to Vercel with GitHub).
2. On GitHub, click New repository, name it `rekhalex-module1`, leave it empty.
3. In VS Code, open this folder, open a terminal, then run:

   ```
   git init
   git add .
   git commit -m "Rekhalex module 1"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/rekhalex-module1.git
   git push -u origin main
   ```

4. On vercel.com choose Add New > Project, pick the repository, and press Deploy.
   Vercel detects the Flask app on its own. Leave every setting as it is.
5. Wait for the build (a minute or two). Open the link it gives you.

## Option B: Vercel command line

```
npm install -g vercel
vercel login
vercel deploy        # preview link
vercel deploy --prod # public link
```

## If something fails

- Build error mentioning a size limit: the Python bundle limit is 500 MB and this
  project is well under it, so check that `.venv` is not being uploaded
  (`.vercelignore` excludes it).
- Page loads but Enhance says "server took too long": the free plan has a time
  limit per request. Try a smaller image, or check your plan's function duration
  in the Vercel dashboard (Settings > Functions).
- "That file is too large": the browser could not shrink it (some TIFFs).
  Convert to JPG or PNG first.
- Page not found at /: make sure `public/index.html` exists in the repository.

## Things to know

- Anyone with the link can upload to it. Do not put real legal documents through a
  public deployment. Use Vercel's deployment protection (Settings > Deployment
  Protection) to make it private, or keep sensitive scans on the local version.
- Each request is handled from scratch, so the first request after a quiet period
  can be slower.
