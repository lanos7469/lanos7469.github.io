const siteContent = window.SITE_CONTENT || {};
const translations = siteContent.translations || {};

document.querySelectorAll("[data-asset]").forEach((image) => {
  const source = siteContent.assets?.[image.dataset.asset];
  if (source) image.src = source;
});
document.querySelectorAll("[data-link]").forEach((link) => {
  const target = siteContent.links?.[link.dataset.link];
  if (target) link.href = target;
});

function renderProjectTasks(lang) {
  const list = document.querySelector(".work-list");
  const keys = siteContent.lists?.projectTasks || [];
  if (!list || !keys.length) return;
  list.replaceChildren(...keys.map((key) => {
    const item = document.createElement("li");
    item.textContent = (translations[lang] || translations.en)[key];
    return item;
  }));
}

function setLanguage(lang) {
  const copy = translations[lang] || translations.en;
  if (!copy) return;
  document.documentElement.lang = lang === "zh" ? "zh-CN" : lang;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const value = copy[element.dataset.i18n];
    if (value !== undefined) element.innerHTML = value;
  });
  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.lang === lang));
  });
  renderProjectTasks(lang);
  localStorage.setItem("homepage-language", lang);
}

document.querySelectorAll("[data-lang]").forEach((button) => {
  button.addEventListener("click", () => setLanguage(button.dataset.lang));
});
setLanguage(localStorage.getItem("homepage-language") || "en");

function showViewFromHash() {
  const hash = window.location.hash.slice(1);
  const view = hash === "work" || hash === "languages" ? hash : "home";
  document.querySelectorAll(".page-view").forEach((element) => {
    element.hidden = element.dataset.view !== view;
  });
  document.querySelectorAll(".main-nav a").forEach((link) => {
    if (link.getAttribute("href") === `#${view}`) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
  if (hash === "about") document.getElementById("about").scrollIntoView();
  else window.scrollTo(0, 0);
}

window.addEventListener("hashchange", showViewFromHash);
showViewFromHash();
