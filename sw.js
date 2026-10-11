const CACHE_NAME = 'open-when-v5';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './style.css',
  './script.js',
  './404.html',
  './fonts/caveat.woff2',
  './fonts/playfair-display.woff2',
  './Assets/gingham_clean.png',
  './Assets/gingham_pattern.svg',
  './Assets/flower_top_right.webp',
  './Assets/torn_paper_clean.webp',
  './Assets/heart_wallpaper.webp',
  './Assets/char_cat_shy.webp',
  './Assets/char_bubu_bouquet.webp',
  './Assets/char_cat_lying.webp',
  './Assets/tkthao219-bubududu.webp',
  './Assets/bubu-kisses-dudu-bubu-dudu.webp',
  './Assets/char_pack1_2.webp',
  './Assets/bubu-dudu.webp',
  './Assets/bubu-dudu (1).webp',
  './Assets/photo_love.webp',
  './Assets/favicon.png',
  './Assets/og_preview.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      }).catch(() => {
        if (event.request.mode === 'navigate') {
          return caches.match('./index.html');
        }
      });
    })
  );
});
