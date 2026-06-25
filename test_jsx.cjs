const fs = require('fs');
const acorn = require('acorn');
const jsx = require('acorn-jsx');
const tsPlugin = require('acorn-typescript');

const content = fs.readFileSync('pages/TournamentsPage.tsx', 'utf8');

try {
  acorn.Parser.extend(jsx(), tsPlugin({ jsx: true })).parse(content, { sourceType: 'module', ecmaVersion: 2020 });
  console.log("Parse OK");
} catch(e) {
  console.log("Parse Error at line " + e.loc.line + " col " + e.loc.column + ": " + e.message);
  
  // print context
  const lines = content.split('\n');
  const start = Math.max(0, e.loc.line - 5);
  const end = Math.min(lines.length, e.loc.line + 5);
  for (let i = start; i < end; i++) {
     console.log((i+1) + ": " + lines[i]);
  }
}
