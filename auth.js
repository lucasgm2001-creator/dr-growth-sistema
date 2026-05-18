// ============================================================
//  DR Growth Sistema — Auth, Permissions & Navigation
// ============================================================

// ---- Setores / Andares do Elevador ----
const SECTIONS = [
  {
    id: 'hall',
    label: 'Hall',
    floor: '★',
    page: 'hall.html',
    icon: '🏠',
    color: '#f59e0b',
    desc: 'Recepção',
    roles: [], // todos têm acesso
  },
  {
    id: 'trafego',
    label: 'Tráfego',
    floor: '01',
    page: 'trafego.html',
    icon: '📊',
    color: '#a855f7',
    desc: 'Campanhas & Métricas',
    roles: ['trafego'],
  },
  {
    id: 'comercial',
    label: 'Comercial',
    floor: '02',
    page: 'comercial.html',
    icon: '📈',
    color: '#3b82f6',
    desc: 'Funil & Leads',
    roles: ['comercial'],
  },
  {
    id: 'clientes',
    label: 'Clientes',
    floor: '03',
    page: 'clientes.html',
    icon: '🤝',
    color: '#10B981',
    desc: 'Pós-venda & Jobs',
    roles: ['comercial', 'financeiro', 'trafego'],
  },
  {
    id: 'financeiro',
    label: 'Financeiro',
    floor: '04',
    page: 'financeiro.html',
    icon: '💰',
    color: '#22c55e',
    desc: 'MRR & Contratos',
    roles: ['financeiro'],
  },
  {
    id: 'administrativo',
    label: 'Administrativo',
    floor: '05',
    page: 'administrativo.html',
    icon: '⚙',
    color: '#f97316',
    desc: 'Configurações',
    roles: ['financeiro', 'trafego'],
  },
];

const ADMIN_SECTION = {
  id: 'admin',
  label: 'Admin',
  floor: '⚙',
  page: 'admin.html',
  icon: '🔑',
  color: '#6366f1',
  desc: 'Configurações',
  roles: [],
};

