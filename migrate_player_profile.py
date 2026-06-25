import re

file_path = 'components/PlayerProfileModal.tsx'
with open(file_path, 'r') as f:
    content = f.read()

# Add import
if 'import { HIGSheet }' not in content:
    content = content.replace("import { Player } from '../types.ts';", "import { Player } from '../types.ts';\nimport { HIGSheet } from './ui/HIGSheet.tsx';")

# Remove custom modal logic
content = re.sub(r'const modalRef = React\.useRef<HTMLDivElement>\(null\);.*?(?=// Only count matches)', '', content, flags=re.DOTALL)

# Replace return structure
# The old return starts like this:
# if (!player) return null;
# return (
#     <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in">
#         <div ref={modalRef} className={`w-full max-w-4xl max-h-[90vh] overflow-y-auto rounded-2xl shadow-2xl ...
old_return_pattern = r"if \(!player\) return null;\n\s*return \(\n\s*<div className=\"fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-fade-in\">\n\s*<div.*?>\n\s*<div className=\"sticky top-0 z-10 flex items-center justify-between p-6 border-b.*?>\n\s*<div>\n\s*<h2.*?>.*?</h2>\n\s*<p.*?>.*?</p>\n\s*</div>\n\s*<button.*?>\n\s*<XIcon.*?>\n\s*</button>\n\s*</div>"

# We will use regex to find the start of the return and replace it with HIGSheet
# It's easier to just do it via standard text replace or let python do the heavy lifting
