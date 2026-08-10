/* 我的小工具（入口页） - Service Worker */
const CACHE = 'tools-launcher-v1';
/* 缓存是按「域名」共享的，不是按目录隔离的：清理旧缓存时只能删自己这个前缀的，
   否则会把各个子应用的缓存一起删掉，害它们离线打不开。 */
const PREFIX = 'tools-launcher-';
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

  // 入口页的 scope 是仓库根目录，会「盖住」子应用目录。这里只接管根目录自身的文件，
  // 子应用（qiuzhilu / jizhangji …）一律放行，交给它们各自的 sw.js 处理，避免两层缓存打架。
  const scope = new URL('./', self.location).pathname;
  if (!url.pathname.startsWith(scope)) return;
  const rel = url.pathname.slice(scope.length);
  const isOwn = rel === '' || !rel.includes('/') || rel.startsWith('icons/');
  if (!isOwn) return;

  // 入口页（HTML）走 network-first：加了新应用刷新即可见，断网时回退缓存。
  // 必须用 cache:'reload' 绕开浏览器自身的 HTTP 缓存（GitHub Pages 的 HTML 是 max-age=600）。
  const isHTML = req.mode === 'navigate' || req.destination === 'document' ||
                 url.pathname.endsWith('.html') || url.pathname.endsWith('/');
  if (isHTML) {
    e.respondWith(
      fetch(req.url, { cache: 'reload', credentials: 'same-origin' }).then((res) => put(req, res))
        .catch(() => caches.match(req).then((c) => c || caches.match('./index.html')))
    );
    return;
  }

  // 图标 / manifest 走 stale-while-revalidate。
  e.respondWith(
    caches.match(req).then((cached) => {
      const network = fetch(req).then((res) => put(req, res)).catch(() => cached);
      return cached || network;
    })
  );
});
