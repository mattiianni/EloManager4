import re

with open('components/ui/HIGSheet.tsx', 'r') as f:
    content = f.read()

# Replace the padding line
old_padding = "padding: '0 0 env(safe-area-inset-bottom, 0)',"
new_padding = "padding: '0 0 calc(env(safe-area-inset-bottom, 0px) + 32px)',"

content = content.replace(old_padding, new_padding)

with open('components/ui/HIGSheet.tsx', 'w') as f:
    f.write(content)

