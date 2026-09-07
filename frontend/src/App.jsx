import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [subject, setSubject] = useState("");
  const [topic, setTopic] = useState("");
  const [level, setLevel] = useState("Beginner");
  const [mode, setMode] = useState("STANDARD");

  const [started, setStarted] = useState(false);
  const [lessonStarted, setLessonStarted] = useState(false);

  const [loading, setLoading] = useState(false);
  const [lessonLoading, setLessonLoading] = useState(false);

  const [lesson, setLesson] = useState(null);
  const [session, setSession] = useState(null);

  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState(null);
  const [evaluating, setEvaluating] = useState(false);

  const startLearning = async () => {
    if (!subject.trim() || !topic.trim()) {
      alert("Please enter a subject and topic.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/study-session`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subject: subject.trim(),
          topic: topic.trim(),
          level,
          mode,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to create study session.");
      }

      const data = await response.json();

      console.log("Study session created:", data);

      setSession(data.session);
      setLesson(data.lesson);
      setLessonStarted(false);
      setStarted(true);
    } catch (error) {
      console.error("Study session error:", error);

      alert(
        "Could not start the study session. Make sure the Cynlith backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const beginLesson = () => {
    setLessonLoading(true);

    setTimeout(() => {
      setLessonStarted(true);
      setLessonLoading(false);

      setTimeout(() => {
        const lessonElement = document.getElementById("lesson-content");

        if (lessonElement) {
          lessonElement.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      }, 100);
    }, 400);
  };

  const submitAnswer = async () => {
    if (!answer.trim()) {
      alert("Please write an answer first.");
      return;
    }

    if (!lesson?.quick_check) {
      alert("No quick-check question is available.");
      return;
    }

    setEvaluating(true);

    try {
      const response = await fetch(`${API_URL}/evaluate-answer`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subject,
          topic,
          level,
          mode,
          question: lesson.quick_check,
          answer: answer.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to evaluate answer.");
      }

      const data = await response.json();

      console.log("Answer evaluation:", data);

      setEvaluation(data);
    } catch (error) {
      console.error("Answer evaluation error:", error);

      alert(
        "Could not evaluate your answer. Make sure the Cynlith backend is running."
      );
    } finally {
      setEvaluating(false);
    }
  };

  const startOver = () => {
    setStarted(false);
    setLessonStarted(false);
    setLesson(null);
    setSession(null);
    setAnswer("");
    setEvaluation(null);
  };

  return (
    <div className="app">
      {/* NAVBAR */}

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
        {/* ================= HOME ================= */}

        {!started ? (
          <section className="welcome">
            <div className="hero-badge">
              YOUR AI LEARNING COMPANION
            </div>

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
                placeholder="e.g. Physics, Biology, Java..."
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

              <button
                className="start-button"
                onClick={startLearning}
                disabled={loading}
              >
                {loading
                  ? "Creating Lesson..."
                  : "Start Learning →"}
              </button>
            </div>
          </section>
        ) : (
          /* ================= STUDY SCREEN ================= */

          <section className="study-screen">
            {/* STUDY HEADER */}

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

            {/* CYNTHIA INTRO */}

            <div className="lesson-card">
              <div className="cynthia-avatar">
                C
              </div>

              <div>
                <p className="eyebrow">CYNTHIA</p>

                <h2>Let's learn this together.</h2>

                <p>
                  Your personalized lesson is ready.
                  Cynthia will explain the concept,
                  show examples, and check your understanding.
                </p>

                <button
                  className="continue-button"
                  onClick={beginLesson}
                  disabled={lessonLoading}
                >
                  {lessonLoading
                    ? "Opening Lesson..."
                    : "Begin Lesson →"}
                </button>
              </div>
            </div>

            {/* LESSON */}

            {lesson && lessonStarted && (
              <div
                className="lesson-content"
                id="lesson-content"
              >
                <div className="lesson-label">
                  CYNTHIA'S LESSON
                </div>

                {/* CORE IDEA */}

                {lesson.core_idea && (
                  <div className="lesson-section">
                    <div className="section-icon">
                      💡
                    </div>

                    <div>
                      <h3>Core Idea</h3>

                      <p>{lesson.core_idea}</p>
                    </div>
                  </div>
                )}

                {/* HOW IT WORKS */}

                {lesson.explanation && (
                  <div className="lesson-section">
                    <div className="section-icon">
                      📖
                    </div>

                    <div>
                      <h3>How It Works</h3>

                      <p>{lesson.explanation}</p>
                    </div>
                  </div>
                )}

                {/* REAL WORLD EXAMPLE */}

                {lesson.example && (
                  <div className="lesson-section">
                    <div className="section-icon">
                      🌎
                    </div>

                    <div>
                      <h3>Real-World Example</h3>

                      <p>{lesson.example}</p>
                    </div>
                  </div>
                )}

                {/* VISUAL EXPLANATION */}

                {lesson.visual && (
                  <div className="media-card">
                    <div className="media-icon">
                      🖼️
                    </div>

                    <div>
                      <h3>Visual Explanation</h3>

                      {typeof lesson.visual === "string" ? (
                        <p>{lesson.visual}</p>
                      ) : (
                        <>
                          <p>
                            {lesson.visual.description ||
                              "A visual explanation will help make this concept easier to understand."}
                          </p>

                          {lesson.visual.needed && (
                            <span className="media-status">
                              Visual learning recommended
                            </span>
                          )}
                        </>
                      )}
                    </div>
                  </div>
                )}

                {/* VIDEO */}

                {lesson.video && (
                  <div className="media-card">
                    <div className="media-icon">
                      🎥
                    </div>

                    <div>
                      <h3>Watch & Learn</h3>

                      {typeof lesson.video === "string" ? (
                        <p>{lesson.video}</p>
                      ) : (
                        <>
                          <p>
                            {lesson.video.description ||
                              "A short educational video can reinforce this concept."}
                          </p>

                          {lesson.video.needed && (
                            <span className="media-status">
                              Video learning recommended
                            </span>
                          )}
                        </>
                      )}
                    </div>
                  </div>
                )}

                {/* QUICK CHECK */}

                {lesson.quick_check && (
                  <div className="quick-check-card">
                    <div className="quick-check-icon">
                      🧩
                    </div>

                    <div>
                      <h3>Quick Check</h3>

                      <p>{lesson.quick_check}</p>

                      <textarea
                        className="answer-box"
                        value={answer}
                        onChange={(e) =>
                          setAnswer(e.target.value)
                        }
                        placeholder="Explain your answer in your own words..."
                        rows={5}
                      />

                      <button
                        className="continue-button"
                        onClick={submitAnswer}
                        disabled={evaluating}
                      >
                        {evaluating
                          ? "Cynthia is thinking..."
                          : "Check My Answer →"}
                      </button>

                      {/* EVALUATION */}

                      {evaluation && (
                        <div className="evaluation-card">
                          <div className="evaluation-header">
                            <span>🧠</span>

                            <strong>
                              Cynthia's Feedback
                            </strong>
                          </div>

                          <p>
                            {evaluation.evaluation}
                          </p>

                          {evaluation.learning_status && (
                            <div className="progress-badge">
                              Learning Status:{" "}
                              {evaluation.learning_status}
                            </div>
                          )}

                          {evaluation.next_action && (
                            <p className="next-action">
                              <strong>Next:</strong>{" "}
                              {evaluation.next_action}
                            </p>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* START OVER */}

            <button
              className="back-button"
              onClick={startOver}
            >
              ← Choose another topic
            </button>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
