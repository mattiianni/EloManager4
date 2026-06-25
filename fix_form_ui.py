import re

with open('pages/PlayersPage.tsx', 'r') as f:
    content = f.read()

# Fix Add form padding and remove borders
content = content.replace(
    '<form onSubmit={handleAddSubmit} className="space-y-4 pt-2">',
    '<form onSubmit={handleAddSubmit} className="space-y-6 pt-4 pb-8">'
)

# Fix Edit form padding and remove borders
content = content.replace(
    '<form onSubmit={handleEditSubmit} className="space-y-4 pt-2">',
    '<form onSubmit={handleEditSubmit} className="space-y-6 pt-4 pb-8">'
)

# Increase vertical padding and remove inner borders in the fields
content = content.replace('px-4 py-3 border-b border-ios-separator', 'px-4 py-5')
content = content.replace('px-4 py-3', 'px-4 py-5')

with open('pages/PlayersPage.tsx', 'w') as f:
    f.write(content)

