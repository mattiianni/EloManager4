import re

with open('pages/PlayersPage.tsx', 'r') as f:
    content = f.read()

old_edit = """    const handleEditSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const newElo = parseFloat(editElo);
        if (playerToEdit && editName.trim() && editSurname.trim() && !isNaN(newElo)) {
            setIsSubmitting(true);"""

new_edit = """    const handleEditSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const newElo = parseFloat(editElo);
        const eName = editName.trim();
        const eSurname = editSurname.trim();
        if (playerToEdit && eName && eSurname && !isNaN(newElo)) {
            const isDuplicate = players.some(p => 
                p.id !== playerToEdit.id &&
                p.name.toLowerCase() === eName.toLowerCase() && 
                p.surname.toLowerCase() === eSurname.toLowerCase()
            );
            if (isDuplicate) {
                alert("Attenzione: Esiste già un altro giocatore con questo nome e cognome!");
                return;
            }
            setIsSubmitting(true);"""

content = content.replace(old_edit, new_edit)
content = content.replace('name: editName,', 'name: eName,')
content = content.replace('surname: editSurname,', 'surname: eSurname,')

with open('pages/PlayersPage.tsx', 'w') as f:
    f.write(content)

