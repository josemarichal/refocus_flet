# Refocus

A 30-day goal adherence tracker. Tap circles daily. Fill the month.

---

## Open on Android

1. Install the **Flet** app from [Google Play](https://play.google.com/store/apps/details?id=io.flet.flet)
2. Tap **Connect** and scan this QR code:

<!-- After deploying to Railway, replace the URL below with your actual app URL.  -->
<!-- Generate a QR at https://qr.io, save as qr.png in the repo, then uncomment: -->
<!-- ![Scan to open Refocus](qr.png) -->

**Your app URL:** `https://YOUR-APP-NAME.up.railway.app`

> To generate the QR: visit [qr.io](https://qr.io), paste your Railway URL,
> download the PNG, add it to the repo as `qr.png`, then uncomment the image line above.

---

## Deploy your own

1. Fork this repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select this repo — Railway auto-detects `railway.toml` and deploys
4. Copy your public URL from the Railway dashboard
5. Generate a QR code for it and add to this README

---

## Run locally

```bash
pip install flet
flet run main.py
```

## Features

- Today view — tap to cycle each goal: empty → done → partial
- Month view — 30-day circle grid with adherence %, streak, completions
- Progress saves automatically between sessions
- 12 goals preloaded, all editable
