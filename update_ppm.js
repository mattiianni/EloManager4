const fs = require('fs');
const path = 'components/PlayerProfileModal.tsx';
let content = fs.readFileSync(path, 'utf8');

// Add import
if (!content.includes('import { HIGSheet }')) {
    content = content.replace("import { Player } from '../types.ts';", "import { Player } from '../types.ts';\nimport { HIGSheet } from './ui/HIGSheet.tsx';");
}

// Remove useEffect for keyboard/mouse logic
content = content.replace(/const modalRef = React\.useRef<HTMLDivElement>\(null\);[\s\S]*?(?=\/\/ Only count matches)/, '');

// Replace return wrapper
const oldReturn = `    return (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4" role="dialog" aria-modal="true">
            <div ref={modalRef} className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-3xl max-h-[90vh] flex flex-col fade-in">
                {/* Header */}
                <header className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                    <div className="flex items-center gap-3">
                        <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                            {player.name} {player.surname}
                        </h2>
                        <span className="text-lg font-bold text-sky-600 dark:text-sky-400">
                            {player.currentElo.toFixed(0)}
                        </span>
                        {stats && stats.lastDelta > 0 && <ArrowUpIcon className="h-5 w-5 text-green-500" />}
                        {stats && stats.lastDelta < 0 && <ArrowDownIcon className="h-5 w-5 text-red-500" />}
                        {stats && stats.lastDelta === 0 && <ArrowStableIcon className="h-5 w-5 text-gray-400" />}
                    </div>
                    <div className="flex items-center gap-3">
                        <span className="text-sm text-gray-500 dark:text-gray-400">{player.position}</span>
                        <button onClick={onClose} className="text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-white" aria-label="Close">
                            <XIcon />
                        </button>
                    </div>
                </header>`;

const newReturn = `    return (
        <HIGSheet isOpen={true} onClose={onClose} title={\`\${player.name} \${player.surname}\`} trailingAction={{ label: 'Chiudi', onPress: onClose }}>
            <div className="w-full flex flex-col">
                {/* Custom header info */}
                <div className="flex items-center justify-between px-6 py-2 border-b border-[var(--ios-separator)]">
                    <div className="flex items-center gap-3">
                        <span className="text-lg font-bold text-sky-600 dark:text-sky-400">
                            ELO: {player.currentElo.toFixed(0)}
                        </span>
                        {stats && stats.lastDelta > 0 && <ArrowUpIcon className="h-5 w-5 text-green-500" />}
                        {stats && stats.lastDelta < 0 && <ArrowDownIcon className="h-5 w-5 text-red-500" />}
                        {stats && stats.lastDelta === 0 && <ArrowStableIcon className="h-5 w-5 text-gray-400" />}
                    </div>
                    <div className="flex items-center gap-3">
                        <span className="text-sm text-gray-500 dark:text-gray-400">{player.position}</span>
                    </div>
                </div>`;

content = content.replace(oldReturn, newReturn);

const oldFooter = `            </div>
        </div>
    );`;

const newFooter = `            </div>
        </HIGSheet>
    );`;

content = content.replace(oldFooter, newFooter);

fs.writeFileSync(path, content);
console.log('Done modifying PlayerProfileModal');
