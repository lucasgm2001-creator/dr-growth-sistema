#!/usr/bin/env python3
"""Second pass — remaining emojis after first run."""
import os

BASE = '/Users/lucasgmoraes/Documents/GitHub/dr-growth-sistema'

def mk(path, w=14):
    paths = {
        'lock':    f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>',
        'key':     f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="7.5" cy="15.5" r="5.5"/><path d="M21 2l-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/></svg>',
        'unlock':  f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 019.9-1"/></svg>',
        'users':   f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>',
        'settings':f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg>',
        'alert':   f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        'trash':   f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6M10 11v6M14 11v6"/><path d="M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2"/></svg>',
        'save':    f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>',
        'mail':    f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22 6 12 13 2 6"/></svg>',
        'tool':    f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/></svg>',
        'clip':    f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/></svg>',
        'check':   f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>',
        'chk-circle':f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
        'star':    f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
        'map':     f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>',
        'dollar':  f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>',
        'chart':   f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        'chart-up':f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
        'credit':  f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>',
        'zap':     f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        'target':  f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
        'calendar':f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
        'pin':     f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>',
        'video':   f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>',
        'home':    f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
        'rocket':  f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 00-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 012-3.95A12.88 12.88 0 0122 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 01-4 2z"/></svg>',
        'trend-dn':f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/></svg>',
        'award':   f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg>',
        'eye':     f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
        'globe':   f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>',
        'brief':   f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2"/></svg>',
        'folder':  f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>',
        'file':    f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
        'filetxt': f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
        'package': f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 002 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
        'phone':   f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 8.81a19.79 19.79 0 01-3.07-8.67A2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg>',
    }
    return paths.get(d, f'[{d}]')

# Pre-compute all SVG values
LOCK   = mk('lock'); KEY    = mk('key'); UNLOCK = mk('unlock')
USERS  = mk('users'); GEAR   = mk('settings'); ALERT  = mk('alert')
TRASH  = mk('trash'); SAVE   = mk('save'); MAIL   = mk('mail')
TOOL   = mk('tool'); CLIP   = mk('clip'); CHECK  = mk('check')
CHK_C  = mk('chk-circle'); STAR   = mk('star'); MAP    = mk('map')
DOLLAR = mk('dollar'); CHART  = mk('chart'); CHART_UP = mk('chart-up')
CREDIT = mk('credit'); ZAP    = mk('zap'); TARGET = mk('target')
CAL    = mk('calendar'); PIN    = mk('pin'); VIDEO  = mk('video')
HOME   = mk('home'); ROCKET = mk('rocket'); TRENDDN= mk('trend-dn')
AWARD  = mk('award'); EYE    = mk('eye'); GLOBE  = mk('globe')
BRIEF  = mk('brief'); FOLDER = mk('folder'); FILE   = mk('file')
FILETXT= mk('filetxt'); PKG    = mk('package'); PHONE  = mk('phone')
LOCK48 = mk('lock', 48)

