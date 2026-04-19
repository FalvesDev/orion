import React, { useState, useEffect, useCallback } from 'react';

let _addToast = null;

export function showToast(msg, type = 'info') {
    if (_addToast) {
        _addToast(msg, type);
    }
}

const COLORS = {
    success: {
        border: 'border-green-500/60',
        bg: 'bg-green-500/10',
        text: 'text-green-300',
        dot: 'bg-green-400',
    },
    error: {
        border: 'border-red-500/60',
        bg: 'bg-red-500/10',
        text: 'text-red-300',
        dot: 'bg-red-400',
    },
    info: {
        border: 'border-cyan-500/60',
        bg: 'bg-cyan-500/10',
        text: 'text-cyan-300',
        dot: 'bg-cyan-400',
    },
};

let _nextId = 0;

const ToastItem = ({ toast, onRemove }) => {
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        // Trigger fade-in on next tick
        const inTimer = requestAnimationFrame(() => setVisible(true));

        // Start fade-out at 2.6s so it completes by 3s
        const outTimer = setTimeout(() => setVisible(false), 2600);

        // Remove from DOM after fade-out completes
        const removeTimer = setTimeout(() => onRemove(toast.id), 3000);

        return () => {
            cancelAnimationFrame(inTimer);
            clearTimeout(outTimer);
            clearTimeout(removeTimer);
        };
    }, [toast.id, onRemove]);

    const colors = COLORS[toast.type] || COLORS.info;

    return (
        <div
            className={`
                flex items-start gap-3 px-4 py-3 rounded-xl border backdrop-blur-xl shadow-2xl
                transition-all duration-300 ease-in-out pointer-events-auto
                ${colors.border} ${colors.bg}
                ${visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'}
            `}
            style={{ minWidth: '260px', maxWidth: '360px' }}
        >
            <div className={`mt-1 w-2 h-2 rounded-full shrink-0 ${colors.dot} shadow-[0_0_6px_currentColor]`} />
            <span className={`text-sm font-mono leading-snug ${colors.text}`}>{toast.msg}</span>
            <button
                onClick={() => onRemove(toast.id)}
                className="ml-auto text-gray-500 hover:text-gray-300 transition-colors text-xs shrink-0"
            >
                ✕
            </button>
        </div>
    );
};

const ToastContainer = () => {
    const [toasts, setToasts] = useState([]);

    const addToast = useCallback((msg, type = 'info') => {
        const id = _nextId++;
        setToasts(prev => [...prev, { id, msg, type }]);
    }, []);

    const removeToast = useCallback((id) => {
        setToasts(prev => prev.filter(t => t.id !== id));
    }, []);

    useEffect(() => {
        _addToast = addToast;
        // Expose globally for use outside React tree
        window.showToast = addToast;
        return () => {
            _addToast = null;
            delete window.showToast;
        };
    }, [addToast]);

    if (toasts.length === 0) return null;

    return (
        <div
            className="fixed bottom-6 right-6 z-[999] flex flex-col gap-2 pointer-events-none"
            aria-live="polite"
            aria-label="Notifications"
        >
            {toasts.map(toast => (
                <ToastItem key={toast.id} toast={toast} onRemove={removeToast} />
            ))}
        </div>
    );
};

export default ToastContainer;
