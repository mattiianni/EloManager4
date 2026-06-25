import re

with open('services/printService.ts', 'r') as f:
    content = f.read()

# 1. Revert the big blue headers in printTournamentStatistics (Classic Stats)
# I had: `<h3 style="background: #1e3a6e; color: #ffffff; padding: 6px 10px; font-size: 14px; font-weight: bold; border-radius: 6px 6px 0 0; margin: 0; text-transform: uppercase;">Informazioni generali</h3>`
# Let's just make it simple `<h3>Informazioni Generali</h3>` or a nice gray.
# Actually, the user says "che prima non c'era", meaning they didn't ask for blue headers anywhere.
# Let's replace `background: #1e3a6e; color: #ffffff; padding: 6px 10px; font-size: 14px; font-weight: bold; border-radius: 6px 6px 0 0; margin: 0; text-transform: uppercase;` with `font-size: 16px; font-weight: bold; margin: 0 0 10px 0; color: #111827;`
content = re.sub(
    r'background: #1e3a6e; color: #ffffff; padding: 6px 10px; font-size: 14px; font-weight: bold; border-radius: 6px 6px 0 0; margin: 0; text-transform: uppercase;',
    r'font-size: 16px; font-weight: bold; margin: 0 0 10px 0; color: #111827;',
    content
)

# And similarly for the other variations of this blue header:
content = re.sub(
    r'background: #1e3a6e; color: #ffffff; padding: 6px 10px; font-size: 14px; font-weight: bold; border-radius: 6px 6px 0 0; margin: 0; margin-top: 18px; text-transform: uppercase;',
    r'font-size: 16px; font-weight: bold; margin: 18px 0 10px 0; color: #111827;',
    content
)

content = re.sub(
    r'background: #1e3a6e; color: #ffffff; padding: 6px 10px; font-size: 14px; font-weight: bold; border-radius: 6px 6px 0 0; margin: 0;',
    r'font-size: 16px; font-weight: bold; margin: 0 0 10px 0; color: #111827;',
    content
)

# Revert border around the info-grid
content = re.sub(
    r'border: 1px solid #1e3a6e; border-top: none; border-radius: 0 0 6px 6px;',
    r'',
    content
)
content = re.sub(
    r'border: 1px solid #1e3a6e; border-top: none;',
    r'',
    content
)
content = re.sub(
    r'border: 1px solid #1e3a6e; border-radius: 4px; overflow: hidden; background: #fff; padding: 0;',
    r'',
    content
)
content = re.sub(
    r'background: #1e3a6e; color: #fff; padding: 6px 8px; font-weight: bold; font-size: 11px; text-transform: uppercase; margin: 0;',
    r'font-size: 12px; font-weight: bold; margin: 0 0 5px 0; color: #374151;',
    content
)

# Revert table headers in printTournamentStatistics
content = re.sub(
    r'th \{ background-color: #1e3a6e; color: white; padding: 6px 10px; text-align: left; font-weight: bold; font-size: 11px; border: 1px solid #1e3a6e; \}',
    r'th { padding: 5px 6px; text-align: left; font-weight: bold; font-size: 11px; border-bottom: 2px solid #e5e7eb; color: #374151; }',
    content
)


# Revert table headers in Team Tournament matches/standings (which I might have made #1e3a6e)
content = re.sub(
    r'th \{ background: #1e3a6e; color: white; font-size: 11px; padding: 5px 6px; text-align: center; border: 1px solid #e5e7eb; \}',
    r'th { background: #f8fafc; color: #1e3a8a; font-size: 11px; padding: 5px 6px; text-align: center; border-bottom: 2px solid #e2e8f0; border-top: 1px solid #e2e8f0; }',
    content
)
content = re.sub(
    r'th \{ background-color: #1e3a6e; color: white; padding: 6px 10px; text-align: left; font-weight: bold; font-size: 11px; border: 1px solid #1e3a6e; \}',
    r'th { background-color: #f8fafc; color: #1e3a8a; padding: 10px; text-align: left; font-weight: bold; font-size: 11px; border-bottom: 2px solid #e2e8f0; }',
    content
)
content = re.sub(
    r'background: #1e3a6e; color: #fff; border: 1px solid #e5e7eb;',
    r'background: #f8fafc; color: #1e3a8a; border-bottom: 2px solid #e2e8f0;',
    content
)

