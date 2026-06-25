import re
import os

# 1. Fix Header font size
header_path = 'components/layout/Header.tsx'
with open(header_path, 'r') as f:
    header_content = f.read()
header_content = header_content.replace(
    'fontSize: "16px", lineHeight: "20px"',
    'fontSize: "18px", lineHeight: "22px"'
)
with open(header_path, 'w') as f:
    f.write(header_content)

# 2. Add px-4 to HIGSheet children in TournamentFlow, BeatTheBoxFlow, MatchesPage
files_to_check = [
    'components/TournamentFlow.tsx',
    'components/BeatTheBoxFlow.tsx',
    'pages/MatchesPage.tsx',
    'pages/DrawPage.tsx'
]

for file_path in files_to_check:
    if not os.path.exists(file_path): continue
    
    with open(file_path, 'r') as f:
        content = f.read()
        
    # Replace <div className="space-y-X"> with <div className="space-y-X px-4"> inside HIGSheet context roughly.
    # A safe way is to find className="space-y-..." and if it doesn't have px-4, add it. 
    # But wait, not all space-y- are root children.
    # What if we just find instances of HIGSheet and ensure their direct children have px-4?
    # Alternatively, just inject px-4 into space-y- inside these files, since they usually lack horizontal padding.
    
    def add_px4(match):
        cls = match.group(1)
        if 'px-' not in cls and 'mx-' not in cls and 'p-' not in cls:
            return f'className="{cls} px-4"'
        return match.group(0)
        
    content = re.sub(r'className="([^"]*space-y-[^"]*)"', add_px4, content)
    
    # Also fix flex justify-end or similar button wrappers that might lack px-4
    def add_px4_flex(match):
        cls = match.group(1)
        if 'px-' not in cls and 'mx-' not in cls and 'p-' not in cls:
            return f'className="{cls} px-4"'
        return match.group(0)
        
    content = re.sub(r'className="([^"]*flex justify-end[^"]*)"', add_px4_flex, content)

    with open(file_path, 'w') as f:
        f.write(content)

