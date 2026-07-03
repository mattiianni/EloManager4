import React, { useMemo } from 'react';
import { usePadelStore } from '../hooks/usePadelStore.tsx';
import { SFIcon } from '../components/ui/SFIcon.tsx';

import PlayerProfileModal from '../components/PlayerProfileModal.tsx';
import { Player, TournamentType } from '../types.ts';
import { groupMatchesByPlayerSets } from '../services/beatTheBoxService.ts';
import { printPlayerProfiles } from '../services/printService.ts';
import { getTournamentDisplayName } from '../utils/tournamentLabels.ts';

interface DashboardPageProps {
    onNavigateToTournaments: (tournamentId: string) => void;
}

const DashboardPage: React.FC<DashboardPageProps> = ({ onNavigateToTournaments }) => {
    const { players, matches, tournaments, eloHistory, getPlayerById } = usePadelStore();
    const [profilePlayer, setProfilePlayer] = React.useState<Player | null>(null);

    const stats = useMemo(() => {
        const activePlayers = players.length;
        const totalMatches = matches.length;
        const completedTournaments = tournaments.filter(t => t.status === 'completed').length;
        let avgElo = 0;
        if (players.length > 0) {
            const sorted = [...players].sort((a, b) => b.currentElo - a.currentElo);
            const top50Count = Math.max(1, Math.floor(sorted.length / 2));
            const top50 = sorted.slice(0, top50Count);
            avgElo = top50.reduce((sum, p) => sum + p.currentElo, 0) / top50Count;
        }

        return { activePlayers, totalMatches, completedTournaments, avgElo };
    }, [players, matches, tournaments]);

    const top5 = useMemo(() => {
        const sorted = [...players].sort((a, b) => b.currentElo - a.currentElo).slice(0, 5);
        return sorted.map(p => {
            const playerHistory = eloHistory
                .filter(e => e.playerId === p.id)
                .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
            const lastDelta = playerHistory.length > 0 ? playerHistory[0].delta : 0;
            return { ...p, lastDelta };
        });
    }, [players, eloHistory]);

    const lastGiornata = useMemo(() => {
        const completed = tournaments
            .filter(t => t.status === 'completed')
            .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
        if (completed.length === 0) return null;

        const tournament = completed[0];
        const tournamentMatches = matches.filter(m => m.tournamentId === tournament.id);

        let top3: { label: string }[] = [];

        if (tournament.type === TournamentType.BeatTheBox) {
            // Beat the Box: use groupMatchesByPlayerSets to find finals
            const { phaseMatches } = groupMatchesByPlayerSets(tournamentMatches);
            const numBoxes = groupMatchesByPlayerSets(tournamentMatches).boxes.size;

            let finalMatches: typeof tournamentMatches = [];
            if (numBoxes >= 4 && phaseMatches.length >= 2) {
                // Has semifinals: first 2 are semis, rest are finals
                finalMatches = phaseMatches.slice(2);
            } else {
                finalMatches = phaseMatches;
            }

            // Finals: match[0] = 1st vs 2nd, match[1] = 3rd vs 4th
            const standings: { team: string[] }[] = [];
            if (finalMatches.length > 0 && finalMatches[0].winner) {
                const fm = finalMatches[0];
                standings.push({ team: fm.winner === 'team1' ? [...fm.team1] : [...fm.team2] }); // 1st
                standings.push({ team: fm.winner === 'team1' ? [...fm.team2] : [...fm.team1] }); // 2nd
            }
            if (finalMatches.length > 1 && finalMatches[1].winner) {
                const fm = finalMatches[1];
                standings.push({ team: fm.winner === 'team1' ? [...fm.team1] : [...fm.team2] }); // 3rd
            }

            top3 = standings.slice(0, 3).map(s => ({
                label: s.team.map(id => {
                    const p = getPlayerById(id);
                    return p ? `${p.name} ${p.surname}` : '?';
                }).join(' & ')
            }));
        } else {
            // Other tournament types: pair standings from all matches
            const pairStats = new Map<string, { wins: number; gamesWon: number; gamesLost: number; team: string[] }>();
            tournamentMatches.forEach(m => {
                if (!m.winner || m.winner === 'draw') return;
                const key1 = [...m.team1].sort().join('||');
                const key2 = [...m.team2].sort().join('||');
                if (!pairStats.has(key1)) pairStats.set(key1, { wins: 0, gamesWon: 0, gamesLost: 0, team: [...m.team1] });
                if (!pairStats.has(key2)) pairStats.set(key2, { wins: 0, gamesWon: 0, gamesLost: 0, team: [...m.team2] });

                const s1 = pairStats.get(key1)!;
                const s2 = pairStats.get(key2)!;
                m.sets.forEach(set => {
                    s1.gamesWon += set.team1;
                    s1.gamesLost += set.team2;
                    s2.gamesWon += set.team2;
                    s2.gamesLost += set.team1;
                });
                if (m.winner === 'team1') s1.wins++;
                else s2.wins++;
            });

            top3 = [...pairStats.values()]
                .sort((a, b) => b.wins - a.wins || (b.gamesWon - b.gamesLost) - (a.gamesWon - a.gamesLost))
                .slice(0, 3)
                .map(s => ({
                    label: s.team.map(id => {
                        const p = getPlayerById(id);
                        return p ? `${p.name} ${p.surname}` : '?';
                    }).join(' & ')
                }));
        }

        return {
            id: tournament.id,
            name: getTournamentDisplayName(tournament, tournaments),
            type: tournament.type,
            date: new Date(tournament.date).toLocaleDateString('it-IT'),
            club: tournament.club,
            top3,
        };
    }, [tournaments, matches, getPlayerById]);

    const recentMatches = useMemo(() => {
        const sorted = [...matches]
            .filter(m => m.winner && m.winner !== 'draw')
            .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
            .slice(0, 5);

        return sorted.map(m => {
            const t1 = m.team1.map(id => {
                const p = getPlayerById(id);
                return p ? `${p.name} ${p.surname[0]}.` : '?';
            }).join(' & ');
            const t2 = m.team2.map(id => {
                const p = getPlayerById(id);
                return p ? `${p.name} ${p.surname[0]}.` : '?';
            }).join(' & ');
            const t1Score = m.sets.reduce((sum, s) => sum + s.team1, 0);
            const t2Score = m.sets.reduce((sum, s) => sum + s.team2, 0);
            const date = new Date(m.date).toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit' });
            return { date, t1, t2, t1Score, t2Score, winner: m.winner };
        });
    }, [matches, getPlayerById]);

    const getMedalIcon = (index: number) => {
        switch (index) {
            case 0: return <SFIcon name="medal.fill" size={20} color="var(--ios-systemYellow)" />;
            case 1: return <SFIcon name="medal.fill" size={20} color="var(--ios-systemGray)" />;
            case 2: return <SFIcon name="medal.fill" size={20} color="var(--ios-systemOrange)" />;
            default: return <span className="text-[15px] font-bold text-ios-label-secondary">{index + 1}.</span>;
        }
    };

    const getTrendIcon = (delta: number) => {
        if (delta > 0) return <SFIcon name="arrow.up" size={14} color="var(--ios-systemGreen)" />;
        if (delta < 0) return <SFIcon name="arrow.down" size={14} color="var(--ios-systemRed)" />;
        return <SFIcon name="minus" size={14} color="var(--ios-systemGray)" />;
    };

    return (
        <div className="py-2 space-y-4">
            
            {/* INTESTAZIONE KPI */}
            <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
                {[
                    { label: 'Giocatori', value: stats.activePlayers, icon: 'person.2.fill', color: 'var(--ios-systemBlue)' },
                    { label: 'Partite', value: stats.totalMatches, icon: 'sportscourt', color: 'var(--ios-systemGreen)' },
                    { label: 'Giornate', value: stats.completedTournaments, icon: 'calendar', color: 'var(--ios-systemOrange)' },
                    { label: 'MEDIA ELO', value: stats.avgElo.toFixed(2), icon: 'chart.bar.fill', color: 'var(--ios-systemIndigo)' }
                ].map((kpi, idx) => (
                    <div key={idx} className="flex flex-col p-4 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-sm">
                        <div className="flex items-center gap-2 mb-2">
                            <SFIcon name={kpi.icon} size={20} color={kpi.color} />
                            <span className="text-gray-500 dark:text-gray-400 uppercase tracking-wider text-xs font-semibold">{kpi.label}</span>
                        </div>
                        <div className="text-2xl font-bold text-gray-900 dark:text-white">{kpi.value}</div>
                    </div>
                ))}
            </div>

            {/* SEZIONE TOP 5 */}
            <div className="">
                <div className="rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden bg-white dark:bg-gray-800 shadow-sm">
                    <div className="px-4 py-3 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center">
                        <span className="font-bold text-gray-900 dark:text-white">Top 5 Giocatori</span>
                        <button onClick={() => printPlayerProfiles(players.map(p => p.id), players, matches, eloHistory, tournaments)} className="flex items-center gap-1 text-sm bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 px-3 py-1.5 rounded-lg transition-colors text-gray-700 dark:text-gray-200" disabled={players.length === 0}>
                            <SFIcon name="printer" size={14} color="currentColor" />
                            Stampa
                        </button>
                    </div>
                    <div className="divide-y divide-gray-100 dark:divide-gray-700">
                        {top5.length === 0 ? (
                            <div className="p-4 text-gray-500 dark:text-gray-400 text-center">Nessun giocatore registrato</div>
                        ) : (
                            top5.map((p, i) => (
                                <div key={p.id} className="flex items-center justify-between p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer transition-colors" onClick={() => setProfilePlayer(p)}>
                                    <div className="flex items-center gap-3">
                                        <div className="w-6 flex justify-center">{getMedalIcon(i)}</div>
                                        <span className="font-semibold text-gray-900 dark:text-white">{p.name} {p.surname}</span>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <div className="flex items-center gap-2">
                                            <span className="font-bold text-sky-600 dark:text-sky-400">{p.currentElo.toFixed(2)}</span>
                                            {getTrendIcon(p.lastDelta)}
                                        </div>
                                        <SFIcon name="chevron.right" size={16} color="var(--ios-systemGray3)" />
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </div>

            {/* SEZIONE ULTIMA GIORNATA */}
            <div className="">
                <div className="rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden bg-white dark:bg-gray-800 shadow-sm">
                    <div className="px-4 py-3 border-b border-gray-100 dark:border-gray-700 font-bold text-gray-900 dark:text-white">Ultima Giornata</div>
                    <div className="divide-y divide-gray-100 dark:divide-gray-700">
                        {!lastGiornata ? (
                            <div className="p-4 text-gray-500 dark:text-gray-400 text-center">Nessuna giornata completata</div>
                        ) : (
                            <>
                                <div className="flex items-center justify-between p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer transition-colors" onClick={() => onNavigateToTournaments(lastGiornata.id)}>
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded bg-orange-500 flex items-center justify-center">
                                            <SFIcon name="trophy.fill" size={16} color="white" />
                                        </div>
                                        <div>
                                            <div className="font-semibold text-gray-900 dark:text-white">{lastGiornata.name}</div>
                                            <div className="text-sm text-gray-500 dark:text-gray-400">{lastGiornata.type} • {lastGiornata.date}</div>
                                        </div>
                                    </div>
                                    <SFIcon name="chevron.right" size={16} color="var(--ios-systemGray3)" />
                                </div>
                                {lastGiornata.top3.length > 0 && lastGiornata.top3.map((entry, i) => (
                                    <div key={i} className="flex items-center gap-3 p-4">
                                        <div className="w-6 flex justify-center">{getMedalIcon(i)}</div>
                                        <span className="font-medium text-gray-800 dark:text-gray-200">{entry.label}</span>
                                    </div>
                                ))}
                            </>
                        )}
                    </div>
                </div>
            </div>

            {/* Ultime Partite */}
            <div className="">
                <div className="rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden bg-white dark:bg-gray-800 shadow-sm">
                    <div className="px-4 py-3 border-b border-gray-100 dark:border-gray-700 font-bold text-gray-900 dark:text-white">Ultime Partite</div>
                    <div className="divide-y divide-gray-100 dark:divide-gray-700">
                        {recentMatches.length === 0 ? (
                            <div className="p-4 text-gray-500 dark:text-gray-400 text-center">Nessuna partita registrata</div>
                        ) : (
                            recentMatches.map((m, i) => (
                                <div key={i} className="flex items-center justify-between p-4 gap-2">
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
                                    <div className="flex shrink-0 items-center gap-1 font-mono text-base font-bold bg-gray-50 dark:bg-gray-900 px-3 py-1 rounded-md border border-gray-200 dark:border-gray-700">
                                        <span className={m.winner === 'team1' ? 'text-green-600 dark:text-green-400' : 'text-gray-500'}>{m.t1Score}</span>
                                        <span className="text-gray-300 dark:text-gray-600">-</span>
                                        <span className={m.winner === 'team2' ? 'text-green-600 dark:text-green-400' : 'text-gray-500'}>{m.t2Score}</span>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </div>

            <PlayerProfileModal player={profilePlayer} onClose={() => setProfilePlayer(null)} />
        </div>
    );
};

export default DashboardPage;
