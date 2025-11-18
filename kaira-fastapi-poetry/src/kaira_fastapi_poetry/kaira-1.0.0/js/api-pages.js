(function() {
  const STORAGE_KEY = "kaira.api.portal";
  const DEFAULT_BASE = "http://localhost"; // nginx/uvicorn served on port 80

  let state = loadState();
  const authListeners = new Set();

  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return { baseUrl: DEFAULT_BASE };
      const parsed = JSON.parse(raw);
      return {
        baseUrl: parsed.baseUrl || DEFAULT_BASE,
        accessToken: parsed.accessToken || "",
        refreshToken: parsed.refreshToken || "",
        profile: parsed.profile || null,
      };
    } catch (err) {
      return { baseUrl: DEFAULT_BASE };
    }
  }

  function persist(partial = {}) {
    state = { ...state, ...partial };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    emitAuthChange();
  }

  function emitAuthChange() {
    authListeners.forEach((cb) => {
      try { cb({ ...state }); } catch (err) { /* ignore */ }
    });
    window.dispatchEvent(new CustomEvent("kaira:auth-change", { detail: { ...state } }));
  }

  function onAuthChange(callback) {
    if (typeof callback !== "function") return () => {};
    authListeners.add(callback);
    callback({ ...state });
    return () => authListeners.delete(callback);
  }

  function getBaseUrl() {
    return state.baseUrl || DEFAULT_BASE;
  }

  function setBaseUrl(url) {
    const sanitized = url && url.trim().length ? url.trim() : DEFAULT_BASE;
    persist({ baseUrl: sanitized });
    document.querySelectorAll("[data-base-input]").forEach((input) => {
      if (document.activeElement !== input) {
        input.value = sanitized;
      }
    });
  }

  function bindBaseInputs(selector = "#base-url") {
    document.querySelectorAll(selector).forEach((input) => {
      input.setAttribute("data-base-input", "true");
      input.value = getBaseUrl();
      input.addEventListener("change", (event) => {
        setBaseUrl(event.target.value);
      });
    });
  }

  function buildUrl(baseUrl, path, query = {}) {
    const url = new URL(path, baseUrl);
    Object.entries(query).forEach(([key, value]) => {
      if (value !== undefined && value !== null && String(value).length > 0) {
        url.searchParams.set(key, value);
      }
    });
    return url;
  }

  function getAccessToken() {
    return state.accessToken || "";
  }

  function getRefreshToken() {
    return state.refreshToken || "";
  }

  function clearSession() {
    persist({ accessToken: "", refreshToken: "", profile: null });
  }

  function setTokens({ access_token, refresh_token }) {
    persist({ accessToken: access_token || "", refreshToken: refresh_token || "" });
  }

  function setProfile(profile) {
    persist({ profile: profile || null });
  }

  async function fetchProfile() {
    if (!getAccessToken()) {
      setProfile(null);
      return null;
    }
    try {
      const profile = await callApi({ method: "GET", path: "/api/users/me" });
      setProfile(profile);
      return profile;
    } catch (err) {
      if (err.payload && err.payload.detail) {
        clearSession();
      }
      throw err;
    }
  }

  async function callApi(options) {
    const {
      method = "GET",
      path,
      query = {},
      body = null,
      headers = {},
      bodyType = "json",
      tokenOverride,
      withAuth = true,
      baseUrl: explicitBase,
    } = options;

    const baseUrl = explicitBase || getBaseUrl();
    const token = tokenOverride !== undefined ? tokenOverride : (withAuth ? getAccessToken() : "");
    const url = buildUrl(baseUrl, path, query);

    const fetchOptions = {
      method,
      headers: {
        Accept: "application/json",
        ...headers,
      },
    };

    if (token) {
      fetchOptions.headers["Authorization"] = `Bearer ${token}`;
    }

    if (body && method !== "GET") {
      if (bodyType === "form") {
        fetchOptions.headers["Content-Type"] = "application/x-www-form-urlencoded";
        fetchOptions.body = new URLSearchParams(body).toString();
      } else if (bodyType === "text") {
        fetchOptions.headers["Content-Type"] = "text/plain";
        fetchOptions.body = body;
      } else if (body instanceof FormData) {
        fetchOptions.body = body;
      } else {
        fetchOptions.headers["Content-Type"] = "application/json";
        fetchOptions.body = JSON.stringify(body);
      }
    }

    const response = await fetch(url.toString(), fetchOptions);
    const text = await response.text();
    let payload;
    try {
      payload = text ? JSON.parse(text) : {};
    } catch (err) {
      payload = text || { error: "Invalid JSON response" };
    }

    if (!response.ok) {
      const error = new Error(`HTTP ${response.status}`);
      error.payload = payload || { error: response.statusText };
      throw error;
    }

    return payload;
  }

  function renderJson(target, payload) {
    const el = typeof target === "string" ? document.getElementById(target) : target;
    if (!el) return;
    if (payload === undefined) {
      el.textContent = "";
      return;
    }
    if (typeof payload === "string") {
      el.textContent = payload;
    } else {
      el.textContent = JSON.stringify(payload, null, 2);
    }
  }

  function attachForm(formId, handler, options = {}) {
    const form = document.getElementById(formId);
    if (!form) return;
    const resultTarget = options.resultTarget || form.dataset.resultTarget;
    const requireAuth = options.requireAuth || form.dataset.requireAuth === "true";
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (requireAuth && !getAccessToken()) {
        if (resultTarget) {
          renderJson(resultTarget, { error: "로그인이 필요합니다." });
        }
        return;
      }
      if (resultTarget) {
        renderJson(resultTarget, "Loading...");
      }
      try {
        const data = await handler(form);
        if (resultTarget) {
          renderJson(resultTarget, data);
        }
      } catch (err) {
        const payload = err.payload || { error: err.message };
        if (resultTarget) {
          renderJson(resultTarget, payload);
        }
      }
    });
  }

  function populateLinks() {
    const base = getBaseUrl();
    document.querySelectorAll("[data-base-aware-link='true']").forEach((el) => {
      if (!base) return;
      const path = el.getAttribute("data-path");
      if (path) {
        el.textContent = new URL(path, base);
      }
    });
  }

  window.apiHelpers = {
    attachForm,
    bindBaseInputs,
    callApi,
    clearSession,
    fetchProfile,
    getAccessToken,
    getBaseUrl,
    getRefreshToken,
    onAuthChange,
    populateLinks,
    renderJson,
    setBaseUrl,
    setProfile,
    setTokens,
  };
})();