// ---- Usuários de demonstração ----
const AUTH = {
  demoUsers: [
    { email: 'daniel@drgrowth.com',   password: 'daniel123',   name: 'Daniel Ramos',   role: 'admin',      color: '#6366f1' },
    { email: 'lucas@drgrowth.com',    password: 'lucas123',    name: 'Lucas Moraes',   role: 'comercial',  color: '#3b82f6' },
    { email: 'gabriel@drgrowth.com',  password: 'gabriel123',  name: 'Gabriel Ramos',  role: 'trafego',    color: '#a855f7' },
    { email: 'thamyris@drgrowth.com', password: 'thamyris123', name: 'Thamyris Lages', role: 'financeiro', color: '#22c55e' },
  ],

  roleLabels: {
    admin:     'Gestor · Acesso total',
    comercial: 'Comercial EUA',
    trafego:   'Tráfego & Administrativo',
    financeiro:'Administrativo & Financeiro',
  },

  roleInitials(name) {
    return name.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase();
  },

  saveSession(user) {
    localStorage.setItem('drg_session', JSON.stringify({
      ...user,
      password: undefined,
      loginAt: new Date().toISOString(),
    }));
  },

  getSession() {
    try {
      const raw = localStorage.getItem('drg_session');
      return raw ? JSON.parse(raw) : null;
    } catch { return null; }
  },

  clearSession() {
    localStorage.removeItem('drg_session');
  },

  async login(email, password) {
    const demo = this.demoUsers.find(u => u.email === email && u.password === password);
    if (demo) {
      this.saveSession(demo);
      return { user: demo, error: null };
    }

    if (window.drSupabase) {
      const { data, error } = await window.drSupabase.auth.signInWithPassword({ email, password });
      if (error) return { user: null, error: error.message };
      const { data: profile } = await window.drSupabase
        .from('profiles').select('*').eq('id', data.user.id).single();
      const user = { email, name: profile?.name || email, role: profile?.role || 'trafego', color: profile?.avatar_color || '#6366f1' };
      this.saveSession(user);
      return { user, error: null };
    }

    return { user: null, error: 'Credenciais inválidas.' };
  },

  // Cria os usuários demo no Supabase Auth (roda uma vez por dispositivo)
  async ensureDemoUsers() {
    if (!window.drSupabase) return;
    const key = 'drg_demo_seeded_v2';
    if (localStorage.getItem(key)) return;

    for (const u of this.demoUsers) {
      const { data, error } = await window.drSupabase.auth.signUp({
        email: u.email,
        password: u.password,
        options: { data: { name: u.name, role: u.role } },
      });

      if (!error && data?.user) {
        await window.drSupabase.from('profiles').upsert({
          id: data.user.id,
          name: u.name,
          role: u.role,
          avatar_color: u.color,
        }, { onConflict: 'id' });
      }
    }

    localStorage.setItem(key, '1');
  },

  // Cria um novo usuário via Supabase Auth + profiles
  async createUser({ name, email, password, role }) {
    if (!window.drSupabase) return { error: 'Supabase não disponível.' };

    const { data, error } = await window.drSupabase.auth.signUp({
      email,
      password,
      options: { data: { name, role } },
    });

    if (error) return { error: error.message };

    if (data?.user) {
      const colors = { admin: '#6366f1', comercial: '#3b82f6', trafego: '#a855f7', financeiro: '#22c55e' };
      await window.drSupabase.from('profiles').upsert({
        id: data.user.id,
        name,
        role,
        avatar_color: colors[role] || '#6366f1',
      }, { onConflict: 'id' });
    }

    return { error: null };
  },

  async logout() {
    if (window.drSupabase) await window.drSupabase.auth.signOut().catch(() => {});
    this.clearSession();
    window.location.href = 'index.html';
  },

  requireAuth() {
    const session = this.getSession();
    if (!session) { window.location.href = 'index.html'; return null; }
    return session;
  },

  // Verifica se usuário tem acesso a um setor
  hasAccess(sectionId, session) {
    const s = session || this.getSession();
    if (!s) return false;
    if (s.role === 'admin') return true;
    if (sectionId === 'hall') return true;

    // Verifica permissões customizadas salvas pelo admin
    const customPerms = this.getCustomPermissions(s.email);
    if (customPerms) return customPerms.includes(sectionId);

    // Fallback: permissões padrão por role
    const section = SECTIONS.find(x => x.id === sectionId);
    if (!section) return false;
    return section.roles.includes(s.role);
  },

  // Permissões customizadas por admin (localStorage)
  getCustomPermissions(email) {
    try {
      const all = JSON.parse(localStorage.getItem('drg_permissions') || '{}');
      return all[email] || null;
    } catch { return null; }
  },

  saveCustomPermissions(email, sectionIds) {
    try {
      const all = JSON.parse(localStorage.getItem('drg_permissions') || '{}');
      all[email] = sectionIds;
      localStorage.setItem('drg_permissions', JSON.stringify(all));
    } catch {}
  },
};

