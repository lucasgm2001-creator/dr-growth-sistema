#!/usr/bin/env python3
"""Replace emoji characters with SVG/text equivalents across DR Growth HTML files."""

import re, os

BASE = '/Users/lucasgmoraes/Documents/GitHub/dr-growth-sistema'

# ── SVG snippets (all use fill=none stroke=currentColor stroke-width=1.5) ──
SVG = {
    'hamburger': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>',
    'close':     '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    'search':    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    'edit':      '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>',
    'phone':     '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 8.81a19.79 19.79 0 01-3.07-8.67A2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg>',
    'phone-off': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="1" y1="1" x2="23" y2="23"/><path d="M9 9a2 2 0 01-.45 2.11L7.27 12.4a16 16 0 006.33 6.33l1.28-1.28A2 2 0 0117 17c.907.339 1.85.573 2.81.7A2 2 0 0122 19.92v3a2 2 0 01-2.18 2A19.79 19.79 0 0111.19 22a19.5 19.5 0 01-7.38-7.38A19.79 19.79 0 010 5.82 2 2 0 012 3.66h3A2 2 0 016.62 5.6"/></svg>',
    'calendar':  '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    'dollar':    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>',
    'chart-bar': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    'user':      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    'credit':    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>',
    'inbox':     '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11L2 12v6a2 2 0 002 2h16a2 2 0 002-2v-6l-3.45-6.89A2 2 0 0016.76 4H7.24a2 2 0 00-1.79 1.11z"/></svg>',
    'magnet':    '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M6 15A6 6 0 006 3H4v6h4"/><path d="M18 15A6 6 0 0018 3h-2v6h4"/><line x1="4" y1="9" x2="20" y2="9"/></svg>',
    'target':    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    'refresh':   '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 11-2.12-9.36L23 10"/></svg>',
    'trash':     '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2"/></svg>',
    'star':      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    'check':     '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>',
    'users':     '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>',
    'circle':    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/></svg>',
    'kanban':    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/></svg>',
    'list':      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>',
    'map':       '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>',
    'settings':  '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg>',
    'trending':  '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
    'building':  '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
    'globe':     '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>',
    'check-circle': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    'alert':     '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><triangle><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/></triangle><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    'eye':       '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
    'plus':      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
    'pin':       '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    'clipboard': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>',
    'message':   '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>',
    'file-text': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    'award':     '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg>',
    'task':      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>',
    'zap':       '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    'clock':     '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    'link':      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>',
    'wifi':      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M5 12.55a11 11 0 0114.08 0"/><path d="M1.42 9a16 16 0 0121.16 0"/><path d="M8.53 16.11a6 16 0 016.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>',
}

def s(key):
    return SVG.get(key, '')

# ── Priority colored circles (for option text we strip emoji, for HTML we use a span) ──
RED_DOT    = '<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#ef4444;vertical-align:middle;margin-right:4px"></span>'
YELLOW_DOT = '<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#eab308;vertical-align:middle;margin-right:4px"></span>'
GREEN_DOT  = '<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#22c55e;vertical-align:middle;margin-right:4px"></span>'

