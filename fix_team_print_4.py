import re

with open('services/printService.ts', 'r') as f:
    content = f.read()

# I see what went wrong. The blue header the user is complaining about is the "RISULTATO FINALE", "PUNTI", "Classifica Provvisoria" etc in the Team Tournament PDF screenshot!
# If you look at the screenshot:
# `RISULTATO FINALE` is in a blue header `#2563eb` (blue-600)
# `PUNTI` is in a blue header
# The `POS | SQUADRA | PT | G ...` table header is blue.
# The user wants "tutto come la grafica delle statistiche dei tornei a squadre". Wait, no, he said "a volte dei pdf hanno le intestazioni un pò tonde, a volte squadrate. ti ho detto che voglio tutto come la grafica delle statistiche dei tornei a squadre."
# Actually, the user's PDF screenshot shows blue headers. They said:
# "ma non ti avevo detto di fare i campi dei risultati verdi e staccati tra di loro e invece e poi che cazzo è sto colore un blu più chiaro, un po' più scuro, ma che cosa hai combinato?"
# They are complaining about the blue headers that I added or modified. Wait, the `printTeamTournamentMatchdayReport` has this CSS:
# `.header-cell { background-color: #2563eb; color: white; ... }`
# Let's change these blue headers to standard grey/black like the classic tournaments if that's what they mean.
# But wait, they said "come la grafica delle statistiche dei tornei a squadre". The `printTeamTournamentStatistics` uses `#1e3a6e` (dark blue) for headers.
# Let's replace ALL `2563eb` with `#e5e5ea` (grey) and text color to black? No, let's look at `printTeamTournamentStatistics` and see what it uses.

# Let's just fix the score text to make sure it's GREEN and separated in THIS file first.
# The `printTeamTournamentMatchdayReport` currently has:
# `<span style="background-color: #1e3a6e; color: white; padding: 3px 8px; ...">${scoreText}</span>` somewhere!

# Let's replace the EXACT lines where scoreText is used in `printTeamTournamentMatchdayReport`:

content = re.sub(
    r"<td style=\"text-align: center; width: 18%; font-size: 11px; padding: 3px 4px;\">\s*<span[^>]*>\$\{scoreText\}</span>\s*</td>",
    r"<td style=\"text-align: center; width: 18%; font-size: 11px; padding: 3px 4px;\">\n                    ${scoreTextHtml}\n                </td>",
    content
)

content = re.sub(
    r"<td style=\"text-align: center; width: 18%; font-size: 11px; padding: 3px 4px;\">\s*\$\{!sets \|\| teamTournamentScoreIsBlank\(sets\) \? null : `.*?`\}\s*</td>",
    r"<td style=\"text-align: center; width: 18%; font-size: 11px; padding: 3px 4px;\">\n                    ${scoreTextHtml}\n                </td>",
    content
)

content = re.sub(
    r"<td style=\"text-align: center; width: 18%; font-size: 11px; padding: 3px 4px;\">\s*\$\{!sets \|\| teamTournamentScoreIsBlank\(sets\) \? null : scoreTextHtml\}\s*</td>",
    r"<td style=\"text-align: center; width: 18%; font-size: 11px; padding: 3px 4px;\">\n                    ${scoreTextHtml}\n                </td>",
    content
)

content = re.sub(
    r"\$\{\!sets \|\| teamTournamentScoreIsBlank\(sets\) \? `.*` : `.*`\}",
    r"${scoreTextHtml}",
    content
)


# Let's also fix the colors the user was complaining about.
# `#2563eb` (blue-600), `#dbeafe` (blue-100) -> remove them. Let's make headers dark blue `#1e3a6e` or grey `#e5e5ea` like the rest.
content = content.replace('#2563eb', '#1e3a6e')
content = content.replace('#dbeafe', '#f2f2f7')

with open('services/printService.ts', 'w') as f:
    f.write(content)