// ============================================================
//  Renderiza o Elevador (sidebar)
// ============================================================
function renderElevator(currentPage) {
  const session = AUTH.getSession();
  if (!session) return;

  const nav = document.getElementById('elevator-nav');
  if (!nav) return;

  let html = '';

  // Andares normais
  SECTIONS.forEach(section => {
    const isActive  = currentPage === section.page;
    const hasAccess = AUTH.hasAccess(section.id, session);
    const isLocked  = !hasAccess;

    html += `
      <div class="elevator-floor ${isActive ? 'active' : ''} ${isLocked ? 'locked' : ''}"
        data-tip="${section.label}"
        onclick="${isLocked ? `showAccessDenied('${section.label}')` : `location.href='${section.page}'`}"
        title="${section.desc}">
        <div class="floor-btn" style="${isActive ? `--floor-color:${section.color}` : ''}">
          <span class="floor-number" style="color:${isActive ? section.color : ''}">${section.floor}</span>
        </div>
        <div class="floor-info">
          <span class="floor-label">${section.label}</span>
          <span class="floor-desc">${section.desc}</span>
        </div>
        ${isLocked ? '<span class="floor-lock">🔒</span>' : ''}
        ${isActive ? `<div class="floor-indicator" style="background:${section.color}"></div>` : ''}
      </div>`;
  });

  // Admin panel (só para admins)
  if (session.role === 'admin') {
    const isActive = currentPage === ADMIN_SECTION.page;
    html += `
      <div class="elevator-floor admin-floor ${isActive ? 'active' : ''}"
        data-tip="${ADMIN_SECTION.label}"
        onclick="location.href='${ADMIN_SECTION.page}'" title="${ADMIN_SECTION.desc}">
        <div class="floor-btn" style="${isActive ? `--floor-color:${ADMIN_SECTION.color}` : ''}">
          <span class="floor-number" style="color:${isActive ? ADMIN_SECTION.color : ''}">${ADMIN_SECTION.floor}</span>
        </div>
        <div class="floor-info">
          <span class="floor-label">${ADMIN_SECTION.label}</span>
          <span class="floor-desc">${ADMIN_SECTION.desc}</span>
        </div>
        ${isActive ? `<div class="floor-indicator" style="background:${ADMIN_SECTION.color}"></div>` : ''}
      </div>`;
  }

  nav.innerHTML = html;
}

function showAccessDenied(sectionName) {
  showToast(`🔒 Acesso ao setor ${sectionName} não liberado. Solicite ao administrador.`, 'error');
}

// ============================================================
//  Renderiza perfil do usuário
// ============================================================
function renderUserProfile(session) {
  const el = document.getElementById('user-profile');
  if (!el || !session) return;
  el.innerHTML = `
    <div class="user-avatar" style="background:linear-gradient(135deg,${session.color},${session.color}88)">
      ${AUTH.roleInitials(session.name)}
    </div>
    <div class="user-info">
      <div class="name">${session.name}</div>
      <div class="role">${AUTH.roleLabels[session.role] || session.role}</div>
    </div>
    <button class="logout-btn" onclick="AUTH.logout()" title="Sair">⎋</button>
  `;
}

