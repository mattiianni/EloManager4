import React from 'react';
import ThemeToggle from '../ui/ThemeToggle.tsx';
import { useAuth } from '../../hooks/useAuth.tsx';
import { APP_MONTH, APP_VERSION } from '../../constants.ts';

interface HeaderProps {
    toggleSidebar: () => void;
    theme: 'light' | 'dark';
    toggleTheme: () => void;
}

const Header: React.FC<HeaderProps> = ({ toggleSidebar, theme, toggleTheme }) => {
    const { logout, workspace } = useAuth();

    return (
        <header 
            className="sticky top-0 z-20 flex items-center justify-between px-4"
            style={{
                height: 'calc(54px + env(safe-area-inset-top, 0px))', // Slightly taller to accommodate subtitle
                paddingTop: 'env(safe-area-inset-top, 0px)',
                background: 'var(--ios-thickMaterial)',
                backdropFilter: 'blur(40px)',
                WebkitBackdropFilter: 'blur(40px)',
                borderBottom: '0.5px solid var(--ios-separator)',
            }}
        >
            {/* Left Action (Sidebar Toggle on Mobile) */}
            <div className="flex flex-1 justify-start">
                <button
                    onClick={toggleSidebar}
                    className="flex items-center justify-center text-ios-blue md:hidden focus:outline-none"
                    aria-label="Toggle sidebar"
                >
                    <span className="material-symbols-outlined text-[24px]" style={{ fontVariationSettings: "'wght' 400" }}>menu</span>
                </button>
            </div>

            {/* Center Title & Subtitle */}
            <div className="flex-[2] flex flex-col items-center justify-center text-center">
                <h1 className="sf-headline text-ios-label truncate w-full" style={{ fontSize: '20px', lineHeight: '24px' }}>
                    Padel Elo Manager
                </h1>
                <div className="sf-caption2 text-ios-label-secondary truncate w-full mt-0.5" style={{ fontSize: '11px', lineHeight: '13px' }}>
                    v{APP_VERSION} / {APP_MONTH}{workspace ? ` • ${workspace.name}` : ''}
                </div>
            </div>

            {/* Right Actions */}
            <div className="flex flex-1 justify-end items-center gap-3">
                <ThemeToggle theme={theme} onToggle={toggleTheme} />
                <button
                    onClick={logout}
                    className="flex items-center justify-center text-ios-blue focus:outline-none"
                    title="Esci"
                    aria-label="Logout"
                >
                    <span className="material-symbols-outlined text-[22px]">logout</span>
                </button>
            </div>
        </header>
    );
};

export default Header;
