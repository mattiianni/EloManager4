import re

with open('services/printService.ts', 'r') as f:
    content = f.read()

# 1. Add formatScoreBoxes helper at the top (after imports)
helper = """
const formatScoreBoxes = (sets: any[], isScheduled: boolean = false) => {
    if (isScheduled) return '<span style="border: 1px solid #ccc; padding: 3px 8px; display: inline-block; font-size: 11px;">&nbsp;</span> - <span style="border: 1px solid #ccc; padding: 3px 8px; display: inline-block; font-size: 11px;">&nbsp;</span>';
    if (!sets || sets.length === 0) return '<span style="border: 1px solid #ccc; padding: 3px 8px; display: inline-block; font-size: 11px;">&nbsp;</span> - <span style="border: 1px solid #ccc; padding: 3px 8px; display: inline-block; font-size: 11px;">&nbsp;</span>';
    
    const isBlank = sets.every((s: any) => Number(s?.team1 || 0) === 0 && Number(s?.team2 || 0) === 0);
    if (isBlank) return '<span style="border: 1px solid #ccc; padding: 3px 8px; display: inline-block; font-size: 11px;">&nbsp;</span> - <span style="border: 1px solid #ccc; padding: 3px 8px; display: inline-block; font-size: 11px;">&nbsp;</span>';

    return sets.map((s: any) => 
        `<span style="background-color: #16a34a; color: white; padding: 3px 6px; border-radius: 2px; font-weight: bold; font-size: 11px; display: inline-block; margin: 0 2px;">${s.team1}-${s.team2}</span>`
    ).join('');
};
"""
if "formatScoreBoxes" not in content:
    content = content.replace('const isIOS = () => {', helper + '\nconst isIOS = () => {')

# 2. Fix round borders: replace 12px and 10px with 0px or 4px for blockier shapes
content = content.replace('border-radius: 12px', 'border-radius: 4px')
content = content.replace('border-radius: 10px', 'border-radius: 4px')

# 3. Replace all dark blue (#1e3a6e) with sky-600 (#0284c7)
content = content.replace('#1e3a6e', '#0284c7')

# 4. Find where score is used
# In many places it uses: `<span style="background-color: #0284c7; color: white; padding: 3px 8px; border-radius: 2px; font-weight: bold; font-size: 11px; display: inline-block;">${score}</span>`
# We want to replace these spans with just `${formatScoreBoxes(match.sets, tournament.status === 'scheduled')}`
# BUT we need to make sure we use the right variable (match.sets vs sm.sets vs sets).

# Pattern 1:
# const score = tournament.status === 'scheduled' ? '□-□' : match.sets.map(s => `${s.team1}-${s.team2}`).join(', ');
# ... `<span ...>${score}</span>`
content = re.sub(
    r"const score = tournament\.status === 'scheduled' \? '□-□' : match\.sets\.map\(s => `\$\{s\.team1\}-\$\{s\.team2\}`\)\.join\(', '\);",
    r"const scoreHtml = formatScoreBoxes(match.sets, tournament.status === 'scheduled');",
    content
)

content = re.sub(
    r"const score = tournament\.status === 'scheduled' \? '' : match\.sets\.map\(s => `\$\{s\.team1\}-\$\{s\.team2\}`\)\.join\(', '\);",
    r"const scoreHtml = formatScoreBoxes(match.sets, tournament.status === 'scheduled');",
    content
)

content = re.sub(
    r"const score = match\.sets\.map\(s => `\$\{s\.team1\}-\$\{s\.team2\}`\)\.join\(', '\);",
    r"const scoreHtml = formatScoreBoxes(match.sets, false);",
    content
)

# Replace the spans that use ${score} with ${scoreHtml}
# `<span style="background-color: #0284c7; color: white; padding: 3px 8px; border-radius: 2px; font-weight: bold; font-size: 11px; display: inline-block;">${score}</span>`
content = re.sub(
    r"`<span style=\"background-color: #0284c7; color: white;[^>]+>\$\{score\}</span>`",
    r"scoreHtml",
    content
)
# For places where score is inside HTML tags but not template literals
content = re.sub(
    r"<span style=\"background-color: #0284c7; color: white;[^>]+>\$\{score\}</span>",
    r"${scoreHtml}",
    content
)

with open('services/printService.ts', 'w') as f:
    f.write(content)

print("Done")
