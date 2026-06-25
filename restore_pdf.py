import re

with open('services/printService.ts', 'r') as f:
    content = f.read()

# 1. Restore big blue headers in printTournamentStatistics (Classic Stats)
content = re.sub(
    r'font-size: 16px; font-weight: bold; margin: 0 0 10px 0; color: #111827;',
    r'background: #1e3a6e; color: #ffffff; padding: 6px 10px; font-size: 14px; font-weight: bold; border-radius: 6px 6px 0 0; margin: 0; text-transform: uppercase;',
    content
)

content = re.sub(
    r'font-size: 16px; font-weight: bold; margin: 18px 0 10px 0; color: #111827;',
    r'background: #1e3a6e; color: #ffffff; padding: 6px 10px; font-size: 14px; font-weight: bold; border-radius: 6px 6px 0 0; margin: 0; margin-top: 18px; text-transform: uppercase;',
    content
)

# Restore stat-card-title
content = re.sub(
    r'font-size: 12px; font-weight: bold; margin: 0 0 5px 0; color: #374151;',
    r'background: #1e3a6e; color: #fff; padding: 6px 8px; font-weight: bold; font-size: 11px; text-transform: uppercase; margin: 0;',
    content
)

# Restore table headers in printTournamentStatistics
content = re.sub(
    r'th \{ padding: 5px 6px; text-align: left; font-weight: bold; font-size: 11px; border-bottom: 2px solid #e5e7eb; color: #374151; \}',
    r'th { background-color: #1e3a6e; color: white; padding: 6px 10px; text-align: left; font-weight: bold; font-size: 11px; border: 1px solid #1e3a6e; }',
    content
)

# Restore table headers in Team Tournament matches/standings
content = re.sub(
    r'th \{ background: #f8fafc; color: #1e3a8a; font-size: 11px; padding: 5px 6px; text-align: center; border-bottom: 2px solid #e2e8f0; border-top: 1px solid #e2e8f0; \}',
    r'th { background: #1e3a6e; color: white; font-size: 11px; padding: 5px 6px; text-align: center; border: 1px solid #e5e7eb; }',
    content
)

content = re.sub(
    r'th \{ background-color: #f8fafc; color: #1e3a8a; padding: 10px; text-align: left; font-weight: bold; font-size: 11px; border-bottom: 2px solid #e2e8f0; \}',
    r'th { background-color: #1e3a6e; color: white; padding: 6px 10px; text-align: left; font-weight: bold; font-size: 11px; border: 1px solid #1e3a6e; }',
    content
)

content = re.sub(
    r'background: #f8fafc; color: #1e3a8a; border-bottom: 2px solid #e2e8f0;',
    r'background: #1e3a6e; color: #fff; border: 1px solid #e5e7eb;',
    content
)

content = re.sub(
    r'background: #f8fafc; color: #1e3a8a;',
    r'background: #1e3a6e; color: #ffffff;',
    content
)

content = re.sub(
    r'background-color: #f8fafc;',
    r'background-color: #1e3a6e;',
    content
)

content = re.sub(
    r'border-bottom: 3px solid #e5e7eb;',
    r'border-bottom: 3px solid #1e3a6e;',
    content
)
content = re.sub(
    r'border-top: 3px solid #e5e7eb;',
    r'border-top: 3px solid #1e3a6e;',
    content
)

with open('services/printService.ts', 'w') as f:
    f.write(content)
