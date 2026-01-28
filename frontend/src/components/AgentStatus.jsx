import React from 'react';

const AgentStatus = ({ step, status }) => {
    // steps: 'idle', 'generating', 'reviewing', 'refining', 'complete'

    const steps = [
        { id: 'generating', label: 'Generator Agent', icon: '⚡' },
        { id: 'reviewing', label: 'Reviewer Agent', icon: '🔍' },
        { id: 'complete', label: 'Final Output', icon: '✨' },
    ];

    const getStepStatus = (stepId) => {
        if (step === 'idle') return 'pending';
        if (step === stepId) return 'active';

        const stepOrder = ['generating', 'reviewing', 'refining', 'complete'];
        const currentIndex = stepOrder.indexOf(step);
        const stepIndex = stepOrder.indexOf(stepId);

        return currentIndex > stepIndex ? 'completed' : 'pending';
    };

    return (
        <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            {steps.map((s, index) => {
                const stepStatus = getStepStatus(s.id);
                const isActive = stepStatus === 'active';
                const isCompleted = stepStatus === 'completed';

                return (
                    <div key={s.id} style={{ display: 'flex', alignItems: 'center', opacity: stepStatus === 'pending' ? 0.4 : 1, flex: 1 }}>
                        <div style={{
                            width: '40px',
                            height: '40px',
                            borderRadius: '50%',
                            background: isActive ? 'var(--primary)' : (isCompleted ? 'var(--success)' : 'rgba(255,255,255,0.1)'),
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: '1.2rem',
                            marginRight: '1rem',
                            boxShadow: isActive ? '0 0 15px var(--primary)' : 'none',
                            transition: 'all 0.3s ease'
                        }}>
                            {isCompleted ? '✓' : s.icon}
                        </div>
                        <div>
                            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Step {index + 1}</div>
                            <div style={{ fontWeight: 600 }}>{s.label}</div>
                        </div>
                        {index < steps.length - 1 && (
                            <div style={{ height: '2px', background: 'var(--surface-border)', flex: 1, margin: '0 1rem' }} />
                        )}
                    </div>
                );
            })}
        </div>
    );
};

export default AgentStatus;
