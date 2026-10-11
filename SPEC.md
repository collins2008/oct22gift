# "Open When" Website Specification

## 1. Visual Style and Theme
- **Backgrounds:**
  - *Gingham Background:* A seamless, pastel pink and cream gingham check pattern. Used on Intro screens, the Envelope Menu, and emotional Handwritten Letters. Includes a pink flower positioned in the top-right corner.
  - *Heart Paper Background:* A crumpled pink paper texture with a large, soft, dark rose/maroon heart motif. Used on standard Serif Letter screens.
- **Note Card (The Container):**
  - An off-white/pale pink card with jagged, torn-paper edges.
  - Center-aligned on the screen.
  - Features a soft drop shadow and a very slight random rotation (e.g., -1 to 1 degrees) to feel organic.
- **Typography:**
  - *Caveat (Handwritten):* Used for intro screens and the emotional letter screen. Text color is a reddish-pink (`#d4587a` approx).
  - *Playfair Display (Serif):* Used for standard letters. Text color is dark maroon/near-black.
- **Interactive Elements (Buttons):**
  - Pill-shaped buttons with a cream fill and a thin brown/gold border.
  - Text is lowercase, matching the handwritten style.
  - On tap, the button shrinks slightly (scale: 0.94) over 90ms.
- **Characters / Stickers:**
  - A white cat and a brown bear. They appear in different poses at the bottom of the card or peeking from the corners.
  - Gentle idle animation: bobbing up and down 3-4px over 2.5s (ease-in-out infinite).
  - Pop-in animation when entering the screen (250ms).

## 2. Screen Flow & Layout (Mobile-First, 390x844)

### Screen 1: Intro 1
- **Background:** Gingham with flower.
- **Card Text:** "I made something for you" (Caveat, pink).
- **Character:** White cat sits at the bottom-left of the card.
- **Button:** "what?" at the bottom-right.

### Screen 2: Intro 2
- **Background:** Gingham with flower.
- **Card Text:** "Will you see it?" (Caveat, pink).
- **Characters:** Bear and cat together in the middle.
- **Buttons:** "yes" (left) and "no" (right).
- **Interaction:** The "no" button runs away (translates randomly) when approached or tapped, shrinking slightly each time. After 3 attempts, it becomes impossible to click. "yes" continues the flow.

### Screen 3: Intro 3
- **Background:** Gingham with flower.
- **Card Text:** "please say yes!" (Caveat, pink).
- **Character:** Pleading white cat on the left.
- **Button:** "fine" on the right.

### Screen 4: Intro 4
- **Background:** Gingham with flower.
- **Card Text:** "yay are you ready for the surprise?"
- **Character:** Bear and cat hugging.
- **Button:** "yes!!"

### Screen 5: Transition & Envelope Menu
- **Transition:** A small maroon envelope appears, flips/opens.
- **Menu:** A grid of 5 small maroon envelopes on the torn card.
- **Labels:** Tiny labels on the flaps: "feeling low", "you miss me", "we argued", "you can't sleep", "you need a smile".
- **Interaction:** Hovering makes them wiggle. Tapping plays a flap-open animation (<400ms) and goes to the letter screen.

### Screen 6: Standard Letter Screen
- **Background:** Heart paper texture.
- **Card Text:** Playfair Display, centered, dark maroon, scrollable if long.
- **Extras:** 
  - Some letters include a framed photo (tilted, overlapping the card corner) with a caption (e.g., "I love you").
  - A circular blue/lavender back arrow button at the bottom.
  - A character peeking in from the bottom corner.

### Screen 7: Handwritten Letter Screen
- **Background:** Gingham with flower.
- **Card Text:** Caveat, pink, scrollable if long.
- **Extras:** Same back button and character peeking as Screen 6.

## 3. Animations and Audio
- **Transitions:** Screens fade in and slide up 12px over 200-250ms.
- **Audio:** A soft click sound on button tap, and optional background music (loaded on first tap, with a mute toggle).
- **Performance:** Use `transform` and `opacity` exclusively for animations. Respect `prefers-reduced-motion`.

## 4. Technical Constraints
- **Stack:** Plain HTML, CSS, Vanilla JS in a single page (`index.html`, `style.css`, `script.js`). No frameworks.
- **Data:** All letter content stored in a `LETTERS` array in `script.js`.
- **Assets:** Optimize images using a script (WebP, cropped, no metadata). Preload critical assets for Screen 1. Lazy-load the rest.
- **Caching:** Service worker (`sw.js`) for offline support and instant subsequent loads.
