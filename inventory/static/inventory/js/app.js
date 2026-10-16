(() => {
  const body = document.body;
  const openButton = document.querySelector(".menu-toggle");
  const closeButton = document.querySelector(".menu-close");

  const closeMenu = () => {
    body.classList.remove("menu-open");
    openButton?.setAttribute("aria-expanded", "false");
  };

  openButton?.addEventListener("click", () => {
    const isOpen = body.classList.toggle("menu-open");
    openButton.setAttribute("aria-expanded", String(isOpen));
  });
  closeButton?.addEventListener("click", closeMenu);
  document.querySelector("[data-menu-close]")?.addEventListener("click", closeMenu);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });

  document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!window.confirm(form.dataset.confirm)) event.preventDefault();
    });
  });
})();
