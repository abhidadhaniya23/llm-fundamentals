// Student deck viewer, static edition: opens from file:// with no server.
// Built by final/build_student.py. The flow and topic Markdown are embedded in the page (window.DECK),
// trainer notes were removed at build time, and reveals open when the student clicks them (or presses R).
// Parsing and rendering helpers are copied in from viewer.js by the build, between the SHARED markers.

const DECK = window.DECK;
const FLOW = document.body.dataset.flow;
const ROOT = `content/${FLOW}/`;
const STORE = `deck-student-${FLOW}`;
const STUDENTS = false; // the shared code's "trainer" path renders every kept fence; trainer fences no longer exist
const TOPIC_CSS = slug => `viewer/topics/${slug}.css`;

let flow = DECK.flow;     // [{ title, file }]
let sections = [];
let state = load() || { file: null, section: 0, revealed: {} };
const svgCache = new Map();

const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const slug = s => String(s).toLowerCase().replace(/[`*_]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const topicSlug = file => (file || '').replace(/^.*\//, '').replace(/\.md$/, '');

function load() { try { return JSON.parse(localStorage.getItem(STORE)); } catch (e) { return null; } }
function save() { try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) {} }

// ---------- topic: split into sections at # and ##, carrying ::: fences across ----------

const FENCE_OPEN = /^:::\s*(trainer|reveal)\b\s*(.*)$/;
const FENCE_CLOSE = /^:::\s*$/;

// Tracks ``` / ~~~ code blocks. A block closes only on a fence of the same character that is at least as long,
// so a file shown in a ```` block can contain ``` lines of its own. Returns the open fence, or false.
function codeFence(line, open) {
  const m = line.match(/^\s*(`{3,}|~{3,})\s*(\S*)/);
  if (!m) return open;
  if (!open) return m[1];
  return (m[1][0] === open[0] && m[1].length >= open.length && !m[2]) ? false : open;
}

// Fences may be left open. One closes itself at the next ::: fence, at a --- line, at the end of the
// file, or at the next # / ## heading (unless it was opened right above that heading, which it then wraps).
// The result has an explicit ::: for every fence, and stray ::: lines are dropped.
function normalizeFences(text) {
  const out = [];
  let inCode = false, open = false, wrapsNextHeading = false;
  const close = () => { if (open) out.push(':::'); open = false; wrapsNextHeading = false; };
  for (const line of text.replace(/\r/g, '').split('\n')) {
    inCode = codeFence(line, inCode);
    if (!inCode) {
      if (FENCE_OPEN.test(line)) { close(); out.push(line); open = true; wrapsNextHeading = true; continue; }
      if (FENCE_CLOSE.test(line)) { close(); continue; }
      if (/^#{1,2}\s/.test(line)) { if (open && !wrapsNextHeading) close(); wrapsNextHeading = false; }
      else if (/^(-{3,}|\*{3,}|_{3,})\s*$/.test(line)) close();
      else if (line.trim() !== '') wrapsNextHeading = false;
    }
    out.push(line);
  }
  close();
  return out.join('\n');
}

function parseTopic(text) {
  text = normalizeFences(text);
  const out = [];
  const seen = {};
  let cur = null, inCode = false, fence = null;
  const start = (level, title, headingInFence) => {
    if (cur && fence) {
      // A fence opened right before this heading belongs to the new section only.
      let j = cur.lines.length - 1;
      while (j >= 0 && cur.lines[j].trim() === '') j--;
      if (j >= 0 && cur.lines[j] === fence.line) cur.lines.splice(j); else cur.lines.push(':::');
    }
    const n = (seen[title] = (seen[title] || 0) + 1);
    cur = { level, title, key: `${title}#${n}`, lines: [], headingInFence };
    out.push(cur);
    if (fence) cur.lines.push(fence.line);
  };
  for (const line of text.replace(/\r/g, '').split('\n')) {
    inCode = codeFence(line, inCode);
    if (!inCode) {
      const h = line.match(/^(#{1,2})\s+(.*?)\s*#*\s*$/);
      if (h) { start(h[1].length, h[2], !!fence && fence.type === 'trainer'); cur.lines.push(line); continue; }
      const o = line.match(FENCE_OPEN);
      if (o) fence = { type: o[1], line };
      else if (FENCE_CLOSE.test(line)) fence = null;
    }
    if (!cur) start(0, 'Intro', false);
    cur.lines.push(line);
  }
  if (cur && fence) cur.lines.push(':::');
  for (const s of out) {
    s.reveals = s.lines.filter(l => /^:::\s*reveal\b/.test(l)).length;
    s.hasStudent = !s.headingInFence;
  }
  return out.filter(s => s.lines.join('').trim() !== '');
}

// Turn a section's lines into Markdown for one audience.
function sectionMarkdown(sec, mode, revealedSet) {
  const out = [];
  let inCode = false, fence = null, revealIdx = -1;
  for (const line of sec.lines) {
    inCode = codeFence(line, inCode);
    if (!inCode) {
      const o = line.match(FENCE_OPEN);
      if (o) {
        const type = o[1];
        const [label, target] = o[2].split(' | ').map(x => (x || '').trim());
        if (type === 'reveal') revealIdx++;
        const shown = type === 'reveal' && revealedSet.has(revealIdx);
        fence = { type, keep: mode === 'trainer' || shown };
        if (fence.keep) {
          const tag = type === 'trainer'
            ? `Trainer only${label ? ' · ' + esc(label) : ''}`
            : `${label ? esc(label) + ' · ' : ''}${shown ? 'shown to students' : 'hidden from students · R to reveal'}`;
          const cls = type === 'reveal' ? `fence reveal ${shown ? 'shown' : 'hidden'}` : 'fence trainer';
          out.push('', `<div class="${cls}" data-i="${type === 'reveal' ? revealIdx : ''}"${target ? ` data-target="${esc(target)}"` : ''}><div class="fence-tag">${tag}</div>`, '');
        }
        continue;
      }
      if (fence && FENCE_CLOSE.test(line)) {
        if (fence.keep) out.push('', '</div>', '');
        fence = null;
        continue;
      }
    }
    if (!fence || fence.keep) out.push(line);
  }
  return out.join('\n');
}

function sectionId(sec) { return `${state.file}::${sec.key}`; }
function revealedFor(sec) { return new Set(state.revealed[sectionId(sec)] || []); }

// ---------- enhancement: plain Markdown in, styled components out ----------

function enhance(root) {
  root.querySelectorAll('blockquote').forEach(b => b.classList.add('story'));

  root.querySelectorAll('p').forEach(p => {
    const first = p.firstElementChild;
    if (!first || first.tagName !== 'STRONG' || p.firstChild !== first) return;
    const lead = first.textContent.replace(/:$/, '').trim();
    p.dataset.lead = slug(lead);
    if (/^task\b/i.test(lead)) p.classList.add('task');
    // "**Label:** a, b, c" → chips
    const rest = p.textContent.slice(first.textContent.length).trim();
    const items = rest.split(',').map(s => s.trim()).filter(Boolean);
    if (items.length >= 3 && items.every(s => s.length < 30) && !/[.!?]$/.test(rest)) {
      p.classList.add('chips');
      p.innerHTML = `${first.outerHTML} ` + items.map(s => `<span class="chip">${esc(s)}</span>`).join('');
    }
  });

  root.querySelectorAll('h2, h3').forEach(h => {
    h.dataset.slug = slug(h.textContent);
    if (/^task\b/i.test(h.textContent)) h.classList.add('task-h');
  });

  root.querySelectorAll('table').forEach(t => {
    const heads = [...t.querySelectorAll('thead th')].map(th => th.textContent.trim());
    heads.forEach((h, i) => {
      const col = slug(h) || `c${i}`;
      t.querySelectorAll(`tr > :nth-child(${i + 1})`).forEach(c => {
        c.dataset.col = col;
        const txt = c.textContent.trim();
        if (txt.length && txt.length <= 40) c.dataset.text = slug(txt);
        if (/✅/.test(h)) c.classList.add('good');
        if (/❌/.test(h)) c.classList.add('bad');
      });
    });
    if (!t.parentElement.classList.contains('tbl')) {
      const w = document.createElement('div'); w.className = 'tbl'; t.replaceWith(w); w.appendChild(t);
    }
  });

  root.querySelectorAll(':not(pre) > code').forEach(c => {
    const m = c.textContent.match(/^([1-5])\d\d\b/);
    if (m) c.classList.add('sc', 'sc' + m[1]);
  });

  root.querySelectorAll('pre > code.language-http').forEach(highlightHttp);
  root.querySelectorAll('pre > code.language-python').forEach(c => { c.innerHTML = hlPython(c.textContent); });
  root.querySelectorAll('pre > code.language-diff').forEach(c => { c.innerHTML = hlDiff(c.textContent); });
  root.querySelectorAll('pre > code[class*="language-output"]').forEach(c => { c.innerHTML = hlPytest(c.textContent); c.parentElement.classList.add('output', /fail/.test(c.className) ? 'fail' : 'pass'); });

  // A shown reveal with a target (::: reveal Label | #pyr .l-unit) lights up that part of the diagram.
  root.querySelectorAll('.fence.reveal.shown[data-target]').forEach(f => {
    try { root.querySelectorAll(f.dataset.target).forEach(el => el.classList.add('on')); } catch (e) { console.warn('Bad reveal target', f.dataset.target); }
  });

  root.querySelectorAll('pre > code.language-mermaid').forEach(c => {
    const box = document.createElement('div');
    box.className = 'diagram';
    const src = c.textContent;
    box.dataset.src = src;
    if (svgCache.has(src)) box.innerHTML = svgCache.get(src);
    c.parentElement.replaceWith(box);
    if (!svgCache.has(src)) renderMermaid(box, src);
  });

  if (!STUDENTS) root.querySelectorAll('.fence.reveal').forEach(f => f.addEventListener('click', () => toggleReveal(+f.dataset.i)));
}

function highlightHttp(code) {
  let body = false;
  code.innerHTML = code.textContent.split('\n').map((line, i) => {
    if (body) return esc(line);
    if (line.trim() === '' && i > 0) { body = true; return ''; }
    let m;
    if ((m = line.match(/^(HTTP\/[\d.]+)\s+(\d{3})(.*)$/)))
      return `<span class="h-ver">${esc(m[1])}</span> <span class="sc sc${m[2][0]}">${m[2]}${esc(m[3])}</span>`;
    if ((m = line.match(/^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(\S+)(.*)$/)))
      return `<span class="h-method m-${m[1].toLowerCase()}">${m[1]}</span> <span class="h-path">${esc(m[2])}</span>${esc(m[3])}`;
    if ((m = line.match(/^([A-Za-z][\w-]*):(.*)$/)))
      return `<span class="h-key">${esc(m[1])}:</span>${esc(m[2])}`;
    return esc(line);
  }).join('\n');
}

// Small highlighters for code shown in the testing flow (ported from brain/testing.js)
const PY_KW = /\b(def|class|return|if|elif|else|for|in|while|import|from|as|with|assert|raise|pass|not|and|or|is|None|True|False|lambda|yield|try|except|finally|self)\b/g;
function hlPython(src) {
  const out = [];
  const re = /("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'|#[^\n]*|@\w[\w.]*|\b\d+(?:\.\d+)?\b)/g;
  let last = 0, m;
  const plain = t => esc(t).replace(PY_KW, '<span class="kw">$1</span>').replace(/\b(def|class)<\/span> (\w+)/g, '$1</span> <span class="fn">$2</span>');
  while ((m = re.exec(src))) {
    out.push(plain(src.slice(last, m.index)));
    const t = m[0];
    const cls = t[0] === '#' ? 'cm' : t[0] === '@' ? 'dec' : /^\d/.test(t) ? 'num' : 'str';
    out.push(`<span class="${cls}">${esc(t)}</span>`);
    last = m.index + t.length;
  }
  out.push(plain(src.slice(last)));
  return out.join('');
}
function hlDiff(src) {
  return src.split('\n').map(l => {
    const c = l.startsWith('+++') || l.startsWith('---') ? 'meta' : l[0] === '+' ? 'add' : l[0] === '-' ? 'del' : l.startsWith('@@') ? 'hunk' : '';
    return c ? `<span class="${c}">${esc(l)}</span>` : esc(l);
  }).join('\n');
}
function hlPytest(src) {
  return src.split('\n').map(l => {
    const h = esc(l);
    if (/^\$ /.test(l)) return `<span class="cmd">${h}</span>`;
    if (/^E\s|^>\s/.test(l)) return `<span class="err">${h}</span>`;
    if (/^=+ .*(failed|error).* =+$/.test(l) || (/failed in|error in/.test(l) && /^\d+ /.test(l))) return `<span class="sum bad">${h}</span>`;
    if (/^=+ .*passed.* =+$/.test(l) || /^\d+ passed/.test(l)) return `<span class="sum ok">${h}</span>`;
    return h.replace(/\b(PASSED)\b/g, '<span class="ok">$1</span>').replace(/\b(FAILED|ERROR)\b/g, '<span class="bad">$1</span>').replace(/\b(SKIPPED)\b/g, '<span class="skip">$1</span>');
  }).join('\n');
}

let mermaidN = 0;
async function renderMermaid(box, src) {
  try {
    const { svg } = await mermaid.render(`mm${++mermaidN}`, src);
    svgCache.set(src, svg);
    document.querySelectorAll('.diagram').forEach(b => { if (b.dataset.src === src) b.innerHTML = svg; });
  } catch (e) {
    box.innerHTML = `<pre class="diagram-error">Diagram error: ${esc(e.message || e)}</pre>`;
  }
}



// ---------- rendering ----------

function firstSectionIndex() { return sections.findIndex(s => s.level === 1); }

function render() {
  const main = $('#slide');
  const topic = flow.find(t => t.file === state.file);
  document.body.dataset.topic = topicSlug(state.file);
  $('#topic-title').textContent = topic ? topic.title : '';
  if (!sections.length) { main.innerHTML = '<p class="empty">This topic has no content yet.</p>'; return; }
  state.section = Math.max(0, Math.min(state.section, sections.length - 1));
  const idx = state.section;
  const sec = sections[idx];
  const md = sectionMarkdown(sec, 'trainer', revealedFor(sec));

  let p = idx; while (p > 0 && sections[p].level !== 1) p--;
  main.dataset.part = sections[p] && sections[p].level === 1 ? slug(sections[p].title) : '';
  main.dataset.section = slug(sec.title);
  main.className = `slide level-${sec.level}` + (idx === firstSectionIndex() ? ' cover' : '');
  main.innerHTML = '<div class="page">' + (idx === firstSectionIndex() ? coverHtml() : '') + marked.parse(md) + '</div>';
  relabelReveals(main);
  enhance(main); // its (!STUDENTS) branch makes each reveal clickable: toggleReveal
  $('#where').textContent = `${idx + 1} / ${sections.length}`;
  renderRail();
  if (renderedKey !== sectionId(sec)) main.scrollTop = 0;
  renderedKey = sectionId(sec);
}
let renderedKey = null;

// The shared fence tags speak to the trainer ("hidden from students · R to reveal"); students get "Show".
function relabelReveals(root) {
  root.querySelectorAll('.fence.reveal').forEach(f => {
    const tag = f.querySelector('.fence-tag');
    if (!tag) return;
    const label = tag.textContent.replace(/(^|\s·\s)(shown to students|hidden from students · R to reveal)$/, '').trim();
    const shown = f.classList.contains('shown');
    tag.textContent = shown ? (label ? `${label} · hide` : 'Hide') : (label ? `Show · ${label}` : 'Show');
    f.title = shown ? 'Click to hide' : 'Click to show (R)';
  });
}

function coverHtml() {
  const n = flow.findIndex(t => t.file === state.file);
  return `<div class="cover-kicker">Topic ${n + 1} of ${flow.filter(t => t.file).length}</div>`;
}

function renderRail() {
  const list = sections.map((s, i) => {
    const badge = s.reveals ? `<span class="b r">${(state.revealed[sectionId(s)] || []).length}/${s.reveals}</span>` : '';
    return `<li class="lv${s.level}${i === state.section ? ' on' : ''}" data-i="${i}">${esc(s.title.replace(/[`*]/g, ''))}${badge}</li>`;
  }).join('');
  const next = sections[state.section + 1];
  const nextTopic = flow[flow.findIndex(t => t.file === state.file) + 1];
  $('#rail').innerHTML = `
    <div class="rail-h">This topic</div><ol class="outline">${list}</ol>
    <div class="rail-h">Next</div>
    <div class="next">${next ? esc(next.title) : nextTopic ? 'Topic: ' + esc(nextTopic.title) : 'End of the session'}</div>
    <div class="rail-h keys-h">Keys</div>
    <div class="keys"><b>→</b> next · <b>←</b> back · ${COMMANDS.filter(c => c.hint).map(c => `<b>${c.hint}</b> ${c.label.toLowerCase()}`).join(' · ')}</div>`;
  const on = $('#rail li.on');
  if (on) on.scrollIntoView({ block: 'nearest' });
}

function renderTopics() {
  $('#topics').innerHTML = '<div class="rail-h">Topics</div><ol>' + flow.map((t, i) =>
    `<li class="${t.file === state.file ? 'on' : ''}${t.file ? '' : ' off'}" data-f="${esc(t.file || '')}">${i + 1}. ${esc(t.title)}</li>`).join('') + '</ol>';
}

// ---------- loading (everything is already in the page) ----------

function loadTopic() {
  const text = DECK.files[state.file];
  sections = parseTopic(text == null ? `# Missing file\n\n\`${state.file}\` is not in this build.` : text);
  let link = document.getElementById('topic-css');
  const href = TOPIC_CSS(topicSlug(state.file));
  if (!DECK.css.includes(href)) { if (link) link.remove(); return; }
  if (!link) { link = document.createElement('link'); link.rel = 'stylesheet'; link.id = 'topic-css'; document.head.appendChild(link); }
  link.href = href;
}

// ---------- navigation and reveals ----------

function go(file, section) {
  const changed = file !== state.file;
  state.file = file;
  state.section = section;
  if (changed) { loadTopic(); if (section === -1) state.section = sections.length - 1; }
  save(); render(); renderTopics();
}

function step(d) {
  const i = state.section + d;
  if (i >= 0 && i < sections.length) return go(state.file, i);
  const files = flow.filter(t => t.file).map(t => t.file);
  const t = files.indexOf(state.file) + d;
  if (t >= 0 && t < files.length) go(files[t], d > 0 ? 0 : -1);
}

function toggleReveal(i) {
  const id = sectionId(sections[state.section]);
  const set = new Set(state.revealed[id] || []);
  set.has(i) ? set.delete(i) : set.add(i);
  state.revealed[id] = [...set];
  save(); render();
  if (set.has(i)) {
    const f = document.querySelector(`.fence.reveal[data-i="${i}"]`);
    if (f) f.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }
}

function revealNext() {
  const sec = sections[state.section];
  const set = revealedFor(sec);
  for (let i = 0; i < sec.reveals; i++) if (!set.has(i)) return toggleReveal(i);
  toast(sec.reveals ? 'Everything on this page is shown' : 'Nothing to show on this page');
}

const allIndexes = n => Array.from({ length: n }, (_, i) => i);
function revealPage() {
  const sec = sections[state.section];
  if (!sec.reveals) return toast('Nothing to show on this page');
  state.revealed[sectionId(sec)] = allIndexes(sec.reveals);
  save(); render();
}
function collapsePage() { delete state.revealed[sectionId(sections[state.section])]; save(); render(); }

function toggleFullscreen() { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }
function togglePanel(id) {
  for (const p of ['topics', 'controls']) if (p !== id) $('#' + p).classList.remove('open');
  $('#' + id).classList.toggle('open');
}

const COMMANDS = [
  { group: 'Answers', label: 'Show next', keys: ['r'], hint: 'R', run: revealNext },
  { label: 'Show all on page', keys: ['a'], hint: 'A', run: revealPage },
  { label: 'Hide all on page', keys: ['h', 'R'], hint: 'H', run: collapsePage },
  { group: 'Navigate', label: 'Outline', keys: [], phone: true, run: () => { $('#controls').classList.remove('open'); document.body.classList.toggle('show-rail'); } },
  { label: 'Topics', keys: ['t'], hint: 'T', run: () => togglePanel('topics') },
  { label: 'Full screen', keys: ['f'], hint: 'F', run: toggleFullscreen },
  { label: 'All decks', keys: [], run: () => { location.href = '../index.html'; } },
];

function renderControls() {
  $('#controls').innerHTML = COMMANDS.map((c, i) =>
    (c.group ? `<div class="rail-h">${c.group}</div>` : '') +
    `<button class="cmd${c.phone ? ' phone-only' : ''}" data-c="${i}"><span>${c.label}</span>${c.hint ? `<kbd>${c.hint}</kbd>` : ''}</button>`).join('');
}

let toastTimer = null;
function toast(msg, ms = 1600) {
  const t = $('#toast');
  t.textContent = msg; t.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.remove('show'), ms);
}

// ---------- start ----------

function init() {
  document.body.classList.add('trainer', 'self'); // "trainer" = the laptop layout in theme.css (outline rail, touch bar)
  mermaid.initialize({
    startOnLoad: false, securityLevel: 'loose', theme: 'base',
    themeVariables: {
      fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif',
      primaryColor: '#eef4f9', primaryBorderColor: '#134F7C', primaryTextColor: '#1d2733',
      lineColor: '#134F7C', secondaryColor: '#fff1e8', tertiaryColor: '#f7f7f4',
    },
  });

  if (!state.file || !flow.some(t => t.file === state.file)) { state.file = (flow.find(t => t.file) || {}).file; state.section = 0; }
  state.revealed = state.revealed || {};
  loadTopic();
  renderTopics();
  render();

  $('#t-prev').addEventListener('click', () => step(-1));
  $('#t-next').addEventListener('click', () => step(1));
  $('#t-reveal').addEventListener('click', revealNext);
  $('#t-more').addEventListener('click', () => togglePanel('controls'));
  $('#controls-btn').addEventListener('click', () => togglePanel('controls'));
  $('#topic-btn').addEventListener('click', () => togglePanel('topics'));
  renderControls();
  $('#controls').addEventListener('click', e => {
    const b = e.target.closest('button[data-c]');
    if (!b) return;
    const c = COMMANDS[+b.dataset.c];
    if (c.label !== 'Outline') $('#controls').classList.remove('open');
    c.run();
  });
  $('#rail').addEventListener('click', e => {
    const li = e.target.closest('li[data-i]');
    if (li) { document.body.classList.remove('show-rail'); go(state.file, +li.dataset.i); }
  });
  $('#topics').addEventListener('click', e => {
    const li = e.target.closest('li[data-f]');
    if (li && li.dataset.f) { $('#topics').classList.remove('open'); go(li.dataset.f, 0); }
  });

  document.addEventListener('keydown', e => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.target.closest && e.target.closest('input, textarea, select')) return;
    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { e.preventDefault(); step(1); return; }
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); step(-1); return; }
    if (e.key === 'Escape') { $('#topics').classList.remove('open'); $('#controls').classList.remove('open'); document.body.classList.remove('show-rail'); return; }
    const c = COMMANDS.find(c => c.keys.includes(e.key));
    if (c) { e.preventDefault(); c.run(); }
  });
}

init();
