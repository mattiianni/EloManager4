import sys

def process_file():
    with open('pages/TournamentsPage.tsx', 'r') as f:
        content = f.read()

    # We need to replace `data-title={` with `><div className="border-b border-[var(--ios-separator)] p-4">`
    # and then the matching `}` with `</div><div className="p-4">`
    
    parts = content.split('data-title={')
    if len(parts) == 1:
        return
        
    out = parts[0]
    
    for part in parts[1:]:
        out += '>\n<div className="border-b border-[var(--ios-separator)] p-4">\n'
        
        # find matching bracket for part
        brace_count = 1
        i = 0
        while i < len(part) and brace_count > 0:
            if part[i] == '{':
                brace_count += 1
            elif part[i] == '}':
                brace_count -= 1
            i += 1
            
        out += part[:i-1] + '\n</div>\n<div className="p-0">\n' + part[i:]
        
    # We also need to remove the `>` from `<div className="..." key={groupId} >` since we added it.
    out = out.replace('shadow-sm"\n                                key={groupId}\n                                >', 'shadow-sm"\n                                key={groupId}')
        
    with open('pages/TournamentsPage.tsx', 'w') as f:
        f.write(out)

process_file()
