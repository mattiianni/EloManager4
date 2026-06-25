import re

with open('pages/AdminPage.tsx', 'r') as f:
    content = f.read()

# Add HIGSegmentedControl import
if "import { HIGSegmentedControl }" not in content:
    content = content.replace("import Button from '../components/ui/Button.tsx';", "import Button from '../components/ui/Button.tsx';\nimport { HIGSegmentedControl } from '../components/ui/HIGSegmentedControl.tsx';")

# Replace Tabs
tabs_html = """{/* Tabs */}
            <div className="flex gap-2 border-b border-gray-200 dark:border-gray-700 pb-2">
                {(['workspaces', 'codes', 'transfer', 'logs'] as const).map(tab => (
                    <button
                        key={tab}
                        onClick={() => setActiveTab(tab)}
                        className={`px-4 py-2 rounded-t-lg font-medium text-sm transition-colors ${
                            activeTab === tab
                                ? 'bg-sky-600 text-white'
                                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
                        }`}
                    >
                        {tab === 'workspaces' ? 'Workspace' : tab === 'codes' ? 'Codici Accesso' : tab === 'transfer' ? 'Invia dati' : 'Audit Log'}
                    </button>
                ))}
            </div>"""

new_tabs_html = """{/* Tabs */}
            <div className="mb-6 px-4 md:px-0 max-w-2xl mx-auto">
                <HIGSegmentedControl 
                    segments={['Workspace', 'Codici Accesso', 'Invia dati', 'Audit Log']}
                    selectedIndex={
                        activeTab === 'workspaces' ? 0 :
                        activeTab === 'codes' ? 1 :
                        activeTab === 'transfer' ? 2 : 3
                    }
                    onChange={(idx) => {
                        setActiveTab(idx === 0 ? 'workspaces' : idx === 1 ? 'codes' : idx === 2 ? 'transfer' : 'logs');
                    }}
                />
            </div>"""

content = content.replace(tabs_html, new_tabs_html)

with open('pages/AdminPage.tsx', 'w') as f:
    f.write(content)
