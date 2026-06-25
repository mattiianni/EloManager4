import os

# 1. MatchesPage.tsx
with open('pages/MatchesPage.tsx', 'r') as f:
    matches_content = f.read()

matches_content = matches_content.replace(
    "'Please select four unique players.'",
    "'Per favore, seleziona 4 giocatori distinti.'"
)
matches_content = matches_content.replace(
    "'Adding Match...'",
    "'Salvataggio...'"
)
matches_content = matches_content.replace(
    "'Add Match'",
    "'Aggiungi Partita'"
)
matches_content = matches_content.replace(
    '"Select Player"',
    '"Seleziona Giocatore"'
)
with open('pages/MatchesPage.tsx', 'w') as f:
    f.write(matches_content)

# 2. DrawPage.tsx
with open('pages/DrawPage.tsx', 'r') as f:
    draw_content = f.read()

draw_content = draw_content.replace(
    "'Please fill all player slots.'",
    "'Per favore, riempi tutti gli slot dei giocatori.'"
)
draw_content = draw_content.replace(
    "`Not enough participants selected. Required: ${requiredParticipants}, Selected: ${participants.length}.`",
    "`Partecipanti insufficienti. Richiesti: ${requiredParticipants}, Selezionati: ${participants.length}.`"
)
with open('pages/DrawPage.tsx', 'w') as f:
    f.write(draw_content)

# 3. AdminPage.tsx
with open('pages/AdminPage.tsx', 'r') as f:
    admin_content = f.read()

admin_content = admin_content.replace(
    "'API request failed'",
    "'Richiesta al server fallita'"
)
with open('pages/AdminPage.tsx', 'w') as f:
    f.write(admin_content)

# 4. HIGDemoPage.tsx
with open('pages/HIGDemoPage.tsx', 'r') as f:
    demo_content = f.read()

demo_content = demo_content.replace(
    '"Are you sure you want to reset all settings to defaults? This action cannot be undone."',
    '"Sei sicuro di voler riportare tutte le impostazioni ai valori di fabbrica? Questa azione è irreversibile."'
)
with open('pages/HIGDemoPage.tsx', 'w') as f:
    f.write(demo_content)

