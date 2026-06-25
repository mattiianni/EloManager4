import re

files = [
    'components/TournamentFlow.tsx',
    'components/BeatTheBoxFlow.tsx'
]

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # replace import
    content = re.sub(r"import Modal from '\./ui/Modal(?:\.tsx)?';", "import { HIGSheet } from './ui/HIGSheet.tsx';", content)
    
    # replace tags
    content = content.replace('<Modal', '<HIGSheet')
    content = content.replace('</Modal>', '</HIGSheet>')
    
    with open(file, 'w') as f:
        f.write(content)
    print(f"Migrated Modal to HIGSheet in {file}")

