/* 记账本 - Service Worker */
const CACHE = 'account-book-v23';
/* 缓存是按「域名」共享的，不是按目录隔离的：清理旧缓存时只能删自己这个前缀的，
   否则会把同仓库其他应用（求职录、入口页）的缓存一起删掉，害它们离线打不开。 */
const PREFIX = 'account-book-';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
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

/* 把响应存回缓存（只存正常的同源响应） */
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

  // 应用本体（HTML）走 network-first：联网时永远拿到最新版，改完文件刷新即生效；
  // 断网时回退到缓存，离线照常可用。
  // 注意必须用 cache:'reload' 绕开浏览器自身的 HTTP 缓存 —— GitHub Pages 给 HTML 发的是
  // max-age=600，直接 fetch(req) 会命中 HTTP 缓存，导致更新最多延迟 10 分钟才可见。
  const isHTML = req.mode === 'navigate' || req.destination === 'document' ||
                 url.pathname.endsWith('.html') || url.pathname.endsWith('/');
  if (isHTML) {
    e.respondWith(
      fetch(req.url, { cache: 'reload', credentials: 'same-origin' }).then((res) => put(req, res))
        .catch(() => caches.match(req).then((c) => c || caches.match('./index.html')))
    );
    return;
  }

  // 图标 / manifest 等静态资源走 stale-while-revalidate：
  // 立刻用缓存渲染，同时后台悄悄更新，下次打开就是新的。
  e.respondWith(
    caches.match(req).then((cached) => {
      const network = fetch(req).then((res) => put(req, res)).catch(() => cached);
      return cached || network;
    })
  );
});