REPLACEMENTS = {
    'admin.html': [
        ('<div class="empty-icon" style="font-size:48px">🔒</div>', f'<div class="empty-icon">{LOCK48}</div>'),
        ('>🔑<', f'>{KEY}<'),
        ('>🔐 Controle de Acesso<', f'>{LOCK} Controle de Acesso<'),
        ('>👥 Usuários<', f'>{USERS} Usuários<'),
        ('>⚙ Sistema<', f'>{GEAR} Sistema<'),
        ('>🗑 Limpar Mural<', f'>{TRASH} Limpar Mural<'),
        ('>🔓 Resetar Permissões<', f'>{UNLOCK} Resetar Permissões<'),
        ('>💾 Salvar permissões<', f'>{SAVE} Salvar permissões<'),
        ('⚠️ Execute apenas uma vez.', 'Atenção: Execute apenas uma vez.'),
        ('💡 Em produção com Supabase,', 'Em produção com Supabase,'),
        ('✉ ${u.email}', MAIL + ' ${u.email}'),
        ("'🔧 Permissões customizadas'", "'" + TOOL + " Permissões customizadas'"),
        ("'📋 Padrão da função'", "'" + CLIP + " Padrão da função'"),
        ("'✅ Conectado'", "'Conectado'"),
        ("'⚠️ Modo demo (sem Supabase)'", "'Modo demo (sem Supabase)'"),
    ],
    'administrativo.html': [
        ('>⚙<', f'>{GEAR}<'),
        ('>★ Clientes<', f'>{STAR} Clientes<'),
        ('>✓ Tarefas<', f'>{CHECK} Tarefas<'),
        ('>🗺 Mapa de Clientes<', f'>{MAP} Mapa de Clientes<'),
        ('>📋 Relatório<', f'>{CLIP} Relatório<'),
        ('>★<', f'>{STAR}<'),
        ('>⚠<', f'>{ALERT}<'),
        ('<span class="card-title">📋 Tarefas Concluídas</span>', f'<span class="card-title">{CHK_C} Tarefas Concluídas</span>'),
        ('empty-icon">★<', f'empty-icon">{STAR}<'),
        ("${t.status==='done'?'✓':''}", "${t.status==='done'?'&#10003;':''}"),
        ("'📅 ${fmt.relative(t.due_date)}", "'" + CAL + " ${fmt.relative(t.due_date)}"),
        ("' ⚠️'", "' !'"),
        ("{ icon:'✅',", "{ icon:'OK',"),
        ("{ icon:'⚙️',", "{ icon:'⚙',"),
    ],
    'clientes.html': [
        ('>🤝<', f'>{USERS}<'),
        ('>⚡<', f'>{ZAP}<'),
        ('>⚠<', f'>{ALERT}<'),
        ("contrato:'📄'", "contrato:'" + FILE + "'"),
        ("briefing:'📋'", "briefing:'" + CLIP + "'"),
        ("relatorio:'📊'", "relatorio:'" + CHART + "'"),
        ("proposta:'💼'", "proposta:'" + BRIEF + "'"),
        ("outro:'📁'", "outro:'" + FOLDER + "'"),
        ('empty-icon">📁<', f'empty-icon">{FOLDER}<'),
        ('<span>📁</span>', f'<span>{FOLDER}</span>'),
        ("doc-icon\">${TYPE_ICON[d.tipo]||'📄'}", "doc-icon\">${TYPE_ICON[d.tipo]||'" + FILE + "'}"),
        ("icon:'🔴'", "icon:'!'"),
        ("icon:'📅'", "icon:'" + CAL + "'"),
        ("icon:'💤'", "icon:'zzz'"),
        ("icon:'⚠️'", "icon:'!'"),
        ("icon:'✅'", "icon:'OK'"),
        ("{ icon:'🤝',", "{ icon:'+',"),
        ("{ icon:'⚡',", "{ icon:'z',"),
    ],
    'comercial.html': [
        ('<span class="card-title">🌎 Mercado: Brasil vs EUA</span>', f'<span class="card-title">{GLOBE} Mercado: Brasil vs EUA</span>'),
        ('<span class="card-title">🏆 Taxa de Fechamento por Responsável</span>', f'<span class="card-title">{AWARD} Taxa de Fechamento por Responsável</span>'),
        ("{ icon:'💬',", "{ icon:'msg',"),
        ("title=\"WhatsApp: ${l.phone}\">📞</a>`", 'title="WhatsApp: ${l.phone}">' + PHONE + '</a>`'),
        (">📞 Chamar no WhatsApp</a>`;", f'>{PHONE} Chamar no WhatsApp</a>`;'),
    ],
    'dashboard.html': [
        ('<span class="nav-icon">⬛</span> Dashboard', f'<span class="nav-icon">{HOME}</span> Dashboard'),
        ('<span class="nav-icon">✓</span> Tarefas', f'<span class="nav-icon">{CHECK}</span> Tarefas'),
        ('<span class="nav-icon">★</span> Clientes', f'<span class="nav-icon">{STAR}</span> Clientes'),
        ('<div class="kpi-icon green">★</div>', f'<div class="kpi-icon green">{STAR}</div>'),
        ('<div class="kpi-icon red">✓</div>', f'<div class="kpi-icon red">{CHECK}</div>'),
        ('empty-icon">✓<', f'empty-icon">{CHECK}<'),
        ("${t.status==='done'?'✓':''}", "${t.status==='done'?'&#10003;':''}"),
        ("'📅 ${fmt.relative(t.due_date)}'", "'" + CAL + " ${fmt.relative(t.due_date)}'"),
        ('`📅 ${fmt.relative(t.due_date)}`', '`' + CAL + ' ${fmt.relative(t.due_date)}`'),
        ('cal-dp-empty-icon">📅<', 'cal-dp-empty-icon">' + CAL + '<'),
    ],
    'financeiro.html': [
        ('>💰<', f'>{DOLLAR}<'),
        ('>📊 Visão Geral<', f'>{CHART} Visão Geral<'),
        ('>📋 Contas a Receber<', f'>{CLIP} Contas a Receber<'),
        ('>📝 Contratos<', f'>{FILETXT} Contratos<'),
        ('>💸 Despesas<', f'>{CREDIT} Despesas<'),
        ('>⚖️ Balanço<', f'>{CHART_UP} Balanço<'),
        ('>📈 Resultado<', f'>{CHART_UP} Resultado<'),
        ('<div class="overdue-alert-icon">⚠️</div>', f'<div class="overdue-alert-icon">{ALERT}</div>'),
        ('>⬆ ATIVO<', '>&uarr; ATIVO<'),
        ('>⬇ PASSIVO<', '>&darr; PASSIVO<'),
        ('>💎 PATRIMÔNIO LÍQUIDO<', f'>{STAR} PATRIMÔNIO LÍQUIDO<'),
        ('empty-icon">💰<', f'empty-icon">{DOLLAR}<'),
        ('>✓ Pago<', f'>{CHECK} Pago<'),
        ("'📦 ${plano}'", "'" + PKG + " ${plano}'"),
        ('`📦 ${plano}`', '`' + PKG + ' ${plano}`'),
    ],
    'trafego.html': [
        ('>🚀<', f'>{ROCKET}<'),
        ('>💸<', f'>{CREDIT}<'),
        ('>🎯<', f'>{TARGET}<'),
        ('>📉<', f'>{TRENDDN}<'),
        ('>⚙️ Configurar API<', f'>{GEAR} Configurar API<'),
        ('>⚙️ Configurar Meta Ads API<', f'>{GEAR} Configurar Meta Ads API<'),
        ("google:   { name:'Google Ads',  icon:'🔍',", "google:   { name:'Google Ads',  icon:'" + TARGET + "',"),
        ("meta:     { name:'Meta Ads',    icon:'📘',", "meta:     { name:'Meta Ads',    icon:'" + GLOBE + "',"),
        ("tiktok:   { name:'TikTok Ads',  icon:'🎵',", "tiktok:   { name:'TikTok Ads',  icon:'" + ZAP + "',"),
        ("linkedin: { name:'LinkedIn Ads',icon:'💼',", "linkedin: { name:'LinkedIn Ads',icon:'" + BRIEF + "',"),
        ("draft:     { label:'Rascunho',   cls:'badge-muted',   icon:'📝' },", "draft:     { label:'Rascunho',   cls:'badge-muted',   icon:'" + FILETXT + "' },"),
        ("revision:  { label:'Em revisão', cls:'badge-yellow',  icon:'👁' },", "revision:  { label:'Em revisão', cls:'badge-yellow',  icon:'" + EYE + "' },"),
        ("scheduled: { label:'Agendado',   cls:'badge-accent',  icon:'📅' },", "scheduled: { label:'Agendado',   cls:'badge-accent',  icon:'" + CAL + "' },"),
        ("published: { label:'Publicado',  cls:'badge-green',   icon:'✅' },", "published: { label:'Publicado',  cls:'badge-green',   icon:'OK' },"),
        ('empty-icon">🚀<', f'empty-icon">{ROCKET}<'),
    ],
    'funil.html': [
        ('<span class="nav-icon">⬛</span> Dashboard', f'<span class="nav-icon">{HOME}</span> Dashboard'),
        ('<span class="nav-icon">✓</span> Tarefas', f'<span class="nav-icon">{CHECK}</span> Tarefas'),
        ('<span class="nav-icon">★</span> Clientes', f'<span class="nav-icon">{STAR}</span> Clientes'),
        ("{ icon:'🤝',", "{ icon:'+',"),
        ("{ icon:'✏️',", "{ icon:'/',"),
        ("{ icon:'🎯',", "{ icon:'◎',"),
    ],
    'leads.html': [
        ('<span class="nav-icon">⬛</span> Dashboard', f'<span class="nav-icon">{HOME}</span> Dashboard'),
        ('<span class="nav-icon">✓</span> Tarefas', f'<span class="nav-icon">{CHECK}</span> Tarefas'),
        ('<span class="nav-icon">★</span> Clientes', f'<span class="nav-icon">{STAR}</span> Clientes'),
        ('Fechar ✕', f'Fechar {CHECK}'),
        ('>✏️ Editar<', f'>{TOOL} Editar<'),
    ],
    'tarefas.html': [
        ('<span class="nav-icon">⬛</span> Dashboard', f'<span class="nav-icon">{HOME}</span> Dashboard'),
        ('<span class="nav-icon">✓</span> Tarefas', f'<span class="nav-icon">{CHECK}</span> Tarefas'),
        ('<span class="nav-icon">★</span> Clientes', f'<span class="nav-icon">{STAR}</span> Clientes'),
        ('empty-icon">✓<', f'empty-icon">{CHECK}<'),
        ("${t.status==='done'?'✓':''}", "${t.status==='done'?'&#10003;':''}"),
        ("'📅 ${dueLabel}", "'" + CAL + " ${dueLabel}"),
        ('`📅 ${dueLabel}', '`' + CAL + ' ${dueLabel}'),
        ("' ⚠️'", "' !'"),
        ("'Tarefa concluída! ✓'", "'Tarefa concluída!'"),
        ("{ icon:'✏️',", "{ icon:'/',"),
        ("{ icon:'📋',", "{ icon:'doc',"),
        ("{ icon:'🗑️',", "{ icon:'×',"),
    ],
    'hall.html': [
        ('<span>👥</span>', f'<span>{USERS}</span>'),
        (' 👋</h1>', '</h1>'),
        ('👋</h1>', '</h1>'),
        ('<span style="font-size:14px;flex-shrink:0">📅</span>', f'<span style="flex-shrink:0">{CAL}</span>'),
        ('<span style="font-size:14px;flex-shrink:0">📌</span>', f'<span style="flex-shrink:0">{PIN}</span>'),
        ('<span>📹 Marcar como reunião</span>', f'<span>{VIDEO} Marcar como reunião</span>'),
        ("if (phase < 0.0625) return '🌑';", "if (phase < 0.0625) return '◐';"),
        ("if (phase < 0.1875) return '🌒';", "if (phase < 0.1875) return '◑';"),
        ("if (phase < 0.3125) return '🌓';", "if (phase < 0.3125) return '◒';"),
        ("if (phase < 0.4375) return '🌔';", "if (phase < 0.4375) return '◓';"),
        ("if (phase < 0.5625) return '🌕';", "if (phase < 0.5625) return '●';"),
        ("if (phase < 0.6875) return '🌖';", "if (phase < 0.6875) return '◓';"),
        ("if (phase < 0.8125) return '🌗';", "if (phase < 0.8125) return '◒';"),
        ("if (phase < 0.9375) return '🌘';", "if (phase < 0.9375) return '◑';"),
        ("return '🌑';", "return '◐';"),
    ],
    'index.html': [
        ("'✓ Bem-vindo, '", "'Bem-vindo, '"),
        ('"✓ Bem-vindo, "', '"Bem-vindo, "'),
        ("'✓ Conta criada!'", "'Conta criada!'"),
        ('"✓ Conta criada!"', '"Conta criada!"'),
        ("btn.textContent = '✓ Bem-vindo, '", "btn.textContent = 'Bem-vindo, '"),
    ],
}

HTML_FILES = [
    'comercial.html', 'dashboard.html', 'administrativo.html',
    'financeiro.html', 'trafego.html', 'clientes.html', 'tarefas.html',
    'leads.html', 'funil.html', 'admin.html', 'hall.html', 'index.html'
]

changed = []
for fname in HTML_FILES:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()
    updated = original
    for old, new in REPLACEMENTS.get(fname, []):
        updated = updated.replace(old, new)
    if updated != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated)
        changed.append(fname)
        print(f'UPDATED {fname}')
    else:
        print(f'UNCHANGED {fname}')

print(f'\nDone. Changed {len(changed)} files.')
