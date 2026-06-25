
import React from 'react';

interface CardProps {
    children: React.ReactNode;
    className?: string;
    title?: React.ReactNode;
    bodyClassName?: string;
}

const Card: React.FC<CardProps> = ({ children, className = '', title, bodyClassName = '' }) => {
    return (
        <div className={`hig-list-section ${className}`} style={{ marginBottom: '35px' }}>
            {title && (
                typeof title === 'string' ? (
                    <div
                        style={{
                            font: '400 13px/18px -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif',
                            color: 'var(--ios-secondaryLabel)',
                            textTransform: 'uppercase',
                            padding: '8px 20px 6px',
                            letterSpacing: '0.02em',
                        }}
                    >
                        {title}
                    </div>
                ) : (
                    <div className="px-4 py-3 md:px-5">
                        {title}
                    </div>
                )
            )}
            
            {children && (
                <div
                    className={bodyClassName}
                    style={{
                        background: 'var(--ios-secondarySystemGroupedBackground)',
                        borderRadius: '10px',
                        overflow: 'hidden',
                        margin: '0 16px',
                        boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
                    }}
                >
                    <div className="p-4 md:p-5">
                        {children}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Card;
