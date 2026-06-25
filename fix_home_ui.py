import re

with open('pages/DashboardPage.tsx', 'r') as f:
    content = f.read()

old_layout = """                                <div key={i} className="flex items-center justify-between p-4">
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded bg-indigo-500 flex items-center justify-center">
                                            <SFIcon name="sportscourt" size={16} color="white" />
                                        </div>
                                        <div>
                                            <div className="flex gap-1.5 items-center truncate">
                                                <span className={`truncate ${m.winner === 'team1' ? 'font-bold text-gray-900 dark:text-white' : 'font-normal text-gray-500 dark:text-gray-400'}`}>{m.t1}</span>
                                                <span className="text-gray-400 dark:text-gray-500 font-normal shrink-0 text-sm">vs</span>
                                                <span className={`truncate ${m.winner === 'team2' ? 'font-bold text-gray-900 dark:text-white' : 'font-normal text-gray-500 dark:text-gray-400'}`}>{m.t2}</span>
                                            </div>
                                            <div className="text-sm text-gray-500 dark:text-gray-400">{m.date}</div>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-1 font-mono text-base font-bold bg-gray-50 dark:bg-gray-900 px-3 py-1 rounded-md border border-gray-200 dark:border-gray-700">"""

new_layout = """                                <div key={i} className="flex items-center justify-between p-4 gap-2">
                                    <div className="flex items-center gap-3 min-w-0 flex-1">
                                        <div className="w-8 h-8 shrink-0 rounded bg-indigo-500 flex items-center justify-center">
                                            <SFIcon name="sportscourt" size={16} color="white" />
                                        </div>
                                        <div className="min-w-0 flex-1">
                                            <div className="flex gap-1.5 items-center min-w-0">
                                                <span className={`truncate ${m.winner === 'team1' ? 'font-bold text-gray-900 dark:text-white' : 'font-normal text-gray-500 dark:text-gray-400'}`}>{m.t1}</span>
                                                <span className="text-gray-400 dark:text-gray-500 font-normal shrink-0 text-sm">vs</span>
                                                <span className={`truncate ${m.winner === 'team2' ? 'font-bold text-gray-900 dark:text-white' : 'font-normal text-gray-500 dark:text-gray-400'}`}>{m.t2}</span>
                                            </div>
                                            <div className="text-sm text-gray-500 dark:text-gray-400 truncate">{m.date}</div>
                                        </div>
                                    </div>
                                    <div className="flex shrink-0 items-center gap-1 font-mono text-base font-bold bg-gray-50 dark:bg-gray-900 px-3 py-1 rounded-md border border-gray-200 dark:border-gray-700">"""

content = content.replace(old_layout, new_layout)

with open('pages/DashboardPage.tsx', 'w') as f:
    f.write(content)

