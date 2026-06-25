import re

with open('services/printService.ts', 'r') as f:
    content = f.read()

# 1. Add getTeamTournamentScoreValue helper after isTeamTournamentEliminationDirect
helper_code = """const isTeamTournamentEliminationDirect = (config: TeamTournamentConfig | null | undefined) =>
    String(config?.format || '') === 'ELIMINAZIONE DIRETTA';

const getTeamTournamentScoreValue = (summary: any, teamProp: 'team1Wins' | 'team2Wins', config?: TeamTournamentConfig | null | undefined) => {
    if (!summary) return null;
    if (config?.scoringType === 'Differenza Games') {
        const val = summary[teamProp.replace('Wins', 'Games')];
        return Number.isFinite(Number(val)) ? Number(val) : '';
    } else {
        const pts = summary[teamProp.replace('Wins', 'Points')];
        if (pts !== undefined && pts !== null) return Number(pts);
        const wins = summary[teamProp];
        return Number.isFinite(Number(wins)) ? Number(wins) : '';
    }
};"""

content = re.sub(
    r"const isTeamTournamentEliminationDirect = \(config: TeamTournamentConfig \| null \| undefined\) =>\n    String\(config\?\.format \|\| ''\) === 'ELIMINAZIONE DIRETTA';",
    helper_code,
    content
)

# 2. Modify buildTeamTournamentFixtureContext to accept config
content = re.sub(
    r"const buildTeamTournamentFixtureContext = \(\n    teams: TeamTournamentTeam\[\],\n    fixtures: TeamTournamentFixture\[\],\n    matchdays: TeamTournamentMatchday\[\]\n\) => \{",
    "const buildTeamTournamentFixtureContext = (\n    teams: TeamTournamentTeam[],\n    fixtures: TeamTournamentFixture[],\n    matchdays: TeamTournamentMatchday[],\n    config?: TeamTournamentConfig | null\n) => {",
    content
)

# 3. Inside buildTeamTournamentFixtureContext, update getFixtureSummary
content = re.sub(
    r"const team1Wins = summary \? \(swap \? Number\(summary\.team2Wins \|\| 0\) : Number\(summary\.team1Wins \|\| 0\)\) : null;\n\s*const team2Wins = summary \? \(swap \? Number\(summary\.team1Wins \|\| 0\) : Number\(summary\.team2Wins \|\| 0\)\) : null;",
    "const team1Wins = summary ? getTeamTournamentScoreValue(summary, swap ? 'team2Wins' : 'team1Wins', config) : null;\n        const team2Wins = summary ? getTeamTournamentScoreValue(summary, swap ? 'team1Wins' : 'team2Wins', config) : null;",
    content
)

# 4. Modify renderTeamTournamentEliminationBracket to accept config
content = re.sub(
    r"const renderTeamTournamentEliminationBracket = \(\n    teams: TeamTournamentTeam\[\],\n    fixtures: TeamTournamentFixture\[\],\n    matchdays: TeamTournamentMatchday\[\]\n\) => \{",
    "const renderTeamTournamentEliminationBracket = (\n    teams: TeamTournamentTeam[],\n    fixtures: TeamTournamentFixture[],\n    matchdays: TeamTournamentMatchday[],\n    config?: TeamTournamentConfig | null\n) => {",
    content
)

content = re.sub(
    r"const \{ getFixtureSummary, resolveFixtureName \} = buildTeamTournamentFixtureContext\(teams, fixtures, matchdays\);",
    "const { getFixtureSummary, resolveFixtureName } = buildTeamTournamentFixtureContext(teams, fixtures, matchdays, config);",
    content
)

# 5. Modify renderTeamTournamentEliminationCompletedFixtures to accept config
content = re.sub(
    r"const renderTeamTournamentEliminationCompletedFixtures = \(\n    teams: TeamTournamentTeam\[\],\n    fixtures: TeamTournamentFixture\[\],\n    matchdays: TeamTournamentMatchday\[\],\n    excludeTournamentDayId\?: string\n\) => \{",
    "const renderTeamTournamentEliminationCompletedFixtures = (\n    teams: TeamTournamentTeam[],\n    fixtures: TeamTournamentFixture[],\n    matchdays: TeamTournamentMatchday[],\n    excludeTournamentDayId?: string,\n    config?: TeamTournamentConfig | null\n) => {",
    content
)

content = re.sub(
    r"const \{ getFixtureSummary \} = buildTeamTournamentFixtureContext\(teams, fixtures, matchdays\);",
    "const { getFixtureSummary } = buildTeamTournamentFixtureContext(teams, fixtures, matchdays, config);",
    content
)

# 6. Fix bracket rendering using s.team1Wins in renderTeamTournamentEliminationBracket and renderTeamTournamentEliminationCompletedFixtures
content = re.sub(
    r"const t1w = swap \? s\.team2Wins : s\.team1Wins;\n\s*const t2w = swap \? s\.team1Wins : s\.team2Wins;",
    "const t1w = getTeamTournamentScoreValue(s, swap ? 'team2Wins' : 'team1Wins', config);\n\t                    const t2w = getTeamTournamentScoreValue(s, swap ? 'team1Wins' : 'team2Wins', config);",
    content
)

# 7. Modify printTeamTournamentMatchdayReport to use getTeamTournamentScoreValue
content = re.sub(
    r"const t1w = Number\.isFinite\(Number\(s\.team1Wins\)\) \? Number\(s\.team1Wins\) : '';\n\s*const t2w = Number\.isFinite\(Number\(s\.team2Wins\)\) \? Number\(s\.team2Wins\) : '';\n\s*const t1p = Number\.isFinite\(Number\(s\.team1Points\)\) \? Number\(s\.team1Points\) : '';\n\s*const t2p = Number\.isFinite\(Number\(s\.team2Points\)\) \? Number\(s\.team2Points\) : '';",
    "const t1w = getTeamTournamentScoreValue(s, 'team1Wins', config);\n\t            const t2w = getTeamTournamentScoreValue(s, 'team2Wins', config);\n\t            const t1p = t1w;\n\t            const t2p = t2w;",
    content
)

# 8. Modify printTeamTournamentReport to pass config down to bracket functions
content = re.sub(
    r"const bracketHtml = renderTeamTournamentEliminationBracket\(teams, fixtures, matchdays\);",
    "const bracketHtml = renderTeamTournamentEliminationBracket(teams, fixtures, matchdays, config);",
    content
)

content = re.sub(
    r"const reminderHtml = renderTeamTournamentEliminationCompletedFixtures\(teams, fixtures, allMatchdays, matchday\.id\);",
    "const reminderHtml = renderTeamTournamentEliminationCompletedFixtures(teams, fixtures, allMatchdays, matchday.id, config);",
    content
)


with open('services/printService.ts', 'w') as f:
    f.write(content)
