import React from 'react';

const ResultCard = ({ data }) => {
    if (!data) return null;

    const { original_content, feedback, refined_content, final_status } = data;
    const contentToShow = refined_content || original_content;
    const isRefined = !!refined_content;

    return (
        <div className="fade-in">
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 350px', gap: '2rem' }}>

                {/* Main Content Area */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>

                    <div className="glass-panel" style={{ padding: '2rem', borderTop: `4px solid ${isRefined ? 'var(--secondary)' : 'var(--primary)'}` }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                            <h3 style={{ fontSize: '1.2rem' }}>Generated Content</h3>
                            {isRefined && <span style={{ background: 'var(--secondary)', padding: '0.25rem 0.75rem', borderRadius: '20px', fontSize: '0.8rem' }}>Refined Version</span>}
                        </div>

                        <p style={{ lineHeight: '1.6', fontSize: '1.1rem', marginBottom: '2rem' }}>
                            {contentToShow.explanation}
                        </p>

                        <h4 style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>Assessment (MCQs)</h4>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            {contentToShow.mcqs.map((mcq, idx) => (
                                <div key={idx} style={{ background: 'rgba(0,0,0,0.2)', padding: '1.5rem', borderRadius: '12px' }}>
                                    <p style={{ marginBottom: '1rem', fontWeight: 500 }}>{idx + 1}. {mcq.question}</p>
                                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                                        {mcq.options.map((opt, optIdx) => (
                                            <div key={optIdx} style={{
                                                padding: '0.75rem',
                                                background: opt.startsWith(mcq.answer) ? 'rgba(16, 185, 129, 0.2)' : 'rgba(255,255,255,0.05)',
                                                border: opt.startsWith(mcq.answer) ? '1px solid var(--success)' : '1px solid transparent',
                                                borderRadius: '8px',
                                                fontSize: '0.9rem'
                                            }}>
                                                {opt}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                </div>

                {/* Sidebar: Reviewer Feedback */}
                <div className="glass-panel" style={{ padding: '1.5rem', height: 'fit-content' }}>
                    <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center' }}>
                        Reviewer Agent
                        <span style={{
                            marginLeft: 'auto',
                            fontSize: '0.8rem',
                            padding: '0.25rem 0.75rem',
                            borderRadius: '12px',
                            background: final_status === 'pass' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                            color: final_status === 'pass' ? 'var(--success)' : 'var(--error)'
                        }}>
                            {final_status.toUpperCase()}
                        </span>
                    </h3>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        {feedback.feedback && feedback.feedback.length > 0 ? (
                            feedback.feedback.map((item, idx) => (
                                <div key={idx} style={{
                                    padding: '1rem',
                                    background: 'rgba(239, 68, 68, 0.1)',
                                    borderLeft: '3px solid var(--error)',
                                    borderRadius: '0 8px 8px 0',
                                    fontSize: '0.9rem'
                                }}>
                                    {item}
                                </div>
                            ))
                        ) : (
                            <div style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                                No issues found. Perfect match!
                            </div>
                        )}
                    </div>

                    <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--surface-border)' }}>
                        <small style={{ color: 'var(--text-muted)' }}>
                            {isRefined ? "The generator automatically refined the content based on this feedback." : "Content passed review criteria."}
                        </small>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default ResultCard;
