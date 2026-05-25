#!/usr/bin/env python3
"""Final pass — remaining scattered emojis."""
import os

BASE = '/Users/lucasgmoraes/Documents/GitHub/dr-growth-sistema'

def cal(w=13):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'

def lock(w=40):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>'

def check(w=14):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>'

def star(w=14):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'

def alert(w=14):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'

def file_text(w=14):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'

def dollar(w=14):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>'

def chart(w=14):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>'

def msg(w=14):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>'

def pkg(w=14):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 002 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>'

def wifi(w=14):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M5 12.55a11 11 0 0114.08 0"/><path d="M1.42 9a16 16 0 0121.16 0"/><path d="M8.53 16.11a6 6 0 016.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>'

CAL = cal(); LOCK40 = lock(40); CHECK = check(); STAR = star()
ALERT = alert(); FILETXT = file_text(); DOLLAR = dollar()
CHART = chart(); MSG = msg(); PKG = pkg(); WIFI = wifi()

REPLACEMENTS = {
    'administrativo.html': [
        # task empty state ✓
        ('empty-icon">✓<', 'empty-icon">' + CHECK + '<'),
        # task-check ✓
        ("${t.status==='done'?'✓':''}", "${t.status==='done'?'&#10003;':''}"),
        # toast ✓
        ("'Tarefa concluída! ✓'", "'Tarefa concluída!'"),
        # calendar in task due dates
        ("'>📅 ${fmt.relative(t.due_date)}", "'>"+CAL+" ${fmt.relative(t.due_date)}"),
        ("`📅 ${fmt.relative(t.due_date)}", '`'+CAL+' ${fmt.relative(t.due_date)}'),
        # lock icon in admin empty state
        ('<div class="empty-icon">🔒</div>', '<div class="empty-icon">' + LOCK40 + '</div>'),
        # logActivity icons → text
        ("{ icon:'📋',", "{ icon:'doc',"),
        ("{ icon:'🤝',", "{ icon:'+',"),
        ("{ icon:'✏️',", "{ icon:'/',"),
    ],
    'clientes.html': [
        # all-clear empty state
        ('empty-icon">✅<', 'empty-icon">' + CHECK + '<'),
        ('"✅">', '"' + CHECK + '">'),
        ('>✅<', '>' + CHECK + '<'),
    ],
    'dashboard.html': [
        ('empty-icon">★<', 'empty-icon">' + STAR + '<'),
        ('<span>📅 ${fmt.relative(t.due_date)}</span>', '<span>'+CAL+' ${fmt.relative(t.due_date)}</span>'),
        ('`📅 ${fmt.relative(t.due_date)}`', '`'+CAL+' ${fmt.relative(t.due_date)}`'),
    ],
    'financeiro.html': [
        # package badge
        ('>📦 ${plano}<', '>'+PKG+' ${plano}<'),
        ('"📦 ${plano}"', '"'+PKG+' ${plano}"'),
        # contract empty state
        ('empty-icon">📝<', 'empty-icon">'+FILETXT+'<'),
        # expenses empty state
        ('empty-icon">💸<', 'empty-icon">'+DOLLAR+'<'),
        # logActivity
        ("{ icon:'💰',", "{ icon:'+',"),
        ("{ icon:'💸',", "{ icon:'-',"),
        # balance check symbols
        ('>✓ Balanço conferido', '>&#10003; Balanço conferido'),
        ('>⚠ Divergência detectada<', '>&#9888; Divergência detectada<'),
    ],
    'tarafas.html': [],
    'tarefas.html': [
        # remaining 📅 in backtick template (different pattern)
        ('`<span style="color:${over?\'var(--red)\'', '`<span style="color:${over?\'var(--red)\''),
        (">📅 ${dueLabel}", '>'+CAL+' ${dueLabel}'),
        ('`📅 ${dueLabel}', '`'+CAL+' ${dueLabel}'),
        (">📅 ${dueLabel}<", '>'+CAL+' ${dueLabel}<'),
    ],
    'trafego.html': [
        # platform fallback icon
        ("{ name:c.platform, icon:'📊',", "{ name:c.platform, icon:'"+CHART+"',"),
        ("|| { icon:'📊' }", "|| { icon:'"+CHART+"' }"),
        ("||{ icon:'📊',", "||{ icon:'"+CHART+"',"),
        # notes with 💬
        ("'>💬 ${c.notes}<", '>'+MSG+' ${c.notes}<'),
        ("💬 ${c.notes}", MSG+" ${c.notes}"),
        # platform icon map for content
        ("Instagram:'📸'", "Instagram:'IG'"),
        ("Facebook:'📘'", "Facebook:'FB'"),
        ("LinkedIn:'💼'", "LinkedIn:'IN'"),
        ("TikTok:'🎵'", "TikTok:'TK'"),
        # fallback platform icon in template
        ("||'📱'}", "||'·'}"),
        # content calendar empty state
        ('empty-icon">📅<', 'empty-icon">'+CAL+'<'),
        # content card date calendar
        ('"📅 ${fmt.date(c.date)}"', '"'+CAL+' ${fmt.date(c.date)}"'),
        ('`📅 ${fmt.date(c.date)}', '`'+CAL+' ${fmt.date(c.date)}'),
        ("📅 ${fmt.date(c.date)}", CAL+" ${fmt.date(c.date)}"),
        # overdue label
        ("'⚠️ Atrasado'", "'Atrasado!'"),
        ("' ⚠️ Atrasado'", "' Atrasado!'"),
        # logActivity
        ("{ icon:'📊',", "{ icon:''+CHART+'',"),
    ],
    'hall.html': [
        # feed empty state
        ('empty-icon">📡<', 'empty-icon">'+WIFI+'<'),
        # inline chat icon in feed entry
        ("icon:'💬'", "icon:'"+MSG+"'"),
        # greeting bonus dollar
        ("bonusEl.textContent = '💰 ' + content.bonus;", "bonusEl.textContent = content.bonus;"),
        # weather — remaining (with variation selectors stripped or full replacement)
        ("'manha-limpa':'☀️'", "'manha-limpa':'☀'"),
        ("'manha-nuvem':'⛅'", "'manha-nuvem':'⛅'"),
        ("'tarde-limpa':'🌤️'", "'tarde-limpa':'⛅'"),
        ("'tarde-nuvem':'🌥️'", "'tarde-nuvem':'⛅'"),
        ("'noite-limpa':'🌙'", "'noite-limpa':'◑'"),
        ("'noite-nuvem':'☁️'", "'noite-nuvem':'☁'"),
        ("'madrugada':'🌑'", "'madrugada':'◐'"),
        ("'nublado-dia':'☁️'", "'nublado-dia':'☁'"),
        ("'nublado-noite':'☁️'", "'nublado-noite':'☁'"),
        ("'garoa-dia':'🌦️'", "'garoa-dia':'⛅'"),
        ("'garoa-noite':'🌧️'", "'garoa-noite':'⛅'"),
        ("'chuva-dia':'🌧️'", "'chuva-dia':'⛅'"),
        ("'chuva-noite':'🌧️'", "'chuva-noite':'⛅'"),
        ("'tempestade-dia':'⛈️'", "'tempestade-dia':'⛈'"),
        ("'tempestade-noite':'⛈️'", "'tempestade-noite':'⛈'"),
        ("'neve-dia':'❄️'", "'neve-dia':'❄'"),
        ("'neve-noite':'❄️'", "'neve-noite':'❄'"),
        ("'neblina-dia':'🌫️'", "'neblina-dia':'≋'"),
        ("'neblina-noite':'🌫️'", "'neblina-noite':'≋'"),
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
