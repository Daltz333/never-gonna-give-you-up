var json = require('cache.json');
var jsonPaths = JSON.parse(json)

// extend this to update the service worker every push
// https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Offline_Service_workers
var cacheName = 'js13kPWA-v1';

self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open('frc-docs').then(function(cache) {
            return cache.addAll(jsonPaths);
        })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
        })
    );
});