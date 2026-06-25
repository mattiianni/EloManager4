import re

with open('pages/TournamentsPage.tsx', 'r') as f:
    content = f.read()

# Replace imports
content = content.replace(
    "import Card from '../components/ui/Card.tsx';",
    "import { HIGList, HIGListSection, HIGListRow } from '../components/ui/HIGList.tsx';\nimport SFIcon from '../components/ui/SFIcon.tsx';"
)
content = content.replace(
    "import Button from '../components/ui/Button.tsx';",
    "import HIGButton from '../components/ui/HIGButton.tsx';"
)
content = content.replace(
    "import { TrashIcon, PrintIcon, PencilIcon, ChevronDownIcon } from '../components/ui/Icons.tsx';",
    ""
)

# Fix Button usage to HIGButton
content = re.sub(r'<Button\b', '<HIGButton', content)
content = re.sub(r'</Button>', '</HIGButton>', content)

# Fix Icons to SFIcon
content = re.sub(r'<PencilIcon\s*/>', '<SFIcon name="pencil" />', content)
content = re.sub(r'<PrintIcon\s*/>', '<SFIcon name="printer" />', content)
content = re.sub(r'<TrashIcon\s*/>', '<SFIcon name="trash" />', content)
content = re.sub(r'<ChevronDownIcon\s+className=([^>]+)/>', r'<SFIcon name="chevron.down" className=\1 />', content)

# Fix Buttons size/variant
content = content.replace('variant="secondary"', 'variant="gray"')
content = content.replace('variant="danger"', 'variant="destructive"')
content = content.replace('size="lg"', 'size="large"')
content = content.replace('size="sm"', 'size="small"')

# Add standard HIG background to TournamentsSkeleton
content = content.replace('app-panel rounded-[24px]', 'bg-[var(--ios-secondarySystemGroupedBackground)] rounded-xl')

# Fix "Inizia da qui" Card to HIGListSection
card_inizia_old = """<Card>
                    <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-2">
                        <div>
                            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                                Inizia da qui!
                            </h2>
                            <p className="text-gray-500 dark:text-gray-400 mt-1">
                                Organizza un nuovo torneo, inserisci una giornata, sorteggia le coppie e memorizza i risultati
                            </p>
                        </div>
                        <HIGButton onClick={onOpenDrawLauncher} size="large" className="w-full flex-shrink-0 !font-bold !text-white sm:w-auto">
                            Nuovo Torneo / Nuova Giornata
                        </HIGButton>
                    </div>
                </Card>"""
                
card_inizia_new = """<HIGListSection>
                    <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4">
                        <div>
                            <h2 className="text-xl font-semibold text-[var(--ios-label)]">
                                Inizia da qui!
                            </h2>
                            <p className="text-[15px] text-[var(--ios-secondaryLabel)] mt-1">
                                Organizza un nuovo torneo, inserisci una giornata, sorteggia le coppie e memorizza i risultati
                            </p>
                        </div>
                        <HIGButton onClick={onOpenDrawLauncher} size="regular" variant="filled" className="w-full sm:w-auto">
                            Nuovo Torneo
                        </HIGButton>
                    </div>
                </HIGListSection>"""

content = content.replace(card_inizia_old, card_inizia_new)

# For tournaments, replace <Card title={...}> ... </Card> with HIGListSection
# Wait, parsing React components with regex is hard. Let's do string replacement for the Card tag.
content = content.replace(
    "<Card",
    "<div className=\"bg-[var(--ios-secondarySystemGroupedBackground)] rounded-[10px] overflow-hidden mb-6 shadow-sm\""
)
content = content.replace("</Card>", "</div>")
content = content.replace("title={", "data-title={")

# Replace "stitch-row" with "border-t border-[var(--ios-separator)]"
content = content.replace("stitch-row p-4 rounded-lg", "border-t border-[var(--ios-separator)] p-4")

with open('pages/TournamentsPage.tsx', 'w') as f:
    f.write(content)