content = re.sub(
    r'background: #1e3a6e; color: #ffffff;',
    r'background: #f8fafc; color: #1e3a8a;',
    content
)

content = re.sub(
    r'background-color: #1e3a6e;',
    r'background-color: #f8fafc;',
    content
)


# 2. Fix green scores
# For the bracket and matchday scores:
# `return `<span style="background-color: #1e3a6e; color: white; padding: 3px 12px; font-weight: 900; font-size: 11px; display: inline-block; line-height: 1;">${t1w}-${t2w}</span>`;`
# Need to make them green and separated.
# Also the ones with `padding: 4px 12px`
green_score_html = r'`<div style="display: inline-flex; align-items: center; justify-content: center;"><span style="background-color: #16a34a; color: white; padding: 4px 8px; font-weight: 900; font-size: 12px; display: inline-block; line-height: 1; border-radius: 3px; min-width: 20px; text-align: center;">${t1w}</span><span style="margin: 0 4px; font-weight: bold; color: #4b5563;">-</span><span style="background-color: #16a34a; color: white; padding: 4px 8px; font-weight: 900; font-size: 12px; display: inline-block; line-height: 1; border-radius: 3px; min-width: 20px; text-align: center;">${t2w}</span></div>`'

content = re.sub(
    r'`<span style="background-color: #[a-f0-9]+; color: white; padding: \d+px \d+px; font-weight: 900; font-size: 11px; display: inline-block; line-height: 1;">\$\{t1w\}-\$\{t2w\}</span>`',
    green_score_html,
    content
)
content = re.sub(
    r'`<span style="background-color: #[a-f0-9]+; color: white; padding: \d+px \d+px; border-radius: 2px; font-weight: bold; font-size: 11px; display: inline-block;">\$\{X\}</span>`',
    r'`<span style="background-color: #16a34a; color: white; padding: 3px 8px; border-radius: 2px; font-weight: bold; font-size: 11px; display: inline-block;">${X}</span>`',
    content
)
content = re.sub(
    r'`<span style="background-color: #[a-f0-9]+; color: white; padding: 2px 8px; border-radius: 2px; font-weight: bold; font-size: 9px; display: inline-block;">\$\{ie\}</span>`',
    r'`<span style="background-color: #16a34a; color: white; padding: 2px 8px; border-radius: 2px; font-weight: bold; font-size: 9px; display: inline-block;">${ie}</span>`',
    content
)

# And in printService.ts, there are `border-bottom: 3px solid #1e3a6e;`
content = re.sub(
    r'border-bottom: 3px solid #1e3a6e;',
    r'border-bottom: 3px solid #e5e7eb;',
    content
)
content = re.sub(
    r'border-top: 3px solid #1e3a6e;',
    r'border-top: 3px solid #e5e7eb;',
    content
)
content = re.sub(
    r'color: #1e3a6e;',
    r'color: #111827;',
    content
)
content = re.sub(
    r'background: #1e3a6e;',
    r'background: #f8fafc;',
    content
)
content = re.sub(
    r'<span style="display:inline-block; padding: 4px 10px; background: #f8fafc; color: #fff; font-size: 11px; font-weight: 900;">',
    r'<span style="display:inline-block; padding: 4px 10px; background: #16a34a; color: #fff; font-size: 11px; font-weight: 900; border-radius: 3px;">',
    content
)


with open('services/printService.ts', 'w') as f:
    f.write(content)
