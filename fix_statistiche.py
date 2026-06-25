import re

with open('pages/StatistichePage.tsx', 'r') as f:
    content = f.read()

# Replace StatBox definition
content = content.replace(
"""const StatBox: React.FC<{ label: string; value: string }> = ({ label, value }) => (
    <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded-lg flex flex-col items-center justify-center text-center">
        <div className="text-sm text-gray-500 dark:text-gray-400 mb-1">{label}</div>
        <div className="text-lg font-bold text-gray-900 dark:text-white">{value}</div>
    </div>
);""",
"""const StatBox: React.FC<{ label: string; value: string }> = ({ label, value }) => (
    <HIGListRow label={label} detail={value} />
);"""
)

# Replace StatCard definition
content = content.replace(
"""const StatCard: React.FC<{ title: string; entries: string[] }> = ({ title, entries }) => (
    <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
        <h5 className="font-semibold text-gray-900 dark:text-white mb-2 text-sm">{title}</h5>
        <div className="space-y-1">
            {entries.map((entry, idx) => (
                <div key={idx} className="text-sm text-gray-700 dark:text-gray-300">
                    {idx + 1}. {entry}
                </div>
            ))}
        </div>
    </div>
);""",
"""const StatCard: React.FC<{ title: string; entries: string[] }> = ({ title, entries }) => (
    <HIGListSection header={title}>
        {entries.map((entry, idx) => (
            <HIGListRow key={idx} label={`${idx + 1}. ${entry}`} />
        ))}
    </HIGListSection>
);"""
)

# Replace AwardCard definition
content = content.replace(
"""const AwardCard: React.FC<{ 
    title: string; 
    subtitle: string; 
    entries: string[]; 
    icon: React.ReactNode; 
    colorClass: string; 
}> = ({ title, subtitle, entries, icon, colorClass }) => (
    <div className={`p-4 rounded-lg border ${colorClass} bg-opacity-10`}>
        <div className="flex items-center gap-2 mb-2">
            {icon}
            <h5 className="font-bold">{title}</h5>
        </div>
        <p className="text-xs mb-3 opacity-80">{subtitle}</p>
        <div className="space-y-1">
            {entries.map((entry, idx) => (
                <div key={idx} className="text-sm font-medium">
                    {idx + 1}. {entry}
                </div>
            ))}
        </div>
    </div>
);""",
"""const AwardCard: React.FC<{ 
    title: string; 
    subtitle: string; 
    entries: string[]; 
    icon: React.ReactNode; 
    colorClass: string; 
}> = ({ title, subtitle, entries, icon, colorClass }) => (
    <HIGListSection header={`${title} - ${subtitle}`}>
        {entries.map((entry, idx) => (
            <HIGListRow key={idx} icon={icon} label={`${idx + 1}. ${entry}`} />
        ))}
    </HIGListSection>
);"""
)

# Now find all grid containers for StatBox and StatCard and AwardCard, and replace them with div
# Grid containers:
# <div className="grid grid-cols-2 md:grid-cols-4 gap-3"> for StatBox (Team Tournament)
content = content.replace('<div className="grid grid-cols-2 md:grid-cols-4 gap-3">', '<HIGListSection header="📋 Informazioni Generali">')
# The closing </div> for this grid needs to become </HIGListSection>. We can do it by replacing `</StatBox>\n                                </div>`
content = content.replace('/>\n                                <StatBox label="Media G/Partita" value={derived ? derived.mediaGamesPerPartita.toFixed(1) : \'—\'} />\n                            </div>', '/>\n                                <StatBox label="Media G/Partita" value={derived ? derived.mediaGamesPerPartita.toFixed(1) : \'—\'} />\n                            </HIGListSection>')

# Grid for classic tournament StatBox:
# <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
content = content.replace('<div className="grid grid-cols-2 md:grid-cols-3 gap-3">', '<HIGListSection header="📋 Informazioni Generali">')
content = content.replace('/>\n                                            <StatBox label="Circolo" value={stats.tournament.club} />\n                                        </div>', '/>\n                                            <StatBox label="Circolo" value={stats.tournament.club} />\n                                        </HIGListSection>')

# Remove the explicit <h4> headers since they are now in HIGListSection header
content = content.replace('<h4 className="text-md font-bold text-gray-900 dark:text-white mb-3">\n                                            📋 Informazioni Generali\n                                        </h4>\n', '')
content = content.replace('<h4 className="text-md font-bold text-gray-900 dark:text-white mb-3">\n                                            📊 Statistiche Avanzate\n                                        </h4>\n', '')
content = content.replace('<h4 className="text-md font-bold text-gray-900 dark:text-white mb-3">\n                                            🏅 Premi Speciali\n                                        </h4>\n', '')

# Replace grids for StatCard and AwardCard
content = content.replace('<div className="grid grid-cols-1 md:grid-cols-2 gap-4">', '<div className="space-y-6">')
content = content.replace('<div className="grid grid-cols-1 md:grid-cols-3 gap-4">', '<div className="space-y-6">')

with open('pages/StatistichePage.tsx', 'w') as f:
    f.write(content)

