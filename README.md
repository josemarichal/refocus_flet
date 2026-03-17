# Refocus — Flet Android App

A 30-day goal tracker built with [Flet](https://flet.dev), Python's Flutter framework.

## Setup

```bash
pip install flet
```

## Run on desktop (preview)

```bash
cd refocus_flet
flet run main.py
```

## Run on Android

1. Install the **Flet** app from the Google Play Store on your phone
2. On your computer, run:
   ```bash
   flet run --android main.py
   ```
3. Scan the QR code shown in your terminal with the Flet app

## Build a standalone APK

```bash
flet build apk
```

The APK will be in `build/apk/`. Transfer it to your phone and install
(you may need to allow installs from unknown sources in Settings).

## Features

- **Today view** — tap each goal's circle to cycle: empty → done → partial
- **Month view** — full 30-day grid per goal with adherence %, streak, and completion count
- **Persistent storage** — progress saves automatically between sessions
- Deep purple palette, "wrestle with god" sits apart with italic styling
