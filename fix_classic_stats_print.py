import re

with open('services/printService.ts', 'r') as f:
    content = f.read()

# I will replace the CSS for h3 and stat-card, or just replace the HTML generation strings directly.
# Let's replace the <h3> titles with the styled ones:
# <h3>Informazioni Generali</h3> -> <h3 style="background: #1e3a6e; color: #ffffff; padding: 6px 10px; font-size: 14px; font-weight: bold; border-radius: 6px 6px 0 0; margin: 0; text-transform: uppercase;">Informazioni generali</h3>

content = re.sub(
    r"<h3>Informazioni Generali</h3>\s*<div class=\"info-grid\">",
    r"""<h3 style="background: #1e3a6e; color: #ffffff; padding: 6px 10px; font-size: 14px; font-weight: bold; border-radius: 6px 6px 0 0; margin: 0;">Informazioni generali</h3>
        <div class="info-grid" style="border: 1px solid #1e3a6e; border-top: none; border-radius: 0 0 6px 6px; padding: 8px; margin-top: 0; margin-bottom: 18px;">""",
    content
)

content = re.sub(
    r"<h3>Top 5 Classifica</h3>\s*<table>",
    r"""<h3 style="background: #1e3a6e; color: #ffffff; padding: 6px 10px; font-size: 14px; font-weight: bold; border-radius: 6px 6px 0 0; margin: 0; text-transform: uppercase;">GIOCATORI - TOP 5</h3>
        <table style="margin-top: 0; border: 1px solid #1e3a6e; border-top: none;">""",
    content
)

# Replace other H3s similarly
content = re.sub(
    r"<h3>Statistiche Avanzate</h3>",
    r"", # We can remove this one, or replace it if needed. The team stats don't have "Statistiche Avanzate" header, it just shows the grid directly.
    content
)

content = re.sub(
    r"<h3>Nuove Statistiche</h3>",
    r"",
    content
)

content = re.sub(
    r"<h3>Premi Speciali</h3>",
    r"",
    content
)

content = re.sub(
    r"<h3>Classifica Completa</h3>\s*<table>",
    r"""<h3 style="background: #1e3a6e; color: #ffffff; padding: 6px 10px; font-size: 14px; font-weight: bold; border-radius: 6px 6px 0 0; margin: 0; margin-top: 18px; text-transform: uppercase;">Classifica giocatori</h3>
        <table style="margin-top: 0; border: 1px solid #1e3a6e; border-top: none;">""",
    content
)

# Now fix the stat cards:
# `<div class="stat-card">
#      <div class="stat-card-title">Più Games Vinti</div>`
# Becomes:
# `<div class="stat-card" style="border: 1px solid #1e3a6e; border-radius: 4px; overflow: hidden; background: #fff; padding: 0;">
#      <div class="stat-card-title" style="background: #1e3a6e; color: #fff; padding: 6px 8px; font-weight: bold; font-size: 11px; text-transform: uppercase; margin: 0;">Più Games Vinti</div>
#      <div style="padding: 8px;">`
# And then we need to close the padding div.
# Instead of regexing all that, let's redefine the stat-card generator or just use regex with closing div.

# The existing HTML uses `<div class="stat-card">\s*<div class="stat-card-title">TITLE</div>\s*${entries}\s*</div>`
def replace_stat_card(match):
    title = match.group(1)
    entries = match.group(2)
    return f"""<div class="stat-card" style="border: 1px solid #1e3a6e; border-radius: 4px; overflow: hidden; background: #fff; padding: 0;">
                <div class="stat-card-title" style="background: #1e3a6e; color: #fff; padding: 6px 8px; font-weight: bold; font-size: 11px; text-transform: uppercase; margin: 0;">{title}</div>
                <div style="padding: 8px;">
                    {entries}
                </div>
            </div>"""

content = re.sub(
    r'<div class="stat-card">\s*<div class="stat-card-title">(.*?)</div>(.*?)\s*</div>',
    replace_stat_card,
    content,
    flags=re.DOTALL
)

# Let's also fix the `.stat-card-entry` inside `printTournamentStatistics` (it was mapped with a specific class).
# In Team stats, it's just `<div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 11px;"><span>1. Name</span><strong>Value</strong></div>`
# But `printTournamentStatistics` maps entries like `<div class="stat-card-entry">1. Name Surname (value)</div>`.
# I'll modify the `stat-card-entry` CSS to match.
content = re.sub(
    r'\.stat-card-entry \{([^\}]*)\}',
    r'.stat-card-entry { font-size: 11px; color: #000; margin-bottom: 6px; line-height: 1.3; }',
    content
)

# And fix `th` style to match
# In printTournamentStatistics:
content = re.sub(
    r'th \{\s*background-color: #1e3a6e;\s*color: white;\s*padding: 5px 6px;\s*text-align: left;\s*font-weight: bold;\s*font-size: 11px;\s*\}',
    r'th { background-color: #1e3a6e; color: white; padding: 6px 10px; text-align: left; font-weight: bold; font-size: 11px; border: 1px solid #1e3a6e; }',
    content
)

with open('services/printService.ts', 'w') as f:
    f.write(content)