// ============================================================
//  Toast
// ============================================================
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span class="toast-icon">${icons[type] || icons.info}</span> ${message}`;
  container.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('show'));
  setTimeout(() => { toast.classList.remove('show'); setTimeout(() => toast.remove(), 350); }, 3800);
}

// ============================================================
//  Sidebar — 3 estados (desktop) + overlay (mobile)
//  closed (16 px) | semi (64 px, padrão) | full (240 px)
// ============================================================
function initMobileSidebar() {
  const toggle  = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  if (!toggle || !sidebar) return;

  const hasElevator = !!document.getElementById('elevator-nav');

  // Páginas sem elevator usam o overlay original
  if (!hasElevator) {
    toggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('show');
    });
    if (overlay) overlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      overlay.classList.remove('show');
    });
    return;
  }

  const isMobile = () => window.innerWidth <= 768;
  const KEY      = 'drg_sidebar_state';
  const CYCLE    = ['semi', 'full', 'closed'];

  function getState() {
    return document.body.getAttribute('data-sidebar') || 'semi';
  }
  function setState(state) {
    document.body.setAttribute('data-sidebar', state);
    if (!isMobile()) localStorage.setItem(KEY, state);
  }

  // Aplica estado salvo (ou padrão semi)
  setState(isMobile() ? 'semi' : (localStorage.getItem(KEY) || 'semi'));

  // Toggle: cicla pelos 3 estados no desktop, overlay no mobile
  toggle.addEventListener('click', () => {
    if (isMobile()) {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('show');
      return;
    }
    const cur = getState();
    setState(CYCLE[(CYCLE.indexOf(cur) + 1) % CYCLE.length]);
  });

  // Clique na faixa fechada → abre semi
  sidebar.addEventListener('click', () => {
    if (!isMobile() && getState() === 'closed') setState('semi');
  });

  if (overlay) overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('show');
  });
}

// ============================================================
//  Tooltip para estado semi (JS — evita clip do overflow)
// ============================================================
function initElevatorTooltips() {
  if (!document.getElementById('elevator-nav')) return;

  const tip = document.createElement('div');
  tip.id = 'elev-tip';
  tip.style.cssText = [
    'position:fixed', 'z-index:9999', 'pointer-events:none',
    'background:#1a2744', 'color:#f1f5f9', 'font-size:12px',
    'font-weight:600', 'white-space:nowrap', 'padding:5px 10px',
    'border-radius:6px', 'border:1px solid rgba(255,255,255,.15)',
    'box-shadow:0 4px 14px rgba(0,0,0,.45)', 'opacity:0',
    'transition:opacity .15s', 'top:0', 'left:0',
  ].join(';');
  document.body.appendChild(tip);

  let hideTimer;

  document.getElementById('elevator-nav').addEventListener('mouseover', e => {
    const floor = e.target.closest('.elevator-floor[data-tip]');
    if (!floor || document.body.getAttribute('data-sidebar') !== 'semi') return;
    clearTimeout(hideTimer);
    const r = floor.getBoundingClientRect();
    tip.textContent = floor.dataset.tip;
    tip.style.left   = (r.right + 8) + 'px';
    tip.style.top    = (r.top + r.height / 2 - tip.offsetHeight / 2) + 'px';
    tip.style.opacity = '1';
  });

  document.getElementById('elevator-nav').addEventListener('mouseout', () => {
    hideTimer = setTimeout(() => { tip.style.opacity = '0'; }, 80);
  });
}

// ============================================================
//  Clocks
// ============================================================
function startClocks() {
  function update() {
    const now = new Date();
    const elBR = document.getElementById('clock-br');
    const elUS = document.getElementById('clock-us');
    if (elBR) elBR.textContent = now.toLocaleTimeString('pt-BR', { timeZone: 'America/Sao_Paulo', hour: '2-digit', minute: '2-digit', second: '2-digit' });
    if (elUS) elUS.textContent = now.toLocaleTimeString('en-US', { timeZone: 'America/New_York', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
  }
  update();
  setInterval(update, 1000);
}

// ============================================================
//  Formatters
// ============================================================
const fmt = {
  currency(value, currency = 'BRL') {
    if (value == null) return '—';
    return new Intl.NumberFormat(currency === 'USD' ? 'en-US' : 'pt-BR', {
      style: 'currency', currency, minimumFractionDigits: 0,
    }).format(value);
  },
  date(dateStr) {
    if (!dateStr) return '—';
    return new Date(dateStr + 'T12:00:00').toLocaleDateString('pt-BR');
  },
  relative(dateStr) {
    if (!dateStr) return '';
    const diff = Math.floor((new Date(dateStr + 'T12:00:00') - new Date()) / 86400000);
    if (diff === 0) return 'Hoje';
    if (diff === 1) return 'Amanhã';
    if (diff === -1) return 'Ontem';
    if (diff > 0) return `em ${diff}d`;
    return `há ${Math.abs(diff)}d`;
  },
  initials(name) {
    if (!name) return '?';
    return name.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase();
  },
  avatarClass(name) {
    const first = (name || '').split(' ')[0];
    const map = { 'Daniel': 'daniel', 'Lucas': 'lucas', 'Gabriel': 'gabriel', 'Thamyris': 'thamyris' };
    return map[first] || 'accent';
  },
  timeAgo(isoStr) {
    if (!isoStr) return '';
    const diff = Math.floor((new Date() - new Date(isoStr)) / 60000);
    if (diff < 1) return 'agora';
    if (diff < 60) return `há ${diff}min`;
    const h = Math.floor(diff / 60);
    if (h < 24) return `há ${h}h`;
    return `há ${Math.floor(h / 24)}d`;
  },
};

// ============================================================
//  Inicialização comum
// ============================================================
function initPage(currentPage) {
  const session = AUTH.requireAuth();
  if (!session) return null;

  renderElevator(currentPage || window.location.pathname.split('/').pop());
  renderUserProfile(session);
  initMobileSidebar();
  startClocks();

  return session;
}

// ============================================================
//  Country Selector
// ============================================================
function initCountrySelector(module, onRefresh) {
  const key = 'drg_country_' + module;
  let current = localStorage.getItem(key) || 'all';

  const el = document.getElementById('country-selector');
  if (!el) return;

  const options = [
    { id:'us',  flag:'🇺🇸', label:'EUA',    desc:'US Operation' },
    { id:'br',  flag:'🇧🇷', label:'Brasil', desc:'Operação BR' },
    { id:'all', flag:'🌐', label:'Todos',  desc:'Visão consolidada' },
  ];

  el.className = 'country-selector animate-in';
  el.innerHTML = options.map(o => `
    <div class="country-card ${current === o.id ? 'active' : ''}" data-country="${o.id}">
      <span class="country-card-flag">${o.flag}</span>
      <div>
        <div class="country-card-name">${o.label}</div>
        <div class="country-card-desc">${o.desc}</div>
      </div>
    </div>
  `).join('');

  el.querySelectorAll('.country-card').forEach(card => {
    card.addEventListener('click', () => {
      current = card.dataset.country;
      localStorage.setItem(key, current);
      el.querySelectorAll('.country-card').forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      window._currentCountry = current;
      if (onRefresh) onRefresh(current);
    });
  });

  window._currentCountry = current;
  window.filterByCountry = (items) =>
    current === 'all' ? items : items.filter(i => !i.country || i.country === current);
}

// ============================================================
//  SFX Global (Web Audio API — sem arquivos externos)
// ============================================================
const SFX = (() => {
  let ctx = null;
  function getCtx() {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    return ctx;
  }
  function tone(freq, type, duration, vol, delay = 0) {
    try {
      const c = getCtx();
      const osc = c.createOscillator();
      const gain = c.createGain();
      osc.connect(gain); gain.connect(c.destination);
      osc.type = type;
      osc.frequency.setValueAtTime(freq, c.currentTime + delay);
      gain.gain.setValueAtTime(0, c.currentTime + delay);
      gain.gain.linearRampToValueAtTime(vol, c.currentTime + delay + 0.01);
      gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + delay + duration);
      osc.start(c.currentTime + delay);
      osc.stop(c.currentTime + delay + duration + 0.05);
    } catch (_) {}
  }
  return {
    click()   { tone(600, 'sine', 0.06, 0.06); },
    success() { tone(660, 'sine', 0.12, 0.12); tone(880, 'sine', 0.18, 0.09, 0.11); },
    error()   { tone(220, 'sawtooth', 0.14, 0.08); },
    open()    { tone(440, 'sine', 0.22, 0.10); tone(554, 'sine', 0.22, 0.08, 0.14); },
    done()    { tone(880, 'sine', 0.10, 0.16); tone(660, 'sine', 0.28, 0.08, 0.09); },
    newLead() {
      tone(523,  'sine', 0.09, 0.18);
      tone(659,  'sine', 0.09, 0.16, 0.10);
      tone(784,  'sine', 0.09, 0.16, 0.20);
      tone(1047, 'sine', 0.28, 0.20, 0.30);
    },
  };
})();

// Injetar sons nos botões primários automaticamente
document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('click', e => {
    const btn = e.target.closest('.btn-primary');
    if (btn && !btn.dataset.nosfx) SFX.click();
  });
});

// Toast com som
const _origShowToast = showToast;
function showToast(message, type = 'info') {
  _origShowToast(message, type);
  if (type === 'success') SFX.success();
  else if (type === 'error') SFX.error();
}

// ============================================================
//  Personal To-Do Widget (all sectors)
// ============================================================
function initTodo() {
  const s = AUTH.getSession();
  const userName = s ? s.name.split(' ')[0].toLowerCase() : 'user';
  const key = `drg_todo_${userName}`;

  function getTodos() { try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch { return []; } }
  function saveTodos(arr) { localStorage.setItem(key, JSON.stringify(arr)); }

  document.body.insertAdjacentHTML('beforeend', `
    <div id="todo-fab" class="todo-fab" onclick="window._todoToggle()">
      <span style="font-size:18px">📝</span>
      <span class="todo-badge" id="todo-badge" style="display:none">0</span>
    </div>
    <div id="todo-panel" class="todo-panel">
      <div class="todo-panel-header">
        <span>📝 Minhas Tarefas</span>
        <button class="todo-close-btn" onclick="window._todoToggle()">✕</button>
      </div>
      <div class="todo-input-row">
        <input type="text" id="todo-input" class="todo-input" placeholder="Nova tarefa…" maxlength="200"
          onkeydown="if(event.key==='Enter')window._todoAdd()">
        <button class="todo-add-btn" onclick="window._todoAdd()">+</button>
      </div>
      <div class="todo-list" id="todo-list"></div>
    </div>
  `);

  window._todoToggle = function() {
    document.getElementById('todo-panel').classList.toggle('open');
  };

  window._todoAdd = function() {
    const input = document.getElementById('todo-input');
    const text = input.value.trim();
    if (!text) return;
    const todos = getTodos();
    todos.unshift({ id: Date.now(), text, done: false });
    saveTodos(todos);
    input.value = '';
    _renderTodos();
  };

  window._todoCheck = function(id) {
    const todos = getTodos();
    const item = todos.find(t => t.id === id);
    if (item) item.done = !item.done;
    saveTodos(todos);
    _renderTodos();
  };

  window._todoDel = function(id) {
    saveTodos(getTodos().filter(t => t.id !== id));
    _renderTodos();
  };

  function _renderTodos() {
    const todos = getTodos();
    const pending = todos.filter(t => !t.done).length;
    const badge = document.getElementById('todo-badge');
    if (pending > 0) { badge.textContent = pending > 9 ? '9+' : pending; badge.style.display = 'flex'; }
    else { badge.style.display = 'none'; }
    const list = document.getElementById('todo-list');
    if (!todos.length) {
      list.innerHTML = `<div class="todo-empty">Sem tarefas. Adicione uma acima.</div>`;
      return;
    }
    list.innerHTML = todos.map(t => `
      <div class="todo-item${t.done ? ' done' : ''}">
        <div class="todo-check" onclick="window._todoCheck(${t.id})">${t.done ? '✓' : ''}</div>
        <div class="todo-text" onclick="window._todoCheck(${t.id})">${t.text}</div>
        <button class="todo-del" onclick="window._todoDel(${t.id})">✕</button>
      </div>`).join('');
  }

  _renderTodos();
}

document.addEventListener('DOMContentLoaded', initTodo);

// ============================================================
//  ACTIVITY LOG — log compartilhado entre todos os setores
// ============================================================
function logActivity(opts) {
  const session = AUTH.getSession ? AUTH.getSession() : null;
  const who = opts.who || (session ? session.name.split(' ')[0] : 'Sistema');
  const entry = {
    id: Date.now() + '_' + Math.random().toString(36).slice(2, 6),
    time: new Date().toISOString(),
    icon:   opts.icon   || '📌',
    color:  opts.color  || '#6366f1',
    msg:    opts.msg    || '',
    sector: opts.sector || '',
    who,
  };
  try {
    const existing = JSON.parse(localStorage.getItem('drg_activity') || '[]');
    existing.unshift(entry);
    localStorage.setItem('drg_activity', JSON.stringify(existing.slice(0, 400)));
  } catch(e) {
    console.warn('[logActivity] Falha ao salvar atividade:', e);
  }
}

// Expõe globalmente
window.AUTH       = AUTH;
window.logActivity = logActivity;
window.SECTIONS   = SECTIONS;
window.fmt        = fmt;
window.initPage   = initPage;
window.showToast  = showToast;
window.renderElevator = renderElevator;
window.initCountrySelector = initCountrySelector;
window.SFX        = SFX;
