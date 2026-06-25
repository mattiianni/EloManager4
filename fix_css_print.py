import re

with open('services/printService.ts', 'r') as f:
    content = f.read()

# Add print-color-adjust to printTournamentStatistics CSS body
content = re.sub(
    r"body \{\s*font-family: 'Manrope', 'Aptos Narrow', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\s*font-feature-settings: 'cv11', 'tnum', 'lnum';\s*font-size: 11px;\s*line-height: 1.3;\s*margin: 0;\s*padding: 0;\s*background: white;\s*\}",
    r"body {\n                font-family: 'Manrope', 'Aptos Narrow', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\n                font-feature-settings: 'cv11', 'tnum', 'lnum';\n                font-size: 11px;\n                line-height: 1.3;\n                margin: 0;\n                padding: 0;\n                background: white;\n                -webkit-print-color-adjust: exact;\n                print-color-adjust: exact;\n            }",
    content
)

with open('services/printService.ts', 'w') as f:
    f.write(content)

