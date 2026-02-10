const API = "http://localhost:8000/v1";

async function postJson(path, data, includeCreds = true) {
  const res = await fetch(`${API}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
    credentials: includeCreds ? "include" : "same-origin"
  });
  const text = await res.text();
  try { return { ok: res.ok, status: res.status, body: JSON.parse(text) }; }
  catch { return { ok: res.ok, status: res.status, body: text }; }
}

document.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (e.target.id === "registerForm") {
    const f = Object.fromEntries(new FormData(e.target));
    const r = await postJson("/register", f, false);
    document.getElementById("regOutput").textContent = JSON.stringify(r, null, 2);
  }
  if (e.target.id === "loginForm") {
    const f = Object.fromEntries(new FormData(e.target));
    const r = await postJson("/login", f, true);
    document.getElementById("loginOutput").textContent = JSON.stringify(r, null, 2);
    
    if (r.ok) {
      window.location.href = "Home.html";
    }
  }
});

document.getElementById?.("postBtn")?.addEventListener("click", async () => {
  const q = document.getElementById("query").value || '{"query":"test"}';
  let parsed;
  try { parsed = JSON.parse(q); } catch { parsed = { query: q }; }
  const res = await postJson("/post", parsed, true);
  document.getElementById("output").textContent = JSON.stringify(res, null, 2);
});

document.getElementById?.("logoutBtn")?.addEventListener("click", async () => {
  const res = await postJson("/logout", {}, true);
  document.getElementById("output").textContent = JSON.stringify(res, null, 2);
});
