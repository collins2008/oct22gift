// ==========================================
// OPEN WHEN – script.js
// Production Hardened Vanilla Interactions
// ==========================================

// ====== EDIT YOUR CONTENT HERE ======
const NAME = 'Baby'; // Replace with partner's nickname

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

// 5 Open When letters matching the reference envelopes:
// You can change 'text', 'photo' ('Assets/your_photo.jpg' or null),
// 'caption', 'font' ('serif' or 'hand'), and 'bg' ('heart' or 'gingham').
const LETTERS = [
  {
    id: 'miss-me',
    label: 'you miss me',
    text: "Hey love, if you're reading this, I'm guessing you're missing me. I miss you too, probably more than you know. Close your eyes and imagine me holding your hand, annoying you, making you laugh. Distance is temporary. What we have isn't. I'm always yours.",
    font: 'serif',
    bg: 'heart',
    photo: null,
    caption: 'I love you',
    character: 'Assets/bubu-kisses-dudu-bubu-dudu.webp'
  },
  {
    id: 'sad',
    label: "you're sad",
    text: "Hi baby. I hate the thought of you feeling low. Whatever happened, it doesn't define you. You're stronger, softer, and more beautiful than you realize. Let yourself feel it, but don't stay there. I'm right beside you in this, cheering you on, always.",
    font: 'serif',
    bg: 'heart',
    photo: null,
    caption: '',
    character: 'Assets/char_pack1_2.webp'
  },
  {
    id: 'happy',
    label: "you're happy",
    text: "Seeing you happy is literally my favorite thing in the world! Your smile lights up everything around you. Whatever made your day today, save this feeling and remember how bright you shine. Keep smiling, gorgeous!",
    font: 'serif',
    bg: 'heart',
    photo: null,
    caption: '',
    character: 'Assets/bubu-dudu.webp'
  },
  {
    id: 'hug',
    label: 'you need a hug',
    text: "Wrap your arms around yourself and squeeze tight—that's me hugging you from across the miles! Sending you the warmest, coziest, longest hug right now. You are safe, you are cherished, and I'm always here for you.",
    font: 'serif',
    bg: 'heart',
    photo: null,
    caption: '',
    character: 'Assets/bubu-dudu (1).webp'
  },
  {
    id: 'fight',
    label: 'we fight',
    text: "If we just argued, take a breath. I never want us to be against each other. It's us versus the problem, always. I love you more than my ego, more than being right. Let's talk, fix it, and choose each other again.",
    font: 'serif',
    bg: 'heart',
    photo: 'Assets/photo_love.webp', 
    caption: 'I love you',
    character: 'Assets/tkthao219-bubududu.webp'
  }
];
// ====== END EDIT AREA ======

