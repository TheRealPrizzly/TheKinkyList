"""Installable web app: manifest, service worker and offline page.

The service worker lives at the site root so it can control every page. It only caches the
offline page and its static files: lists and to-dos are private, so pages are never stored
on the device.
"""

import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

# Bump when the offline page or its files change, so phones fetch the new copies.
CACHE_VERSION = "v1"

BACKGROUND = "#16050f"  # --bg
THEME = "#3b0a24"  # --wine


@require_GET
@cache_control(max_age=60 * 60 * 24)
def manifest(request):
    data = {
        "id": "/",
        "name": "The Kinky List",
        "short_name": "Kinky List",
        "description": "A romantic, gamified bucket list for couples.",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": BACKGROUND,
        "theme_color": THEME,
        "categories": ["lifestyle", "entertainment"],
        "icons": [
            {"src": static("icons/icon-192.png"), "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": static("icons/icon-512.png"), "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": static("icons/maskable-512.png"), "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    return JsonResponse(data, content_type="application/manifest+json")


@require_GET
@cache_control(no_cache=True)
def service_worker(request):
    offline_files = [
        "/offline/",
        static("css/app.css"),
        static("icons/icon-192.png"),
    ]
    script = SERVICE_WORKER.replace("__CACHE__", f"kinkylist-{CACHE_VERSION}").replace(
        "__FILES__", json.dumps(offline_files)
    )
    return HttpResponse(script, content_type="application/javascript")


@require_GET
def offline(request):
    return render(request, "offline.html")


SERVICE_WORKER = """
const CACHE = "__CACHE__";
const OFFLINE_FILES = __FILES__;

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(OFFLINE_FILES)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key))))
  );
  self.clients.claim();
});

// Pages always come from the network; the cached offline page only stands in when there is none.
self.addEventListener("fetch", (event) => {
  if (event.request.mode === "navigate") {
    event.respondWith(fetch(event.request).catch(() => caches.match("/offline/")));
  } else if (OFFLINE_FILES.includes(new URL(event.request.url).pathname)) {
    event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
  }
});
"""
