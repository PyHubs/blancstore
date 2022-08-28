let staticSite = "blancstore"
let assets = [
  "/",
  "/index.html",
  "/assets",
  "/books",
  "/executable",
  "/sites",
  "about.html",
  "blogs.html",
  "logo.png",
  "style.css"
]

self.addEventListener("install", installEvent => {
  installEvent.waitUntil(
    caches.open(staticSite).then(cache => {
      cache.addAll(assets)
    })
  )
})
