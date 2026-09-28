(() => {
  "use strict";

  // Rand onder de header zodra je scrolt
  const header = document.querySelector(".header");
  const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Mobiel menu
  const btn = document.querySelector(".menu-btn");
  if (btn) {
    const close = () => { document.body.classList.remove("menu-open"); btn.setAttribute("aria-expanded", "false"); };
    btn.addEventListener("click", () => {
      const open = document.body.classList.toggle("menu-open");
      btn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });
    window.addEventListener("resize", () => { if (window.innerWidth > 900) close(); });
  }

  // Contactformulier: opent een e-mail met de ingevulde gegevens
  const form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const d = new FormData(form);
      const body = [
        `Naam: ${d.get("naam")}`,
        `Bedrijf: ${d.get("bedrijf") || "-"}`,
        `E-mail: ${d.get("email")}`,
        `Telefoon: ${d.get("telefoon") || "-"}`,
        `Aantal medewerkers: ${d.get("team") || "-"}`,
        `Interesse: ${d.get("onderwerp") || "-"}`,
        "",
        d.get("bericht"),
      ].join("\n");
      const subject = `Aanvraag kennismaking – ${d.get("bedrijf") || d.get("naam")}`;
      window.location.href = `mailto:${form.dataset.to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    });
  }
})();
