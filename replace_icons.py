import os
import re

icon_map = {
    'SearchIcon': 'magnifyingglass',
    'TrophyIcon': 'trophy.fill',
    'UsersIcon': 'person.2.fill',
    'UserIcon': 'person.fill',
    'ChartBarIcon': 'chart.bar.fill',
    'ChartLineUpIcon': 'chart.line.uptrend.xyaxis',
    'XIcon': 'xmark',
    'CheckIcon': 'checkmark',
    'RefreshIcon': 'arrow.clockwise',
    'MenuIcon': 'line.3.horizontal',
    'HomeIcon': 'house.fill',
    'CogIcon': 'gearshape.fill',
    'TrashIcon': 'trash.fill',
    'PlusIcon': 'plus',
    'PencilIcon': 'pencil',
    'AlertTriangleIcon': 'exclamationmark.triangle.fill',
    'ChevronRightIcon': 'chevron.right',
    'ChevronLeftIcon': 'chevron.left',
    'ChevronDownIcon': 'chevron.down',
    'ChevronUpIcon': 'chevron.up',
    'InfoIcon': 'info.circle.fill',
    'CalendarIcon': 'calendar',
    'ArrowUpIcon': 'arrow.up',
    'ArrowDownIcon': 'arrow.down',
    'ArrowStableIcon': 'minus',
    'SaveIcon': 'square.and.arrow.down',
    'CrownIcon': 'crown.fill',
    'StarIcon': 'star.fill',
}

files_to_check = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root or '.gemini' in root:
        continue
    for file in files:
        if file.endswith('.tsx') and file != 'Icons.tsx' and file != 'SFIcon.tsx':
            files_to_check.append(os.path.join(root, file))

# We will just do a dry run to see how many replacements we can make
# Since this can be extremely invasive, let's just print what would be replaced.
for file in files_to_check:
    with open(file, 'r') as f:
        content = f.read()
    
    if 'import { ' in content and 'Icons.tsx' in content:
        # Check what icons are imported
        print(f"File: {file}")
        
