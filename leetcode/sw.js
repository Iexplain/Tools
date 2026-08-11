/* LeetTrack - Service Worker */
const CACHE = 'leetrack-v1';
/* 缓存是按「域名」共享的，不是按目录隔离的：清理旧缓存时只能删自己这个前缀的，
   否则会把同仓库其他应用（求职录、记账本、入口页）的缓存一起删掉。 */
const PREFIX = 'leetrack-';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './data/questions.js',
  './icons/icon-180.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-512-maskable.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k.startsWith(PREFIX) && k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

function put(req, res) {
  if (res && res.status === 200 && res.type === 'basic') {
    const clone = res.clone();
    caches.open(CACHE).then((c) => c.put(req, clone));
  }
  return res;
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // HTML 走 network-first：联网拿最新版，断网回退缓存（cache:'reload' 绕开浏览器 HTTP 缓存）
  const isHTML = req.mode === 'navigate' || req.destination === 'document' ||
                 url.pathname.endsWith('.html') || url.pathname.endsWith('/');
  if (isHTML) {
    e.respondWith(
      fetch(req.url, { cache: 'reload', credentials: 'same-origin' }).then((res) => put(req, res))
        .catch(() => caches.match(req).then((c) => c || caches.match('./index.html')))
    );
    return;
  }

  // 静态资源 stale-while-revalidate
  e.respondWith(
    caches.match(req).then((cached) => {
      const network = fetch(req).then((res) => put(req, res)).catch(() => cached);
      return cached || network;
    })
  );
});
