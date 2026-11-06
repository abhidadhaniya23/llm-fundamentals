// Shared helpers for the benchmarking demos.
// Demo.sync(id, state, render): keeps one state object in step between the trainer and student
// windows (both embed the same iframe, same origin) over a BroadcastChannel. Call set({...}) to change it.
window.Demo = {
  sync(id, state, render) {
    const ch = (() => { try { return new BroadcastChannel('bench-demo-' + id); } catch (e) { return null; } })();
    const set = (patch, quiet) => {
      Object.assign(state, patch);
      render(state);
      if (ch && !quiet) ch.postMessage({ type: 'state', state });
    };
    if (ch) {
      ch.onmessage = e => {
        if (e.data.type === 'state') set(e.data.state, true);
        if (e.data.type === 'hello') ch.postMessage({ type: 'state', state });
      };
      ch.postMessage({ type: 'hello' });
    }
    render(state);
    return set;
  },
  param(name, fallback) { return new URLSearchParams(location.search).get(name) || fallback; },
  esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); },
  label() { const d = document.createElement('div'); d.className = 'synthetic'; d.textContent = 'Fictional Contoso data'; document.body.appendChild(d); },
};
