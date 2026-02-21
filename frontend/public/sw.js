const CACHE_NAME = "alkhayma-v1";
const STATIC_ASSETS = ["/", "/index.html", "/manifest.json"];

// Install event
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    }),
  );
  self.skipWaiting();
});

// Activate event
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        }),
      );
    }),
  );
  self.clients.claim();
});

// Fetch event
self.addEventListener("fetch", (event) => {
  // Skip non-GET requests
  if (event.request.method !== "GET") {
    return;
  }

  // Skip API calls - always fetch fresh
  if (event.request.url.includes("/api")) {
    event.respondWith(
      fetch(event.request)
        .then((response) => response)
        .catch(() => {
          // Return offline page or error response
          return new Response(JSON.stringify({ error: "Network error" }), {
            status: 503,
            headers: { "Content-Type": "application/json" },
          });
        }),
    );
    return;
  }

  // Cache first strategy for static assets
  event.respondWith(
    caches.match(event.request).then((response) => {
      return (
        response ||
        fetch(event.request)
          .then((response) => {
            // Clone the response
            const clonedResponse = response.clone();

            // Cache the response
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, clonedResponse);
            });

            return response;
          })
          .catch(() => {
            // Return cached version or offline page
            return caches.match(event.request);
          })
      );
    }),
  );
});

// Message event for cache busting
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});
