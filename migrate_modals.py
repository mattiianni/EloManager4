import os
import re

files_to_check = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root or '.gemini' in root:
        continue
    for file in files:
        if file.endswith('.tsx') and file != 'Modal.tsx' and file != 'HIGSheet.tsx':
            files_to_check.append(os.path.join(root, file))

for file in files_to_check:
    with open(file, 'r') as f:
        content = f.read()
    
    if '<Modal' in content or 'Modal from' in content:
        # Check if it imports Modal
        if "import Modal from '../components/ui/Modal" in content or 'import Modal from "./ui/Modal' in content:
            # Replace import
            content = re.sub(r"import Modal from '\.\./components/ui/Modal(?:\.tsx)?';", "import { HIGSheet } from '../components/ui/HIGSheet';", content)
            content = re.sub(r"import Modal from '\./ui/Modal(?:\.tsx)?';", "import { HIGSheet } from './ui/HIGSheet';", content)
            
            # Replace tags
            content = content.replace('<Modal', '<HIGSheet')
            content = content.replace('</Modal>', '</HIGSheet>')
            
            with open(file, 'w') as f:
                f.write(content)
            print(f"Migrated Modal to HIGSheet in {file}")

