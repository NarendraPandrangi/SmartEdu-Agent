import React, { useState } from 'react';

const InputForm = ({ onSubmit, isLoading }) => {
    const [grade, setGrade] = useState(4);
    const [topic, setTopic] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (topic.trim()) {
            onSubmit({ grade: parseInt(grade), topic });
        }
    };

    return (
        <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem' }}>
            <h2 style={{ marginBottom: '1.5rem', fontSize: '1.5rem', background: 'linear-gradient(to right, #6366f1, #ec4899)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                Generate Educational Content
            </h2>
            <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: 'min-content 1fr auto', gap: '1rem', alignItems: 'end' }}>
                <div>
                    <label htmlFor="grade">Grade Level</label>
                    <input
                        id="grade"
                        type="number"
                        min="1"
                        max="12"
                        value={grade}
                        onChange={(e) => setGrade(e.target.value)}
                        className="input-field"
                        style={{ width: '100px' }}
                    />
                </div>
                <div>
                    <label htmlFor="topic">Topic</label>
                    <input
                        id="topic"
                        type="text"
                        placeholder="e.g. Photosynthesis, Ancient Rome, Fractions"
                        value={topic}
                        onChange={(e) => setTopic(e.target.value)}
                        className="input-field"
                    />
                </div>
                <button type="submit" className="btn" disabled={isLoading || !topic.trim()} style={{ height: '46px' }}>
                    {isLoading ? 'Processing...' : 'Start Agents'}
                </button>
            </form>
        </div>
    );
};

export default InputForm;
