import re

files = [
    'pages/MatchesPage.tsx',
    'components/BeatTheBoxFlow.tsx',
    'components/TournamentFlow.tsx',
    'components/ui/BeatTheBoxAnimation.tsx'
]

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # Text colors
    content = re.sub(r'text-blue-\d+', 'text-ios-blue', content)
    content = re.sub(r'dark:text-blue-\d+', '', content) # remove dark mode specific since iOS vars handle dark mode automatically
    
    # Bg colors
    content = re.sub(r'bg-blue-50(0)?', 'bg-ios-blue', content) # matches bg-blue-500
    content = re.sub(r'bg-blue-50 ', 'bg-ios-bg-secondary ', content) # matches bg-blue-50
    content = re.sub(r'bg-blue-50"', 'bg-ios-bg-secondary"', content)
    
    content = re.sub(r'dark:bg-blue-\d+(/\d+)?', '', content)
    content = re.sub(r'hover:bg-blue-\d+', 'hover:bg-ios-blue/80', content)
    
    # Border colors
    content = re.sub(r'border-blue-\d+', 'border-ios-blue', content)
    content = re.sub(r'dark:border-blue-\d+', '', content)
    
    # Clean up double spaces
    content = re.sub(r'  +', ' ', content)
    content = content.replace(' "', '"')
    
    with open(file, 'w') as f:
        f.write(content)
    print(f"Fixed tailwind colors in {file}")

