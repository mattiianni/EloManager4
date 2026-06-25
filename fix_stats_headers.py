import re

with open('pages/StatistichePage.tsx', 'r') as f:
    content = f.read()

# Replace <div className="... bg-sky-600 text-white ..."> with clean border-b version
# Typical format: <div className="px-4 py-2 bg-sky-600 text-white text-sm font-bold flex items-center gap-1.5">
# Or: <div className="px-4 py-2 bg-sky-600 text-white text-sm font-bold">
# Let's use regex to replace `bg-sky-600 text-white` with `border-b border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white`
# and we also need to change icon colors if they are forced to 'white'

content = re.sub(
    r'className="([^"]*)bg-sky-600 text-white([^"]*)"',
    r'className="\1border-b border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white\2"',
    content
)

# For `StatCard`, there is `{icon && React.cloneElement(icon as React.ReactElement, { color: 'white' })}`.
# I should change that back to standard color, or simply remove the `{ color: 'white' }` override.
# Let's replace `{ color: 'white' }` with `{ color: 'currentColor' }` or similar, or just not pass color.
# Actually, the original icon had its own color. Let's just render the `{icon}` directly.
content = content.replace(
    "{icon && React.cloneElement(icon as React.ReactElement, { color: 'white' })}",
    "{icon}"
)

# For TOP 5 Classifica: `<SFIcon name="trophy.fill" size={16} color="white" />`
content = content.replace(
    '<SFIcon name="trophy.fill" size={16} color="white" />',
    '<SFIcon name="trophy.fill" size={16} color="var(--ios-systemYellow)" />'
)

with open('pages/StatistichePage.tsx', 'w') as f:
    f.write(content)

print("Headers fixed in StatistichePage.tsx")
