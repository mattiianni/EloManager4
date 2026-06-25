with open('pages/MatchesPage.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "alert('Tournament completed with finals! ELO ratings have been updated.');",
    "alert('Torneo completato con finali! I punteggi ELO sono stati aggiornati.');"
)

content = content.replace(
    "alert('Tournament completed! ELO ratings have been updated.');",
    "alert('Torneo completato! I punteggi ELO sono stati aggiornati.');"
)

with open('pages/MatchesPage.tsx', 'w') as f:
    f.write(content)
