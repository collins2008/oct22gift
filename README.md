# 💌 "Open When" Romantic Website

A mobile-first interactive "Open When" letter website built with pure HTML, CSS, and vanilla JavaScript. 

Features a nostalgic pastel pink gingham aesthetic, torn-paper note cards with organic drop shadows, cute animated character stickers, an interactive runaway "No" button, unsealable maroon envelopes, and polaroid photos.

Audited and approved by a 5-specialist review board (QA Tester, Performance Engineer, Designer, Emotional Editor, and Security Lead). 

---

## ✨ Features

- **📱 Mobile-First Experience:** Built specifically for phone viewports (390×844 iPhone, 360×740 Android), with an elegant centered column layout on desktop.
- **🎀 Authentic Aesthetic:** Mathematically seamless pastel pink gingham wallpaper, transparent floral accents, and torn-paper cards.
- **🐱 Interactive Character Stickers:** High-resolution transparent stickers of shy cats and bear pairs with gentle idle bobbing animations that never block buttons.
- **🏃‍♂️ Playful Evasion Interaction:** A "No" button on Screen 2 that darts away within safe bounds, scales down to 0.55 without ever disappearing, and ensures they say "Yes".
- **✉️ Unsealable Maroon Envelopes:** 5 envelopes with upward flaps and peeking stationery cards reading *"with love"* that open on tap.
- **📸 Framed Polaroid Letters:** Letters render with elegant Playfair Display serif typography and tilted polaroid photo frames.
- **⚡ Blazing Fast Performance:** Initial paint is under **180 ms**; Time to Interactive on Slow 4G is **0.19 seconds**; total deploy assets are **under 250 KB**.
- **📴 100% Offline Ready:** Built-in Service Worker (`sw.js` v4) caches all assets so your partner can read their letters on airplanes, trains, or with no signal.
- **🔒 Private & Secure:** Stripped of all photo EXIF/GPS metadata; blocked from search engines via `robots.txt` and `<meta name="robots" content="noindex">`.
- **🔗 Rich Social Previews:** WhatsApp and iMessage preview image (`Assets/og_preview.png`, <50 KB) and heart favicon.

---

## 🚀 Quick Start (Local Viewing)

### Option 1: Direct Double-Click
Double-click [`index.html`](file:///c:/Users/Collins%20Ibilibor/Documents/local/Desktop/Gift/index.html) to open in any modern browser.

### Option 2: Local HTTP Server (Recommended for PWA/Service Worker testing)
Open PowerShell or Terminal in this folder and run:
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000` in your browser.

---

## 🎨 How to Personalize & Customize

All customizable content is conveniently grouped in [`script.js`](file:///c:/Users/Collins%20Ibilibor/Documents/local/Desktop/Gift/script.js):

### 1. Change Partner Name & Introductory Text
Edit the `CONFIG` object at line 9:
```javascript
const CONFIG = {
  intro1: 'I made something for you',
  intro2: 'Will you see it?',
  intro3: 'please say yes!',
  intro4: 'are you ready for the surprise?',
  btn1: 'what?',
  btn2yes: 'yes',
  btn2no: 'no',
  btn3: 'fine',
  btn4: 'yes!!'
};
```

### 2. Edit or Add Letters
In `script.js`, find the `LETTERS` array (lines 24–76). Each letter is an object:
```javascript
{
  id: 'miss-me',
  label: 'you miss me', // Label under the envelope
  text: "Hey love, if you're reading this...", // The letter message
  font: 'serif', // 'serif' (Playfair Display) or 'hand' (Caveat)
  bg: 'heart', // 'heart' (pink heart crumpled paper) or 'gingham'
  photo: 'Assets/photo_love.webp', // Set to null if no photo, or path to image
  caption: 'I love you', // Caption under polaroid photo
  character: 'Assets/tkthao219-bubududu.webp' // Peeking corner sticker
}
```

### 3. Add Custom Photos
1. Copy your photo into the `Assets/` directory.
2. In `script.js`, set `photo: 'Assets/your_photo.jpg'` on any letter.
3. The site frames it as a vintage Polaroid with a gentle tilt!

### 4. Add Background Music (Optional)
1. Place your MP3 audio file named `music.mp3` into `Assets/`.
2. In `index.html`, set `<audio id="bg-music" src="Assets/music.mp3" preload="none" loop></audio>`.
3. The circular button in the bottom right will play and pause music with saved state.

---

## 🌐 Deployment, Updates & Rollback

### Free 60-Second Deployment via Netlify Drop:
1. Go to **[app.netlify.com/drop](https://app.netlify.com/drop)**.
2. Drag and drop this entire project folder into the upload window.
3. Netlify will generate a live HTTPS link (e.g., `https://sweet-gift-for-her.netlify.app`) with custom cache headers from `_headers` active!

### How to Update After Deployment:
1. Make your changes to letters or photos.
2. In `sw.js`, bump the cache version name (e.g. from `open-when-v4` to `open-when-v5`).
3. Drag the updated folder onto Netlify Drop.
4. Because `sw.js` uses `self.skipWaiting()` and `self.clients.claim()`, your partner's phone will seamlessly update to the latest letters on their next visit!

### How to Roll Back:
1. In your Netlify site dashboard, navigate to **Deploys**.
2. Click on any previous deploy timestamp and select **"Restore deploy"**.
3. The site rolls back instantly with zero downtime.

---

## 📂 Project Architecture

```text
├── Assets/                        # Production-ready optimized WebP/PNG assets
│   ├── gingham_clean.png          # Seamless pastel pink gingham wallpaper (0.6 KB)
│   ├── flower_top_right.webp      # Transparent corner flower (30 KB)
│   ├── heart_wallpaper.webp       # Crumpled paper heart background (77 KB)
│   ├── char_cat_shy.webp          # Shy cat sticker (3.7 KB)
│   ├── char_bubu_bouquet.webp     # Couple with bouquet sticker (4.1 KB)
│   ├── char_cat_lying.webp        # Pleading cat sticker (2.4 KB)
│   ├── tkthao219-bubududu.webp    # Hugging bears sticker (6.4 KB)
│   ├── og_preview.png             # WhatsApp preview thumbnail (<50 KB)
│   ├── favicon.ico / favicon.png  # Browser favicons
│   └── raw/                       # Source sticker sheets & uncompressed archives
├── index.html                     # Semantic HTML5 markup, meta tags, and accessibility
├── style.css                      # Complete responsive styling & inlined WOFF2 fonts
├── script.js                      # Screen flow, evasion logic, sound, and letters data
├── 404.html                       # Romantic custom 404 page
├── sw.js                          # Service Worker v4 (Cache-First offline PWA)
├── _headers                       # Security CSP and caching headers
├── robots.txt                     # Disallows search engine crawlers
├── SPEC.md                        # Screen-by-screen architectural specification
├── REVIEW_LOG.md                  # Comprehensive QA audit & test log (Passes 1 & 2)
└── SUGGESTIONS.md                 # Top 10 ranked suggestions & future enhancements
```
