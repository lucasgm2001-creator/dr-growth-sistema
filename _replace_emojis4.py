#!/usr/bin/env python3
"""Fourth pass — true emoji (U+1F300+) and emoji-presentation symbols."""
import os, re

BASE = '/Users/lucasgmoraes/Documents/GitHub/dr-growth-sistema'

def cal(w=13):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'

CAL = cal()

REPLACEMENTS = {
    'administrativo.html': [
        # 📅 in backtick date templates (two distinct patterns)
        (">📅 ${fmt.relative(t.due_date)}", '>' + CAL + ' ${fmt.relative(t.due_date)}'),
        (">📅 ${fmt.date(t.due_date)}", '>' + CAL + ' ${fmt.date(t.due_date)}'),
    ],
    'hall.html': [
        # 🌐 globe fallback in calendar event icon
        ("|| '🌐'", "|| '·'"),
        # 📅 in empty calendar state
        (
            '<div class="cal-dp-empty-icon">📅</div>',
            '<div class="cal-dp-empty-icon">' + CAL + '</div>',
        ),
        # 📹 Reunião / 📌 Compromisso type labels — strip emoji prefix
        ("ev.isMeeting ? '📹 Reunião' : '📌 Compromisso'",
         "ev.isMeeting ? 'Reunião' : 'Compromisso'"),
        # ⛅ (U+26C5, Emoji_Presentation=Yes) → plain text
        ("'manha-nuvem':'⛅'", "'manha-nuvem':'~'"),
        ("'tarde-limpa':'⛅'", "'tarde-limpa':'~'"),
        ("'tarde-nuvem':'⛅'", "'tarde-nuvem':'~'"),
        ("'garoa-dia':'⛅'", "'garoa-dia':'~'"),
        ("'garoa-noite':'⛅'", "'garoa-noite':'~'"),
        ("'chuva-dia':'⛅'", "'chuva-dia':'~'"),
        ("'chuva-noite':'⛅'", "'chuva-noite':'~'"),
        # ⛈ (U+26C8, Emoji_Presentation=Yes) → plain text
        ("'tempestade-dia':'⛈'", "'tempestade-dia':'!!'"),
        ("'tempestade-noite':'⛈'", "'tempestade-noite':'!!'"),
    ],
    'trafego.html': [
        # STATUS_CONT fallback icon 📝
        ("icon:'📝'", "icon:'·'"),
        # logActivity icons
        ("icon:'📣'", "icon:'+'"),
        ("icon:'🗑️'", "icon:'×'"),
        ("icon:'🎬'", "icon:'▶'"),
        # empty state 📣
        ('<div class="empty-icon">📣</div>', '<div class="empty-icon">+</div>'),
    ],
}

changed = []
for fname, pairs in REPLACEMENTS.items():
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'MISSING {fname}')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()
    updated = original
    for old, new in pairs:
        updated = updated.replace(old, new)
    if updated != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated)
        changed.append(fname)
        print(f'UPDATED {fname}')
    else:
        print(f'UNCHANGED {fname}')

print(f'\nDone. Changed {len(changed)} files.')
