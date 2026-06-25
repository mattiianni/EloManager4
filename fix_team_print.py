import re

with open('services/printService.ts', 'r') as f:
    content = f.read()

# Replace all blue (#1e3a6e) or dark blue backgrounds in printService.ts
# I see #1e3a6e used in backgrounds for score spans inside `printTeamTournamentMatchdayReport`, `printTeamTournamentReport`, etc.
# Actually I need to find the specific score span that looks like `<span style="background-color: #1e3a6e; ...">${scoreText}</span>`
# In the Python script from before, I replaced #1e3a6e with #0284c7 (which is why the user sees a blue, sky-600 colored header / span now).
# Let's replace #0284c7 back with #1e3a6e for general headers if the user wanted that?
# Wait, the user said "ma che cazzo hai combinato? hai messo queste intestazioni blu... ti avevo detto verdi e staccate".
# Wait, no, the user said "i risultati vanno SEMPRE E OVUNQUE nei pdf inseriti in campi verdi, non blu"
# E per le intestazioni "che cazzo è sto colore un blu più chiaro... nella home ti ho detto nel PDF... queste intestazioni blu".
# In fact, I replaced #1e3a6e with #0284c7 EVERYWHERE in the file.
# The user wants:
# 1. Headers to be their original color or specifically they complain about the "blu più chiaro" I put. Let's revert ALL #0284c7 back to #1e3a6e (the original dark blue) or whatever it was for headers.
# 2. But the score spans should be green and separated. My formatScoreBoxes does green and separated, but I need to make sure I used it correctly for TEAM tournaments too.

content = content.replace('#0284c7', '#1e3a6e')

# Now for the score boxes. I need to make sure `formatScoreBoxes` is used everywhere, including in `printTeamTournamentMatchdayReport` and `printTeamTournamentReport` which I might have missed if they use `scoreText` instead of `score`.

# Look for `const scoreText = ...` and see if it's replaced.
# In `printTeamTournamentMatchdayReport`:
# `const scoreText = (!sets || teamTournamentScoreIsBlank(sets)) ? null : sets.map((s: any) => \`\${s.team1}-\${s.team2}\`).join(', ');`
content = re.sub(
    r"const scoreText = \(!sets \|\| teamTournamentScoreIsBlank\(sets\)\) \? null : sets\.map\(\(s: any\) => `\$\{s\.team1\}-\$\{s\.team2\}`\)\.join\(', '\);",
    r"const scoreTextHtml = formatScoreBoxes(sets, false);",
    content
)

content = re.sub(
    r"const scoreText = \(!sets \|\| teamTournamentScoreIsBlank\(sets\)\) \? '' : sets\.map\(\(s: any\) => `\$\{s\.team1\}-\$\{s\.team2\}`\)\.join\(', '\);",
    r"const scoreTextHtml = formatScoreBoxes(sets, false);",
    content
)

# And replace where `scoreText` is used in a span
content = re.sub(
    r"`<span style=\"[^\"]*background(?:-color)?:\s*#[0-9a-fA-F]+;[^\"]*>\$\{scoreText\}</span>`",
    r"scoreTextHtml",
    content
)

content = re.sub(
    r"<span style=\"[^\"]*background(?:-color)?:\s*#[0-9a-fA-F]+;[^\"]*>\$\{scoreText\}</span>",
    r"${scoreTextHtml}",
    content
)

# Wait, in `printTeamTournamentMatchdayReport` line ~2216:
# `? \`<span style="background-color: #1e3a6e; color: white; padding: 3px 8px; border-radius: 2px; font-weight: bold; font-size: 11px; display: inline-block;">\${scoreText}</span>\``
# Wait, I reverted `#0284c7` to `#1e3a6e` just above, so this should match `#1e3a6e`.

with open('services/printService.ts', 'w') as f:
    f.write(content)

print("Fixed printService.ts")
