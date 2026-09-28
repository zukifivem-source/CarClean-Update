(() => {
  "use strict";
  document.documentElement.classList.add("js");

  const header = document.querySelector(".header");
  const scrub = document.querySelector(".scrub");
  const stage = document.querySelector(".stage");
  const chapters = [...document.querySelectorAll(".chapter")];
  const dots = [...document.querySelectorAll(".progress a")];
  const progressNav = document.querySelector(".progress");
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Header achtergrond na scrollen
  const onHeader = () => header.classList.toggle("scrolled", window.scrollY > 24);
  onHeader();
  window.addEventListener("scroll", onHeader, { passive: true });

  // Hoofdstukken: zichtbaar maken + actieve stip
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      e.target.classList.add("in");
      const i = chapters.indexOf(e.target);
      dots.forEach((d, j) => d.classList.toggle("active", j === i));
      stage?.classList.toggle("side-right", e.target.classList.contains("right"));
    }
  }, { threshold: 0.45 });
  chapters.forEach((c) => io.observe(c));

  // Voortgangsstippen alleen tonen binnen de film
  if (progressNav && scrub) {
    new IntersectionObserver(([e]) => progressNav.classList.toggle("hidden", !e.isIntersecting), { threshold: 0.02 }).observe(scrub);
  }

  // Scroll-gestuurde film
  if (!scrub || !stage || reduced) return;

  const isMobile = () => window.matchMedia("(max-width: 820px), (pointer: coarse)").matches;
  const video = document.createElement("video");
  video.muted = true;
  video.playsInline = true;
  video.setAttribute("playsinline", "");
  video.setAttribute("muted", "");
  video.preload = "auto";
  video.setAttribute("aria-hidden", "true");
  video.tabIndex = -1;
  stage.appendChild(video);

  let blobUrl = null;
  let currentSrc = null;
  let controller = null;
  let target = 0;
  let raf = 0;
  let lastWidth = window.innerWidth;

  const load = async () => {
    const src = isMobile() ? stage.dataset.srcMobile : stage.dataset.src;
    if (src === currentSrc) return;
    currentSrc = src;
    controller?.abort();
    controller = new AbortController();
    try {
      const res = await fetch(src, { signal: controller.signal });
      if (!res.ok) throw new Error(res.status);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      if (blobUrl) URL.revokeObjectURL(blobUrl);
      blobUrl = url;
      stage.classList.remove("ready");
      video.src = url;
      video.addEventListener("loadeddata", () => {
        seek();
        video.addEventListener("seeked", () => stage.classList.add("ready"), { once: true });
      }, { once: true });
    } catch (err) {
      if (err.name === "AbortError") return;
      // Fallback (bv. lokaal geopend via file://): bron direct op de video zetten
      video.src = src;
      video.addEventListener("loadeddata", () => {
        seek();
        video.addEventListener("seeked", () => stage.classList.add("ready"), { once: true });
      }, { once: true });
      video.addEventListener("error", () => { currentSrc = null; }, { once: true }); // poster blijft staan
    }
  };

  const progress = () => {
    const rect = scrub.getBoundingClientRect();
    const span = rect.height - window.innerHeight;
    return span > 0 ? Math.min(1, Math.max(0, -rect.top / span)) : 0;
  };

  const seek = () => {
    if (!video.duration || video.seeking) return;
    const t = target * (video.duration - 0.05);
    if (Math.abs(video.currentTime - t) > 0.01) video.currentTime = t;
  };

  const tick = () => {
    raf = 0;
    target = progress();
    seek();
  };
  const onScroll = () => { if (!raf) raf = requestAnimationFrame(tick); };
  video.addEventListener("seeked", () => { if (Math.abs(video.currentTime - target * (video.duration - 0.05)) > 0.04) onScroll(); });

  // iOS: video eenmalig "ontgrendelen" bij eerste aanraking
  const prime = () => {
    const p = video.play();
    if (p) p.then(() => { video.pause(); seek(); }).catch(() => {});
  };
  window.addEventListener("touchstart", prime, { once: true, passive: true });
  window.addEventListener("pointerdown", prime, { once: true, passive: true });

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", () => {
    if (window.innerWidth === lastWidth) return; // negeer adresbalk-hoogte op mobiel
    lastWidth = window.innerWidth;
    load();
    onScroll();
  });

  // Pas laden als de pagina klaar is, zodat eerste weergave snel blijft
  if (document.readyState === "complete") load();
  else window.addEventListener("load", load, { once: true });

  window.addEventListener("pagehide", () => {
    controller?.abort();
    cancelAnimationFrame(raf);
    if (blobUrl) URL.revokeObjectURL(blobUrl);
  });
})();

// Contactformulier: opent een e-mail met de ingevulde gegevens
(() => {
  const form = document.getElementById("contact-form");
  if (!form) return;
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const d = new FormData(form);
    const body = [
      `Naam: ${d.get("naam")}`,
      `Bedrijf: ${d.get("bedrijf") || "-"}`,
      `E-mail: ${d.get("email")}`,
      `Telefoon: ${d.get("telefoon") || "-"}`,
      `Teamgrootte: ${d.get("team") || "-"}`,
      "",
      d.get("bericht"),
    ].join("\n");
    const to = form.dataset.to;
    window.location.href = `mailto:${to}?subject=${encodeURIComponent("Aanvraag gratis procesScan – " + (d.get("bedrijf") || d.get("naam")))}&body=${encodeURIComponent(body)}`;
  });
})();
