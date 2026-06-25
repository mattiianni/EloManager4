import re

def remove_blue(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # MatchesPage uses `bg-blue-50 dark:bg-blue-900` and `bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800`
    # We replace them with generic HIG colors `bg-[var(--ios-secondarySystemGroupedBackground)]` or just `bg-white dark:bg-gray-800`
    content = content.replace('bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800', 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700')
    content = content.replace('bg-blue-50 dark:bg-blue-900', 'bg-gray-50 dark:bg-gray-800')
    content = content.replace('text-blue-800 dark:text-blue-200', 'text-gray-900 dark:text-white')
    content = content.replace('text-blue-600 dark:text-blue-300', 'text-gray-600 dark:text-gray-400')
    content = content.replace('text-blue-700 dark:text-blue-300', 'text-gray-700 dark:text-gray-300')
    content = content.replace('text-blue-900 dark:text-blue-300', 'text-gray-900 dark:text-gray-300')
    
    # StatistichePage.tsx has blue configuration in HIGListSection
    # blue: 'bg-blue-50 dark:bg-blue-900/20 border-blue-400/50 dark:border-blue-300/18',
    content = content.replace(
        "blue: 'bg-blue-50 dark:bg-blue-900/20 border-blue-400/50 dark:border-blue-300/18'",
        "blue: 'bg-gray-50 dark:bg-gray-800/50 border-gray-200 dark:border-gray-700'"
    )
    
    # TeamTournamentSummaryPage.tsx
    content = content.replace('bg-blue-600', 'bg-sky-500')

    with open(filepath, 'w') as f:
        f.write(content)

remove_blue('pages/MatchesPage.tsx')
remove_blue('pages/StatistichePage.tsx')
try:
    remove_blue('pages/TeamTournamentSummaryPage.tsx')
except Exception:
    pass