document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const loader = document.getElementById('loader');
  const bgMusic = document.getElementById('bg-music');
  const globalBg = document.getElementById('global-bg');
  const flowerDecor = document.getElementById('flower-decor');
  const musicToggle = document.getElementById('music-toggle');
  const toastEl = document.getElementById('toast');

  // Populate Intro Text
  const tIntro1 = document.getElementById('t-intro1');
  const tIntro2 = document.getElementById('t-intro2');
  const tIntro3 = document.getElementById('t-intro3');
  const tIntro4 = document.getElementById('t-intro4');
  const btnWhat = document.getElementById('btn-what');
  const btnYes = document.getElementById('btn-yes');
  const btnNo = document.getElementById('btn-no');
  const btnFine = document.getElementById('btn-fine');
  const btnReady = document.getElementById('btn-ready');

  if (tIntro1) tIntro1.innerText = CONFIG.intro1;
  if (tIntro2) tIntro2.innerText = CONFIG.intro2;
  if (tIntro3) tIntro3.innerText = CONFIG.intro3;
  if (tIntro4) tIntro4.innerText = CONFIG.intro4;
  if (btnWhat) btnWhat.innerText = CONFIG.btn1;
  if (btnYes) btnYes.innerText = CONFIG.btn2yes;
  if (btnNo) btnNo.innerText = CONFIG.btn2no;
  if (btnFine) btnFine.innerText = CONFIG.btn3;
  if (btnReady) btnReady.innerText = CONFIG.btn4;

  // Audio Context & Acoustic Web Audio Click (zero network requests)
  let audioCtx = null;
  function playClick() {
    // Haptics on supported mobile devices
    if (typeof navigator !== 'undefined' && navigator.vibrate) {
      try { navigator.vibrate([15]); } catch (e) {}
    }
    // Web Audio Synthesizer
    try {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(820, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(160, audioCtx.currentTime + 0.035);
      gain.gain.setValueAtTime(0.09, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.035);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.035);
    } catch (e) {}
  }

  // Non-blocking toast notification helper
  let toastTimer = null;
  function showToast(message) {
    if (!toastEl) return;
    toastEl.innerText = message;
    toastEl.classList.remove('hidden');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toastEl.classList.add('hidden');
    }, 2400);
  }

  // Dismiss loader on window load
  window.addEventListener('load', () => {
    setTimeout(() => {
      if (loader) loader.classList.add('hidden');
    }, 350);
  });

  // State Management & Transitions
  let isTransitioning = false;

  function switchScreen(hideId, showId, pushToHistory = true) {
    if (isTransitioning) return;
    isTransitioning = true;
    playClick();

    const hideEl = document.getElementById(hideId);
    const showEl = document.getElementById(showId);

    if (hideEl) hideEl.classList.remove('active');

    if (pushToHistory && window.history) {
      window.history.pushState({ screen: showId }, '', `#${showId}`);
    }

    setTimeout(() => {
      if (showEl) showEl.classList.add('active');
      isTransitioning = false;
    }, 220);
  }

  // Restore screen on initial load / page refresh
  const initialHash = window.location.hash.replace('#', '');
  const validScreens = ['s-intro1', 's-intro2', 's-intro3', 's-intro4', 's-menu'];
  if (validScreens.includes(initialHash)) {
    document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
    const targetEl = document.getElementById(initialHash);
    if (targetEl) {
      targetEl.classList.add('active');
      if (window.history) {
        window.history.replaceState({ screen: initialHash }, '', `#${initialHash}`);
      }
    }
  } else {
    if (window.history) {
      window.history.replaceState({ screen: 's-intro1' }, '', '#s-intro1');
    }
  }

  // Handle browser back gesture & popstate across ALL screens
  window.addEventListener('popstate', (e) => {
    const hash = window.location.hash.replace('#', '');
    const targetScreen = (e.state && e.state.screen) 
      ? e.state.screen 
      : (validScreens.includes(hash) ? hash : 's-intro1');
      
    const currentActive = document.querySelector('.screen.active');
    if (!currentActive || currentActive.id === targetScreen) return;

    if (currentActive.id === 's-letter') {
      closeLetter(false);
    } else {
      currentActive.classList.remove('active');
      setTimeout(() => {
        const targetEl = document.getElementById(targetScreen);
        if (targetEl) targetEl.classList.add('active');
        isTransitioning = false;
      }, 220);
    }
  });

  window.addEventListener('hashchange', () => {
    const hash = window.location.hash.replace('#', '');
    if (validScreens.includes(hash)) {
      document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
      const targetEl = document.getElementById(hash);
      if (targetEl) targetEl.classList.add('active');
    }
  });

  // Navigation handlers
  if (btnWhat) btnWhat.addEventListener('click', () => switchScreen('s-intro1', 's-intro2'));
  if (btnYes) btnYes.addEventListener('click', () => switchScreen('s-intro2', 's-intro3'));
  if (btnFine) btnFine.addEventListener('click', () => switchScreen('s-intro3', 's-intro4'));
  if (btnReady) btnReady.addEventListener('click', () => switchScreen('s-intro4', 's-menu'));

  // Evasion Logic for "No" Button
  // Must NEVER leave screen, NEVER become invisible (min scale 0.55), and "yes" must always work
  let noBtnAttempts = 0;
  let noBtnScale = 1.0;

  function evadeNoBtn(e) {
    if (e && e.type === 'touchstart') {
      e.preventDefault();
    }
    noBtnAttempts++;
    // Keep scale between 0.55 and 1.0 so it never disappears
    noBtnScale = Math.max(0.55, 1.0 - (noBtnAttempts * 0.1));
    
    // Controlled, bounded offsets within card action row
    const offsets = [
      { x: 25, y: -18 },
      { x: 38, y: 14 },
      { x: 20, y: -28 },
      { x: 34, y: 22 },
      { x: 18, y: -12 }
    ];
    const off = offsets[noBtnAttempts % offsets.length];
    if (btnNo) {
      btnNo.style.transform = `translate(${off.x}px, ${off.y}px) scale(${noBtnScale})`;
    }
  }

  if (btnNo) {
    btnNo.addEventListener('mouseenter', evadeNoBtn);
    btnNo.addEventListener('touchstart', evadeNoBtn, { passive: false });
    btnNo.addEventListener('click', evadeNoBtn);
  }

  // Generate 5 Maroon Envelopes
  const envelopeGrid = document.getElementById('envelope-grid');
  if (envelopeGrid) {
    LETTERS.forEach(letter => {
      const item = document.createElement('div');
      item.className = 'envelope-item';
      item.setAttribute('role', 'button');
      item.setAttribute('tabindex', '0');
      item.setAttribute('aria-label', `Open when ${letter.label}`);
      item.innerHTML = `
        <div class="env-wrap">
          <div class="env-flap-up"></div>
          <div class="env-letter-peek">with love</div>
          <div class="env-body">
            <div class="env-label-strip">OPEN WHEN</div>
          </div>
        </div>
        <div class="env-bottom-label">${letter.label}</div>
      `;

      // Prefetch this letter's photo/sticker on hover or touchstart
      const prefetch = () => {
        if (letter.photo) {
          const img = new Image();
          img.src = letter.photo;
        }
        if (letter.character) {
          const img = new Image();
          img.src = letter.character;
        }
      };
      item.addEventListener('mouseenter', prefetch, { once: true });
      item.addEventListener('touchstart', prefetch, { once: true, passive: true });

      item.addEventListener('click', () => {
        const wrap = item.querySelector('.env-wrap');
        openLetter(letter, wrap);
      });

      envelopeGrid.appendChild(item);
    });
  }

  // Open Letter Screen with resilient fallbacks
  function openLetter(letter, envWrap) {
    if (isTransitioning) return;
    isTransitioning = true;
    playClick();

    if (envWrap) envWrap.classList.add('open');

    setTimeout(() => {
      const sMenu = document.getElementById('s-menu');
      const sLetter = document.getElementById('s-letter');
      const letterContainer = document.getElementById('letter-container');
      const letterTornImg = document.getElementById('letter-torn-img');
      const letterLayout = document.getElementById('letter-layout');
      const letterText = document.getElementById('letter-text');
      const charEl = document.getElementById('letter-character');
      const photoFrame = document.getElementById('letter-photo-frame');
      const photoImg = document.getElementById('letter-photo');
      const captionEl = document.getElementById('letter-caption');

      // Setup Background & Card Style
      if (!letter || letter.bg === 'heart') {
        if (globalBg) globalBg.className = 'bg-layer bg-heart';
        if (flowerDecor) flowerDecor.classList.add('hidden');
        if (letterContainer) letterContainer.className = 'simple-card';
        if (letterTornImg) letterTornImg.classList.add('hidden');
      } else {
        if (globalBg) globalBg.className = 'bg-layer bg-gingham';
        if (flowerDecor) flowerDecor.classList.remove('hidden');
        if (letterContainer) letterContainer.className = 'card-wrap';
        if (letterTornImg) letterTornImg.classList.remove('hidden');
      }

      // Font style
      if (letterText) {
        if (letter && letter.font === 'hand') {
          letterText.className = 'font-hand';
          letterText.style.fontSize = '1.75rem';
        } else {
          letterText.className = 'font-serif';
          letterText.style.fontSize = '1.05rem';
        }
        letterText.innerText = (letter && letter.text) ? letter.text : "I love you always and forever.";
      }

      // Character Sticker with error fallback
      if (charEl) {
        charEl.onerror = () => { charEl.style.display = 'none'; };
        if (letter && letter.character) {
          charEl.style.display = 'block';
          charEl.src = letter.character;
        } else {
          charEl.style.display = 'none';
        }
      }

      // Photo Frame with error fallback
      if (photoImg) {
        photoImg.onerror = () => {
          if (photoFrame) photoFrame.classList.add('hidden');
          if (letterLayout) letterLayout.classList.add('column');
        };
      }

      if (letter && letter.photo) {
        if (photoImg) photoImg.src = letter.photo;
        if (captionEl) captionEl.innerText = letter.caption || 'I love you';
        if (photoFrame) photoFrame.classList.remove('hidden');
        if (letterLayout) letterLayout.classList.remove('column');
      } else {
        if (photoFrame) photoFrame.classList.add('hidden');
        if (letterLayout) letterLayout.classList.add('column');
      }

      // Transition into Letter Screen
      if (sMenu) sMenu.classList.remove('active');
      if (window.history) {
        window.history.pushState({ screen: 's-letter' }, '', '#letter');
      }

      setTimeout(() => {
        if (sLetter) sLetter.classList.add('active');
        if (envWrap) envWrap.classList.remove('open');
        isTransitioning = false;
      }, 220);

    }, 380); // Wait for flap animation
  }

  // Back Button / Close Letter (Letter -> Menu)
  function closeLetter(pushToHistory = true) {
    if (isTransitioning) return;
    isTransitioning = true;
    playClick();

    const sLetter = document.getElementById('s-letter');
    const sMenu = document.getElementById('s-menu');

    if (sLetter) sLetter.classList.remove('active');

    if (pushToHistory && window.history) {
      window.history.pushState({ screen: 's-menu' }, '', '#s-menu');
    }

    setTimeout(() => {
      if (globalBg) globalBg.className = 'bg-layer bg-gingham';
      if (flowerDecor) flowerDecor.classList.remove('hidden');
      if (sMenu) sMenu.classList.add('active');
      isTransitioning = false;
    }, 220);
  }

  const btnBack = document.getElementById('btn-back');
  if (btnBack) btnBack.addEventListener('click', () => closeLetter(true));

  // Music Toggle with non-blocking toast
  let isPlayingMusic = false;
  if (musicToggle) {
    musicToggle.addEventListener('click', () => {
      const srcAttr = bgMusic ? (bgMusic.getAttribute('src') || '') : '';
      if (!srcAttr.trim()) {
        showToast("Add your music.mp3 to Assets/ to play music! 🎵");
        return;
      }
      if (isPlayingMusic) {
        bgMusic.pause();
        musicToggle.innerText = '▶';
      } else {
        bgMusic.play().catch(() => {});
        musicToggle.innerText = '⏸';
      }
      isPlayingMusic = !isPlayingMusic;
    });
  }

  // Idle prefetching of non-critical assets after initial paint
  const prefetchIdleAssets = () => {
    const assets = [
      'Assets/char_bubu_bouquet.webp',
      'Assets/char_cat_lying.webp',
      'Assets/tkthao219-bubududu.webp',
      'Assets/heart_wallpaper.webp'
    ];
    assets.forEach(src => {
      const img = new Image();
      img.src = src;
    });
  };

  if ('requestIdleCallback' in window) {
    window.requestIdleCallback(prefetchIdleAssets);
  } else {
    setTimeout(prefetchIdleAssets, 1200);
  }
});