# ── File-specific replacements ─────────────────────────────────────────────
REPLACEMENTS = {
    # Applied to ALL html files
    '*': [
        # Menu toggle hamburger
        ('>☰<', f'>{s("hamburger")}<'),
        # Close X in buttons/modals
        ('>✕<', f'>{s("close")}<'),
        # Search icon span
        ('<span class="search-icon">🔍</span>', f'<span class="search-icon">{s("search")}</span>'),
        # Clock flags → text only
        ('<span class="clock-tz">🇧🇷 BR</span>', '<span class="clock-tz">BR</span>'),
        ('<span class="clock-tz">🇺🇸 ET</span>', '<span class="clock-tz">ET</span>'),
        # Edit button (template literal in JS and static HTML)
        ('>✏️<', f'>{s("edit")}<'),
    ],
    'comercial.html': [
        # Tabs
        ('>◈ Funil Kanban<', f'>{s("kanban")} Funil Kanban<'),
        ('>◉ Lista de Leads<', f'>{s("list")} Lista de Leads<'),
        ('>💰 Pipeline<', f'>{s("dollar")} Pipeline<'),
        ('>📊 Métricas<', f'>{s("chart-bar")} Métricas<'),
        ('>📞 Agenda<', f'>{s("phone")} Agenda<'),
        ('>💵 Comissões<', f'>{s("credit")} Comissões<'),
        ('>👤 Vendedores<', f'>{s("user")} Vendedores<'),
        # Modal titles
        ('>💰 Registrar Comissão<', f'>{s("dollar")} Registrar Comissão<'),
        # Card titles
        ('<span class="card-title">📥 Origem dos Leads</span>', f'<span class="card-title">{s("inbox")} Origem dos Leads</span>'),
        ('<span class="card-title">💰 Pipeline por Estágio</span>', f'<span class="card-title">{s("dollar")} Pipeline por Estágio</span>'),
        ('<span class="card-title">👤 Pipeline por Responsável</span>', f'<span class="card-title">{s("user")} Pipeline por Responsável</span>'),
        ('<span class="card-title">📊 Resumo do Funil</span>', f'<span class="card-title">{s("chart-bar")} Resumo do Funil</span>'),
        # Close button text
        ('Fechar ✕', f'Fechar {s("close")}'),
        # Form labels
        ('<label>📅 Próximo Contato</label>', f'<label>{s("calendar")} Próximo Contato</label>'),
        # Select options — strip emoji (can't use HTML in option)
        ('>🇺🇸 EUA<', '>EUA<'),
        ('>🇧🇷 Brasil<', '>Brasil<'),
        ('>🔴 Alta — contato urgente<', '>Alta — contato urgente<'),
        ('>🟡 Média — acompanhar<', '>Média — acompanhar<'),
        ('>🟢 Baixa — sem pressa<', '>Baixa — sem pressa<'),
        # Option with magnet
        ("value=\"Magnetic Funnels\">🧲 Magnetic Funnels<", "value=\"Magnetic Funnels\">Magnetic Funnels<"),
        # IA toggle button sparkle
        ('&#10024;</span> Preencher com IA', f'{s("star")}</span> Preencher com IA'),
        ('&#10024; Analisar e Preencher', f'{s("star")} Analisar e Preencher'),
        # Empty state icons in JS
        ("empty-icon\">📞<", f'empty-icon">{s("phone")}<'),
        ("empty-icon\">◉<", f'empty-icon">{s("circle")}<'),
        # JS template literals — flags in metrics section
        ('"🇺🇸 EUA <span', '"EUA <span'),
        ('"🇧🇷 Brasil <span', '"Brasil <span'),
        # Followup badge: 📅 labels
        ('label=`📅 Atrasado ', 'label=`Cal. Atrasado '),
        ("label='📅 Hoje'", "label='Cal. Hoje'"),
        ("label='📅 Amanhã'", "label='Cal. Amanhã'"),
        ('label=`📅 em ', 'label=`Cal. em '),
        # Priority map in JS
        ("{ alta:'🔴', media:'🟡', baixa:'🟢' }", "{ alta:'●', media:'●', baixa:'●' }"),
        # Magnetic funnels badge in JS template
        ("? '🧲 ' : ''", "? '' : ''"),
        ("? '🧲 ' : ''", "? '' : ''"),
        # Clock row in JS template (buildCard)
        ("🇧🇷 ${brTime}", "BR ${brTime}"),
        ("🇺🇸 ${usTime}", "EUA ${usTime}"),
        # STAGE_ACTIVITY icons → text SVG strings
        ("{ icon:'🔄',", "{ icon:'↺',"),
        ("{ icon:'😶',", "{ icon:'—',"),
        ("{ icon:'📅',", "{ icon:'Cal.',"),
        ("{ icon:'📋',", "{ icon:'Doc.',"),
        ("{ icon:'🎉',", "{ icon:'★',"),
        ("{ icon:'❌',", "{ icon:'✗',"),
        # logActivity calls
        ("logActivity({ icon:'✏️',", "logActivity({ icon:'/',"),
        ("logActivity({ icon:'🗑️',", "logActivity({ icon:'×',"),
        ("logActivity({ icon:'🤝',", "logActivity({ icon:'+',"),
        ("logActivity({ icon:'🎯',", "logActivity({ icon:'◎',"),
        # showToast with emoji
        ('showToast(`🎉 "', 'showToast(`"'),
        # no-phone button
        ('style="opacity:.6">📵</button>', f'style="opacity:.6">{s("phone-off")}</button>'),
        # table phone/edit buttons (full pattern)
        ('"📞"', f'"{s("phone")}"'),
    ],
    'dashboard.html': [
        ('>☰<', f'>{s("hamburger")}<'),
        ('<span class="clock-tz"><span class="tz-full">🇧🇷 São Paulo</span><span class="tz-short">🇧🇷 <small>SP</small></span></span>',
         '<span class="clock-tz"><span class="tz-full">São Paulo, BR</span><span class="tz-short"><small>SP</small></span></span>'),
        ('<span class="clock-tz"><span class="tz-full">🇺🇸 Orlando, FL</span><span class="tz-short">🇺🇸 <small>FL</small></span></span>',
         '<span class="clock-tz"><span class="tz-full">Orlando, FL</span><span class="tz-short"><small>FL</small></span></span>'),
        # Calendar emoji icon in HTML
        ('<span style="font-size:14px;flex-shrink:0">📅</span>', f'<span style="flex-shrink:0">{s("calendar")}</span>'),
        # Holiday legend
        ('<span class="cal-holiday-legend">🇧🇷🇺🇸 <em>feriado</em></span>',
         '<span class="cal-holiday-legend"><em>feriado</em></span>'),
        # TZ modal close
        ('>✕<', f'>{s("close")}<'),
        # TZ flag buttons → text
        ('<span class="tz-btn-flag">🇧🇷</span>', '<span class="tz-btn-flag">BR</span>'),
        ('<span class="tz-btn-flag">🇺🇸</span>', '<span class="tz-btn-flag">EUA</span>'),
        # bonus text
        ("bonusEl.textContent = '💰 ' + content.bonus;", "bonusEl.textContent = content.bonus;"),
        # Calendar empty state
        ("'cal-dp-empty-icon\">📅<", f"'cal-dp-empty-icon\">{s('calendar')}<"),
        # Weather icons in JS map — replace with text codes
        ("'manha-limpa':'☀️'",     "'manha-limpa':'☀'"),
        ("'manha-nuvem':'⛅'",     "'manha-nuvem':'⛅'"),
        ("'tarde-limpa':'🌤️'",    "'tarde-limpa':'🌤'"),
        ("'tarde-nuvem':'🌥️'",    "'tarde-nuvem':'🌥'"),
        ("'noite-limpa':'🌙'",     "'noite-limpa':'◑'"),
        ("'noite-nuvem':'☁️'",     "'noite-nuvem':'☁'"),
        ("'madrugada':'🌑'",       "'madrugada':'◐'"),
        ("'nublado-dia':'☁️'",     "'nublado-dia':'☁'"),
        ("'nublado-noite':'☁️'",   "'nublado-noite':'☁'"),
        ("'garoa-dia':'🌦️'",      "'garoa-dia':'🌧'"),
        ("'garoa-noite':'🌧️'",    "'garoa-noite':'🌧'"),
        ("'chuva-dia':'🌧️'",      "'chuva-dia':'🌧'"),
        ("'chuva-noite':'🌧️'",    "'chuva-noite':'🌧'"),
        ("'tempestade-dia':'⛈️'",  "'tempestade-dia':'⛈'"),
        ("'tempestade-noite':'⛈️'","'tempestade-noite':'⛈'"),
        ("'neve-dia':'❄️'",        "'neve-dia':'❄'"),
        ("'neve-noite':'❄️'",      "'neve-noite':'❄'"),
        ("'neblina-dia':'🌫️'",    "'neblina-dia':'≋'"),
        ("'neblina-noite':'🌫️'",  "'neblina-noite':'≋'"),
        # Timezone flags in JS data — keep as text
        ("flag:'🇧🇷'", "flag:'BR'"),
        ("flag:'🇺🇸'", "flag:'EUA'"),
        # Holiday flag fields
        (",flag:'🇧🇷'}", ",flag:'BR'}"),
        (",flag:'🇺🇸'}", ",flag:'EUA'}"),
        # Tz comparison box flag
        ("tzInfo?.flag||''}", "tzInfo?.flag||''}"),
        ('"🇧🇷 <strong>', '"BR <strong>'),
    ],
}

HTML_FILES = [
    'comercial.html', 'dashboard.html', 'administrativo.html',
    'financeiro.html', 'trafego.html', 'clientes.html', 'tarefas.html',
    'leads.html', 'funil.html', 'admin.html', 'hall.html', 'index.html'
]

def apply_replacements(filename, content):
    # Global replacements
    for old, new in REPLACEMENTS.get('*', []):
        content = content.replace(old, new)
    # File-specific
    for old, new in REPLACEMENTS.get(filename, []):
        content = content.replace(old, new)
    return content

changed = []
for fname in HTML_FILES:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'SKIP {fname} (not found)')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()
    updated = apply_replacements(fname, original)
    if updated != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated)
        changed.append(fname)
        print(f'UPDATED {fname}')
    else:
        print(f'UNCHANGED {fname}')

print(f'\nDone. Changed {len(changed)} files: {changed}')
