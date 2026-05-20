const CACHE = 'maestro-arrocero-v1';

const PRECACHE = [
  '/',
  '/index.html',
  '/brasas.html',
  '/manifest.json',
  '/img/icon-192.png',
  '/img/icon-512.png',
  '/img/alhorno.jpg',
  '/img/caldoso.jpg',
  '/img/carabineros.jpg',
  '/img/carrilleras.jpg',
  '/img/chuleton.jpg',
  '/img/fideua.jpg',
  '/img/marisco.jpg',
  '/img/negro.jpg',
  '/img/valenciana.jpg',
  '/img/vegetal.jpg',
  '/img/brasas/parrillada.jpg',
  '/img/brasas/ribeye.jpg',
  '/img/brasas/pollo-humo.jpg',
  '/img/brasas/picanha.jpg',
  '/img/brasas/costillas-bbq.jpg',
  '/img/brasas/secreto-iberico.jpg',
  '/img/brasas/cordero-brasas.jpg',
  '/img/brasas/alitas-ahumadas.jpg',
  '/img/brasas/entrecot-lena.jpg',
  '/img/brasas/pinchos-morunos.jpg',
  '/img/brasas/churrasco.jpg',
  '/img/brasas/cat-vacuno.jpg',
  '/img/brasas/cat-cerdo.jpg',
  '/img/brasas/cat-aves.jpg',
  '/img/brasas/cat-cordero.jpg',
  '/img/brasas/cat-alinos.jpg',
  '/img/brasas/cat-lena.jpg',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        if (!res || res.status !== 200 || res.type === 'opaque') return res;
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      }).catch(() => {
        if (e.request.destination === 'document') return caches.match('/index.html');
      });
    })
  );
});
