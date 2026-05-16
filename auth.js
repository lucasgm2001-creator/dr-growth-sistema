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
    id: 'financeiro',
    label: 'Financeiro',
    floor: '03',
    page: 'financeiro.html',
    icon: '💰',
    color: '#22c55e',
    desc: 'MRR & Contratos',
    roles: ['financeiro'],
  },
  {
    id: 'administrativo',
    label: 'Administrativo',
    floor: '04',
    page: 'administrativo.html',
    icon: '⚙',
    color: '#f97316',
    desc: 'Clientes & Tarefas',
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
//  Mobile sidebar
// ============================================================
function initMobileSidebar() {
  const toggle  = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  if (!toggle || !sidebar) return;
  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    if (overlay) overlay.classList.toggle('show');
  });
  if (overlay) overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('show');
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
    { id:'all', flag:'🌐', label:'Todos', desc:'Visão consolidada' },
    { id:'br',  flag:'🇧🇷', label:'Brasil', desc:'Operação BR' },
    { id:'us',  flag:'🇺🇸', label:'EUA', desc:'US Operation' },
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

// Expõe globalmente
window.AUTH       = AUTH;
window.SECTIONS   = SECTIONS;
window.fmt        = fmt;
window.initPage   = initPage;
window.showToast  = showToast;
window.renderElevator = renderElevator;
window.initCountrySelector = initCountrySelector;
window.SFX        = SFX;
