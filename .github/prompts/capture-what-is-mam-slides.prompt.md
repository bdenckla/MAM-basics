---
description: "Retake screenshots and regenerate thumbnails for the what-is-mam slideshow video. Opens each URL in the VS Code integrated browser, captures a 1280×720 slide screenshot (saved as 2560×1440 at 2× DPR), then runs py/main_make_thumbs.py to scale each slide down to a 480×270 thumbnail. Images live in doc/what-is-mam-img/."
agent: "agent"
tools: ["open_browser_page", "navigate_page", "run_playwright_code", "run_in_terminal"]
---

Retake the slide screenshots and regenerate thumbnails for [doc/what-is-mam.md](../../doc/what-is-mam.md).

Follow these steps exactly:

## 1. Sefaria — Genesis 1

Open `https://www.sefaria.org/Genesis.1?lang=he&aliyot=0` in the integrated browser.
Set viewport to 1280×720, wait 3 seconds for the page to fully render, then save:
- `doc/what-is-mam-img/slide-sefaria.png`

## 2. Hebrew Wikisource — MAM main page

Navigate to `https://he.wikisource.org/wiki/%D7%9E%D7%A7%D7%A8%D7%90_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94#%D7%A8%D7%90%D7%A9`.
Set viewport to 1280×720, wait 2 seconds, then save:
- `doc/what-is-mam-img/slide-wikisource.png`

## 3. Al-Hatorah — Miqraot Gedolot (Vayikra 21:1)

Navigate to `https://mg.alhatorah.org/Full/Vayikra/21.1#e0nf`.
Set viewport to 1280×720, press `Escape` to dismiss any popups, wait 3 seconds, then save:
- `doc/what-is-mam-img/slide-alhatorah.png`

## 4. Generate thumbnails

Run `.venv\Scripts\python.exe py\main_make_thumbs.py --images-dir doc\what-is-mam-img` from the repo root.
This script reads every `doc/what-is-mam-img/slide-*.png` and writes a corresponding
`doc/what-is-mam-img/thumb-*.png` scaled to 480×270 (portrait slides scale to fit height) using Pillow LANCZOS.

## 5. Verify

View `doc/what-is-mam-img/slide-sefaria.png`, `doc/what-is-mam-img/slide-wikisource.png`, and
`doc/what-is-mam-img/slide-alhatorah.png` to confirm they look correct (no unwanted
popups, content visible). Report any issues.
