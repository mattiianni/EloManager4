import os
import re

keywords = ["successfully", "failed", "error", "completed", "updated", "deleted", "sure", "want to delete", "add", "edit", "save", "cancel", "tournament", "match", "player", "ratings"]
ignore = ["console.", "import", "className", "from", "export", "function", "const", "let", "var", "interface", "type", "return", "if", "else"]

findings = []

for root, _, files in os.walk('pages'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    lower_line = line.lower()
                    
                    if any(ign in lower_line for ign in ignore) and "alert" not in lower_line and "confirm" not in lower_line:
                        # don't completely skip, but we want to focus on UI text
                        pass

                    if "alert(" in lower_line or "confirm(" in lower_line or "throw new" in lower_line:
                        findings.append(f"{path}:{i+1}: {line.strip()}")
                        continue
                        
                    for kw in keywords:
                        # only if it's inside quotes or tags (heuristic)
                        if kw in lower_line and (">" in line or "'" in line or '"' in line or "`" in line):
                            # skip common code patterns
                            if "className=" in line or "=>" in line or "===" in line or "!==" in line:
                                continue
                            findings.append(f"{path}:{i+1}: {line.strip()}")
                            break

with open('english_findings.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(findings))

