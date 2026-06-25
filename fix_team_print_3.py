import re

with open('services/printService.ts', 'r') as f:
    content = f.read()

# I need to see where `scoreTextHtml` is injected in the HTML.
# In printTeamTournamentMatchdayReport:
# <td style="text-align: center; width: 18%; font-size: 11px; padding: 3px 4px;">
#     ${!sets || teamTournamentScoreIsBlank(sets) ? null : `...`}
# </td>
# Or something like that.

# Let's just find and replace the whole block in printTeamTournamentMatchdayReport that generates the score
content = re.sub(
    r"<td style=\"text-align: center; width: 18%; font-size: 11px; padding: 3px 4px;\">\s*(?:\$\{!sets \|\| teamTournamentScoreIsBlank\(sets\) \? null : scoreTextHtml\}|\$\{scoreTextHtml\})\s*</td>",
    r"<td style=\"text-align: center; width: 18%; font-size: 11px; padding: 3px 4px;\">\n                    ${scoreTextHtml}\n                </td>",
    content
)

content = re.sub(
    r"<td style=\"text-align: center; width: 18%; font-size: 10px; padding: 2px 4px;\">\s*(?:\$\{!sets \|\| teamTournamentScoreIsBlank\(sets\) \? '' : scoreTextHtml\}|\$\{scoreTextHtml\})\s*</td>",
    r"<td style=\"text-align: center; width: 18%; font-size: 10px; padding: 2px 4px;\">\n                        ${scoreTextHtml}\n                    </td>",
    content
)

# And what about the overall score for the team match? "1-2"
# E.g. `<span style="background-color: #1e3a6e; color: white; padding: 3px 12px; font-weight: 900; font-size: 11px; display: inline-block; line-height: 1;">${t1w}-${t2w}</span>`
# I should make sure I haven't broken it, but it should be fine. It is `#1e3a6e` which is original dark blue.

# Also, the user complained about "un blu più chiaro, un po' più scuro".
# Wait, let me check the CSS I injected for the team tournament tables.
# `border-top: 3px solid #2563eb; border-bottom: 3px solid #1e3a6e;`
# #2563eb is blue-600, #1e3a6e is dark blue. This was probably there originally.
# But wait, in the Python script I had replaced all #1e3a6e with #0284c7 (sky-600) and then back again. So it should be back to original.

with open('services/printService.ts', 'w') as f:
    f.write(content)

