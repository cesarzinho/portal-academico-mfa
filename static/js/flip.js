function flipAndGo(url) {
  const card = document.querySelector(".card");
  if (!card) return (window.location.href = url);

  card.classList.add("flip-out");

  setTimeout(() => {
    window.location.href = url;
  }, 320);
}

function attachFlipHandlers() {
    if (!document.body.classList.contains("flip-enabled")) return;
    document.querySelectorAll("a.flip-link").forEach(a => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      flipAndGo(a.getAttribute("href"));
    });
  });

  document.querySelectorAll("form.flip-form").forEach(form => {
    form.addEventListener("submit", (e) => {
      if (!form.checkValidity()) return;

      e.preventDefault();
      const card = document.querySelector(".card");
      if (!card) return form.submit();

      card.classList.add("flip-out");
      setTimeout(() => form.submit(), 320);
    });
  });

  const card = document.querySelector(".card");
  if (card) {
    card.classList.add("flip-in");
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        card.classList.add("flip-ready");
        card.classList.remove("flip-in");
      });
    });
  }
}

document.addEventListener("DOMContentLoaded", attachFlipHandlers);
