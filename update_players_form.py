import re

with open('pages/PlayersPage.tsx', 'r') as f:
    content = f.read()

# Add duplicate check logic to handleAddSubmit
old_add_submit = """    const handleAddSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (name.trim() && surname.trim()) {
            setIsSubmitting(true);"""

new_add_submit = """    const handleAddSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const nName = name.trim();
        const nSurname = surname.trim();
        if (nName && nSurname) {
            const isDuplicate = players.some(p => 
                p.name.toLowerCase() === nName.toLowerCase() && 
                p.surname.toLowerCase() === nSurname.toLowerCase()
            );
            if (isDuplicate) {
                alert("Attenzione: Esiste già un giocatore con questo nome e cognome!");
                return;
            }
            setIsSubmitting(true);"""

content = content.replace(old_add_submit, new_add_submit)
content = content.replace('await addPlayer(name, surname, position);', 'await addPlayer(nName, nSurname, position);')

# Fix UI for Add form
old_add_form = """                    <HIGListSection>
                        <div className="flex items-center px-4 py-2 border-b" style={{ borderColor: 'var(--ios-separator)' }}>
                            <input
                                type="text"
                                placeholder="Nome"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                className="w-full bg-transparent text-ios-label placeholder-ios-label-tertiary focus:outline-none"
                                required
                            />
                        </div>
                        <div className="flex items-center px-4 py-2 border-b" style={{ borderColor: 'var(--ios-separator)' }}>
                            <input
                                type="text"
                                placeholder="Cognome"
                                value={surname}
                                onChange={(e) => setSurname(e.target.value)}
                                className="w-full bg-transparent text-ios-label placeholder-ios-label-tertiary focus:outline-none"
                                required
                            />
                        </div>
                        <div className="flex items-center px-4 py-2">
                            <select
                                value={position}
                                onChange={(e) => setPosition(e.target.value as FieldPosition)}
                                className="w-full bg-transparent text-ios-label focus:outline-none"
                            >
                                {Object.values(FieldPosition).map(pos => (
                                    <option key={pos} value={pos}>{pos}</option>
                                ))}
                            </select>
                        </div>
                    </HIGListSection>"""

new_add_form = """                    <div className="bg-ios-bg-secondary rounded-xl overflow-hidden mx-4">
                        <div className="flex flex-col sm:flex-row sm:items-center px-4 py-3 border-b border-ios-separator">
                            <label className="sm:w-1/3 text-sm font-medium text-ios-label-secondary mb-1 sm:mb-0">Nome</label>
                            <input
                                type="text"
                                placeholder="Inserisci il nome"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                className="sm:w-2/3 bg-transparent text-ios-label focus:outline-none"
                                required
                            />
                        </div>
                        <div className="flex flex-col sm:flex-row sm:items-center px-4 py-3 border-b border-ios-separator">
                            <label className="sm:w-1/3 text-sm font-medium text-ios-label-secondary mb-1 sm:mb-0">Cognome</label>
                            <input
                                type="text"
                                placeholder="Inserisci il cognome"
                                value={surname}
                                onChange={(e) => setSurname(e.target.value)}
                                className="sm:w-2/3 bg-transparent text-ios-label focus:outline-none"
                                required
                            />
                        </div>
                        <div className="flex flex-col sm:flex-row sm:items-center px-4 py-3">
                            <label className="sm:w-1/3 text-sm font-medium text-ios-label-secondary mb-1 sm:mb-0">Posizione</label>
                            <select
                                value={position}
                                onChange={(e) => setPosition(e.target.value as FieldPosition)}
                                className="sm:w-2/3 bg-transparent text-ios-label focus:outline-none"
                            >
                                {Object.values(FieldPosition).map(pos => (
                                    <option key={pos} value={pos}>{pos}</option>
                                ))}
                            </select>
                        </div>
                    </div>"""

content = content.replace(old_add_form, new_add_form)

# Fix UI for Edit form
old_edit_form = """                    <HIGListSection>
                        <div className="flex items-center px-4 py-2 border-b" style={{ borderColor: 'var(--ios-separator)' }}>
                            <input
                                type="text"
                                placeholder="Nome"
                                value={editName}
                                onChange={(e) => setEditName(e.target.value)}
                                className="w-full bg-transparent text-ios-label focus:outline-none"
                                required
                            />
                        </div>
                        <div className="flex items-center px-4 py-2 border-b" style={{ borderColor: 'var(--ios-separator)' }}>
                            <input
                                type="text"
                                placeholder="Cognome"
                                value={editSurname}
                                onChange={(e) => setEditSurname(e.target.value)}
                                className="w-full bg-transparent text-ios-label focus:outline-none"
                                required
                            />
                        </div>
                        <div className="flex items-center px-4 py-2">
                            <select
                                value={editPosition}
                                onChange={(e) => setEditPosition(e.target.value as FieldPosition)}
                                className="w-full bg-transparent text-ios-label focus:outline-none"
                            >
                                {Object.values(FieldPosition).map(pos => (
                                    <option key={pos} value={pos}>{pos}</option>
                                ))}
                            </select>
                        </div>
                    </HIGListSection>"""

new_edit_form = """                    <div className="bg-ios-bg-secondary rounded-xl overflow-hidden mx-4">
                        <div className="flex flex-col sm:flex-row sm:items-center px-4 py-3 border-b border-ios-separator">
                            <label className="sm:w-1/3 text-sm font-medium text-ios-label-secondary mb-1 sm:mb-0">Nome</label>
                            <input
                                type="text"
                                placeholder="Inserisci il nome"
                                value={editName}
                                onChange={(e) => setEditName(e.target.value)}
                                className="sm:w-2/3 bg-transparent text-ios-label focus:outline-none"
                                required
                            />
                        </div>
                        <div className="flex flex-col sm:flex-row sm:items-center px-4 py-3 border-b border-ios-separator">
                            <label className="sm:w-1/3 text-sm font-medium text-ios-label-secondary mb-1 sm:mb-0">Cognome</label>
                            <input
                                type="text"
                                placeholder="Inserisci il cognome"
                                value={editSurname}
                                onChange={(e) => setEditSurname(e.target.value)}
                                className="sm:w-2/3 bg-transparent text-ios-label focus:outline-none"
                                required
                            />
                        </div>
                        <div className="flex flex-col sm:flex-row sm:items-center px-4 py-3">
                            <label className="sm:w-1/3 text-sm font-medium text-ios-label-secondary mb-1 sm:mb-0">Posizione</label>
                            <select
                                value={editPosition}
                                onChange={(e) => setEditPosition(e.target.value as FieldPosition)}
                                className="sm:w-2/3 bg-transparent text-ios-label focus:outline-none"
                            >
                                {Object.values(FieldPosition).map(pos => (
                                    <option key={pos} value={pos}>{pos}</option>
                                ))}
                            </select>
                        </div>
                    </div>"""

content = content.replace(old_edit_form, new_edit_form)

with open('pages/PlayersPage.tsx', 'w') as f:
    f.write(content)

