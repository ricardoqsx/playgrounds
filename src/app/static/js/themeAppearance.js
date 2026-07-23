(function () {
  var storageKey = "playgrounds-bg-theme";
  var themeStorageKey = "playgrounds-theme";
  var allowedThemes = [
    "base",
    "teal",
    "blue",
    "violet",
    "amber",
    "multi",
    "aqua",
    "spectrum",
    "slate",
    "copper",
    "sky",
    "purple",
    "rose",
    "lime",
    "indigo",
    "crimson",
    "ember",
    "sunset",
    "gold",
    "honey",
    "volcano",
    "coral",
  ];
  var allowedColorThemes = ["dark", "light"];

  function isAllowed(theme) {
    return allowedThemes.indexOf(theme) !== -1;
  }

  function applyTheme(theme) {
    var nextTheme = isAllowed(theme) ? theme : "base";
    if (nextTheme === "base") {
      document.documentElement.removeAttribute("data-cms-bg-theme");
    } else {
      document.documentElement.setAttribute("data-cms-bg-theme", nextTheme);
    }

    try {
      localStorage.setItem(storageKey, nextTheme);
    } catch (error) {}

    document.querySelectorAll(".cms-bg-swatch[data-cms-bg-theme]").forEach(function (button) {
      var active = button.getAttribute("data-cms-bg-theme") === nextTheme;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  function isAllowedColorTheme(theme) {
    return allowedColorThemes.indexOf(theme) !== -1;
  }

  function applyColorTheme(theme) {
    var nextTheme = isAllowedColorTheme(theme) ? theme : "dark";
    document.documentElement.setAttribute("data-theme", nextTheme);
    document.body.setAttribute("data-bs-theme", nextTheme);

    try {
      localStorage.setItem(themeStorageKey, nextTheme);
    } catch (error) {}

    document.querySelectorAll(".cms-theme-option[data-cms-theme]").forEach(function (button) {
      var active = button.getAttribute("data-cms-theme") === nextTheme;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  function getStoredColorTheme() {
    try {
      var theme = localStorage.getItem(themeStorageKey);
      return isAllowedColorTheme(theme) ? theme : "dark";
    } catch (error) {
      return "dark";
    }
  }

  function getStoredTheme() {
    try {
      var theme = localStorage.getItem(storageKey);
      return isAllowed(theme) ? theme : "base";
    } catch (error) {
      return "base";
    }
  }

  function initThemeSelector() {
    applyColorTheme(getStoredColorTheme());
    applyTheme(getStoredTheme());

    document.addEventListener("click", function (event) {
      var themeButton = event.target.closest(".cms-theme-option[data-cms-theme]");
      if (themeButton) {
        event.preventDefault();
        event.stopPropagation();
        applyColorTheme(themeButton.getAttribute("data-cms-theme"));
        return;
      }

      var button = event.target.closest(".cms-bg-swatch[data-cms-bg-theme]");
      if (!button) return;
      event.preventDefault();
      event.stopPropagation();
      applyTheme(button.getAttribute("data-cms-bg-theme"));
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initThemeSelector, { once: true });
  } else {
    initThemeSelector();
  }
})();
