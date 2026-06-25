import re

with open('services/printService.ts', 'r') as f:
    content = f.read()

# Replace where scoreTextHtml is used but might still be inside a span that we didn't catch because the color changed back to #1e3a6e.
content = re.sub(
    r"`<span style=\"[^\"]*background(?:-color)?:\s*#[0-9a-fA-F]+;[^\"]*>\$\{scoreTextHtml\}</span>`",
    r"scoreTextHtml",
    content
)

content = re.sub(
    r"<span style=\"[^\"]*background(?:-color)?:\s*#[0-9a-fA-F]+;[^\"]*>\$\{scoreTextHtml\}</span>",
    r"${scoreTextHtml}",
    content
)

# And look for the specific lines in `printTeamTournamentMatchdayReport` and `printTeamTournamentReport` where score was rendered for sets.
# e.g., `sm.sets ? \`<span ...>...</span>\` : ''`

content = re.sub(
    r"\(!sets \|\| teamTournamentScoreIsBlank\(sets\)\)\s*\?\s*null\s*:\s*scoreTextHtml",
    r"scoreTextHtml",
    content
)

content = re.sub(
    r"\(!sets \|\| teamTournamentScoreIsBlank\(sets\)\)\s*\?\s*''\s*:\s*scoreTextHtml",
    r"scoreTextHtml",
    content
)

with open('services/printService.ts', 'w') as f:
    f.write(content)

print("Fixed score text replacements")
