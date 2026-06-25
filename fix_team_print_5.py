import re

with open('services/printService.ts', 'r') as f:
    content = f.read()

content = re.sub(
    r"\$\{scoreText\s*\?\s*`<span[^>]*>\$\{scoreText\}</span>`\s*:\s*'<span[^>]*>&nbsp;</span>\s*-\s*<span[^>]*>&nbsp;</span>'\s*\}",
    r"${scoreTextHtml}",
    content
)

content = re.sub(
    r"<span style=\"background-color: #1e3a6e; color: white; padding: 2px 8px; font-weight: 900; font-size: 10px; display: inline-block; white-space: nowrap;\">\$\{scoreText\}</span>",
    r"${scoreTextHtml}",
    content
)

content = re.sub(
    r"`<span style=\"background: #1e3a6e; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;\">\$\{score\}</span>`",
    r"scoreHtml",
    content
)

content = re.sub(
    r"<span style=\"background: #1e3a6e; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;\">\$\{score\}</span>",
    r"${scoreHtml}",
    content
)

with open('services/printService.ts', 'w') as f:
    f.write(content)

