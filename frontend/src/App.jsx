import { useState } from "react";
import "./App.css";

function App() {
  const [subject, setSubject] = useState("");
  const [topic, setTopic] = useState("");
  const [level, setLevel] = useState("Beginner");
  const [mode, setMode] = useState("STANDARD");
  const [started, setStarted] = useState(false);

  const startLearning = () => {
    if (!subject.trim() || !topic.trim()) return;
    setStarted(true);
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">C</div>
          <span>Cynlith</span>
        </div>

        <div className="nav-status">
          <span>🔥 0 day streak</span>
          <span>⭐ 0 XP</span>
        </div>
      </header>

      <main className="main-content">
        {!started ? (
          <section className="welcome">
            <div className="hero-badge">YOUR AI LEARNING COMPANION</div>

            <h1>
              Learn anything.
              <br />
              <span>Understand everything.</span>
            </h1>

            <p className="subtitle">
              Cynthia adapts to your level, teaches step-by-step,
              and helps you actually understand what you study.
            </p>

            <div className="learning-card">
              <h2>What do you want to learn?</h2>

              <label>Subject</label>
              <input
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="e.g. Physics, Java, Biology..."
              />

              <label>Topic</label>
              <input
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g. Newton's Second Law"
              />

              <div className="options">
                <div>
                  <label>Level</label>
                  <select
                    value={level}
                    onChange={(e) => setLevel(e.target.value)}
                  >
                    <option>Beginner</option>
                    <option>Intermediate</option>
                    <option>Advanced</option>
                  </select>
                </div>

                <div>
                  <label>Teaching mode</label>
                  <select
                    value={mode}
                    onChange={(e) => setMode(e.target.value)}
                  >
                    <option value="SIMPLE">Simple</option>
                    <option value="STANDARD">Standard</option>
                    <option value="HARDCORE">Hardcore</option>
                  </select>
                </div>
              </div>

              <button className="start-button" onClick={startLearning}>
                Start Learning →
              </button>
            </div>
          </section>
        ) : (
          <section className="study-screen">
            <div className="study-header">
              <div>
                <p className="eyebrow">{subject}</p>
                <h1>{topic}</h1>
              </div>

              <div className="session-info">
                <span>{level}</span>
                <span>{mode}</span>
              </div>
            </div>

            <div className="lesson-card">
              <div className="cynthia-avatar">C</div>

              <div>
                <p className="eyebrow">CYNTHIA</p>
                <h2>Let's learn this together.</h2>
                <p>
                  Your study session is ready. Cynthia will explain the
                  core idea, give examples, and check your understanding.
                </p>

                <button className="continue-button">
                  Begin Lesson →
                </button>
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
