import sys

with open('pages/StatistichePage.tsx', 'r') as f:
    content = f.read()

content = content.replace("import Card from '../components/ui/Card.tsx';", 
                          "import Card from '../components/ui/Card.tsx';\nimport { HIGList, HIGListRow, HIGListSection } from '../components/ui/HIGList.tsx';\nimport SFIcon from '../components/ui/SFIcon.tsx';")

with open('pages/StatistichePage.tsx', 'w') as f:
    f.write(content)
