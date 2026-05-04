---
description: "Retake screenshots and regenerate thumbnails for the what-is-mam slideshow video. Renders the title-card slide via main_slide_generator.py render-slides, opens URLs and a local HTML source in the VS Code integrated browser, captures 1280×720 screenshots (saved as 2560×1440 at 2× DPR), then runs main_slide_generator.py make-thumbs to scale each slide down to a 480×270 thumbnail. Images live in misc/what-is-mam/img/."
agent: "agent"
tools: ["open_browser_page", "navigate_page", "run_playwright_code", "run_in_terminal"]
---

Retake the slide screenshots and regenerate thumbnails for [misc/what-is-mam/script.md](../../misc/what-is-mam/script.md).

Follow these steps exactly:

## 1. Title card — render via Python

Run `.venv\Scripts\python.exe py\main_slide_generator.py render-slides --deck what-is-mam title-card` from the repo root.
This writes `misc/what-is-mam/img/slide-title-card.png` directly (no browser needed).

## 2. Sefaria — Genesis 1

Open `https://www.sefaria.org/Genesis.1?lang=he&aliyot=0` in the integrated browser.
Set viewport to 1280×720, wait 3 seconds for the page to fully render, then save:
- `misc/what-is-mam/img/slide-sefaria.png`

## 3. Hebrew Wikisource — MAM main page

Navigate to `https://he.wikisource.org/wiki/%D7%9E%D7%A7%D7%A8%D7%90_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94#%D7%A8%D7%90%D7%A9`.
Set viewport to 1280×720, wait 2 seconds, then save:
- `misc/what-is-mam/img/slide-wikisource.png`

## 4. Al-Hatorah — Miqraot Gedolot (Vayikra 21:1)

Navigate to `https://mg.alhatorah.org/Full/Vayikra/21.1#e0nf`.
Set viewport to 1280×720, press `Escape` to dismiss any popups, wait 3 seconds, then save:
- `misc/what-is-mam/img/slide-alhatorah.png`

## 5. Phonetic Tanakh — local HTML source

Open `misc/what-is-mam/img-sources/phonetic-psalms1.html` as a `file://` URL in the integrated browser.
Set viewport to 1280×720, wait 2 seconds for the page to fully render, then save:
- `misc/what-is-mam/img/slide-phonetic.png`

## 6. Generate thumbnails

Run `.venv\Scripts\python.exe py\main_slide_generator.py make-thumbs --deck what-is-mam` from the repo root.
This reads every `misc/what-is-mam/img/slide-*.png` and writes a corresponding
`misc/what-is-mam/img/thumb-*.png` scaled to 480×270 (portrait slides scale to fit height) using Pillow LANCZOS.

## 7. Verify

View `misc/what-is-mam/img/slide-title-card.png`, `misc/what-is-mam/img/slide-sefaria.png`,
`misc/what-is-mam/img/slide-wikisource.png`, `misc/what-is-mam/img/slide-alhatorah.png`, and
`misc/what-is-mam/img/slide-phonetic.png` to confirm they look correct (no unwanted
popups, content visible). Report any issues.
