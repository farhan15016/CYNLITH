import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function parseLesson(rawLesson) {
  if (!rawLesson) return null;

  if (typeof rawLesson === "object") {
    return rawLesson;
  }

  try {
    return JSON.parse(rawLesson);
  } catch {
    return {
      explanation: rawLesson,
    };
  }
}

function parseEvaluation(rawEvaluation) {
  if (!rawEvaluation) {
    return {
      result: "Evaluated",
      feedback: "",
      hint: "",
    };
  }

  const feedback = String(rawEvaluation);

  const resultMatch = feedback.match(
    /Result:\s*(Correct|Partially Correct|Incorrect)/i
  );

  const feedbackMatch = feedback.match(
    /Feedback:\s*([\s\S]*?)(?=\nHint:|$)/i
  );

  const hintMatch = feedback.match(
    /Hint:\s*([\s\S]*)/i
  );

  return {
    result: resultMatch ? resultMatch[1] : "Evaluated",
    feedback: feedbackMatch
      ? feedbackMatch[1].trim()
      : feedback,
    hint: hintMatch ? hintMatch[1].trim() : "",
  };
}

function App() {
  const [subject, setSubject] = useState("");
  const [topic, setTopic] = useState("");
  const [level, setLevel] = useState("Beginner");
  const [mode, setMode] = useState("STANDARD");

  const [started, setStarted] = useState(false);
  const [lessonStarted, setLessonStarted] = useState(false);

  const [session, setSession] = useState(null);
  const [lesson, setLesson] = useState(null);

  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState(null);
  const [evaluating, setEvaluating] = useState(false);

  const [error, setError] = useState("");

  const startLearning = async () => {
    if (!subject.trim() || !topic.trim()) {
      setError("Please enter a subject and topic.");
      return;
    }

    setError("");

    try {
      const response = await fetch(`${API_URL}/study-session`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subject,
          topic,
          level,
          mode,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to create study session");
      }

      const data = await response.json();

      setSession(data.session || null);
      setLesson(parseLesson(data.lesson));
      setStarted(true);
      setLessonStarted(false);
      setEvaluation(null);
      setAnswer("");
    } catch (err) {
      console.error(err);
      setError(
        "Could not connect to Cynthia. Make sure the backend is running."
      );
    }
  };

  const beginLesson = () => {
    setLessonStarted(true);

    setTimeout(() => {
      const lessonElement = document.getElementById("lesson-content");

      if (lessonElement) {
        lessonElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    }, 100);
  };

  const submitAnswer = async () => {
    if (!answer.trim()) {
      setError("Write an answer before checking it.");
      return;
    }

    setError("");
    setEvaluating(true);

    try {
      const question =
        lesson?.quick_check ||
        "Explain the main idea of this topic.";

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
          question,
          answer,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to evaluate answer");
      }

      const data = await response.json();

      setEvaluation({
        ...data,
        parsed: parseEvaluation(data.evaluation),
      });
    } catch (err) {
      console.error(err);
      setError("Cynthia could not evaluate the answer.");
    } finally {
      setEvaluating(false);
    }
  };

  const continueLearning = () => {
    if (!evaluation?.next_question) return;

    setLesson((previousLesson) => ({
      ...previousLesson,
      quick_check: evaluation.next_question,
    }));

    setAnswer("");
    setEvaluation(null);

    setTimeout(() => {
      const quickCheck = document.querySelector(".quick-check-card");

      if (quickCheck) {
        quickCheck.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      }
    }, 100);
  };

  const startOver = () => {
    setStarted(false);
    setLessonStarted(false);
    setSession(null);
    setLesson(null);
    setEvaluation(null);
    setAnswer("");
    setError("");
    setSubject("");
    setTopic("");
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
        {/* ERROR */}
        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {/* START SCREEN */}
        {!started && (
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

              <button
                className="start-button"
                onClick={startLearning}
              >
                Start Learning →
              </button>
            </div>
          </section>
        )}

        {/* STUDY SCREEN */}
        {started && (
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
              <div className="cynthia-avatar">C</div>

              <div>
                <p className="eyebrow">CYNTHIA</p>

                <h2>
                  Let's learn this together.
                </h2>

                <p>
                  Your personalized study session is ready.
                  Cynthia will explain the topic and then check
                  whether you really understood it.
                </p>

                <button
                  className="continue-button"
                  onClick={beginLesson}
                >
                  {lessonStarted
                    ? "Lesson Started ✓"
                    : "Begin Lesson →"}
                </button>
              </div>
            </div>

            {/* SESSION INFORMATION */}
            {session && (
              <div className="session-summary">
                <p className="eyebrow">SESSION</p>

                <p>
                  Cynthia is adapting this learning session
                  to your level.
                </p>
              </div>
            )}

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
                    <div className="section-icon">💡</div>

                    <div>
                      <h3>Core Idea</h3>

                      <p>{lesson.core_idea}</p>
                    </div>
                  </div>
                )}

                {/* EXPLANATION */}
                {lesson.explanation && (
                  <div className="lesson-section">
                    <div className="section-icon">🧠</div>

                    <div>
                      <h3>Let's Understand It</h3>

                      <p>{lesson.explanation}</p>
                    </div>
                  </div>
                )}

                {/* EXAMPLE */}
                {lesson.example && (
                  <div className="lesson-section example-section">
                    <div className="section-icon">🎯</div>

                    <div>
                      <h3>Example</h3>

                      <p>{lesson.example}</p>
                    </div>
                  </div>
                )}

                {/* EQUATION */}
                {lesson.equation && (
                  <div className="equation-card">
                    <div className="section-icon">📐</div>

                    <div>
                      <h3>Key Equation</h3>

                      <div className="equation">
                        {lesson.equation}
                      </div>
                    </div>
                  </div>
                )}

                {/* VISUAL */}
                {lesson.visual?.needed && (
                  <div className="visual-card">
                    <div className="section-icon">👀</div>

                    <div>
                      <h3>
                        {lesson.visual.title ||
                          "Visual Explanation"}
                      </h3>

                      <p>
                        {lesson.visual.description ||
                          "Cynthia recommends a visual explanation for this concept."}
                      </p>

                      {lesson.visual.labels?.length > 0 && (
                        <div className="visual-labels">
                          {lesson.visual.labels.map(
                            (label, index) => (
                              <span key={index}>
                                {label}
                              </span>
                            )
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* VIDEO */}
                {lesson.video?.needed && (
                  <div className="media-card">
                    <div className="section-icon">🎥</div>

                    <div>
                      <h3>Video Learning Recommended</h3>

                      <p>
                        {lesson.video.description ||
                          "A video could help reinforce this concept."}
                      </p>

                      <span className="media-status">
                        Video learning recommended
                      </span>
                    </div>
                  </div>
                )}

                {/* QUICK CHECK */}
                {lesson.quick_check && (
                  <div className="quick-check-card">
                    <div className="quick-check-icon">
                      🎯
                    </div>

                    <div>
                      <p className="eyebrow">
                        TEST YOUR UNDERSTANDING
                      </p>

                      <h3>Quick Check</h3>

                      <p className="question">
                        {lesson.quick_check}
                      </p>

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
                    </div>
                  </div>
                )}

                {/* EVALUATION */}
                {evaluation && (
                  <div className="evaluation-card">
                    <p className="eyebrow">
                      CYNTHIA'S FEEDBACK
                    </p>

                    {/* RESULT */}
                    <div
                      className={`evaluation-result ${evaluation.parsed.result
                        .toLowerCase()
                        .replaceAll(" ", "-")}`}
                    >
                      <span className="evaluation-result-icon">
                        {evaluation.parsed.result
                          .toLowerCase()
                          .includes("correct") &&
                        !evaluation.parsed.result
                          .toLowerCase()
                          .includes("incorrect")
                          ? "✅"
                          : evaluation.parsed.result
                              .toLowerCase()
                              .includes("partial")
                          ? "🟡"
                          : "❌"}
                      </span>

                      <div>
                        <span className="evaluation-result-label">
                          Result
                        </span>

                        <strong>
                          {evaluation.parsed.result}
                        </strong>
                      </div>
                    </div>

                    {/* FEEDBACK */}
                    {evaluation.parsed.feedback && (
                      <div className="feedback-section">
                        <h4>💬 Cynthia's Feedback</h4>

                        <p>
                          {evaluation.parsed.feedback}
                        </p>
                      </div>
                    )}

                    {/* HINT */}
                    {evaluation.parsed.hint &&
                      evaluation.parsed.hint !== "..." && (
                        <div className="hint-section">
                          <h4>💡 Hint</h4>

                          <p>
                            {evaluation.parsed.hint}
                          </p>
                        </div>
                      )}

                    {/* LEARNING STATUS */}
                    {evaluation.learning_status && (
                      <div className="learning-status">
                        <span className="status-label">
                          📈 Learning Status
                        </span>

                        <strong>
                          {evaluation.learning_status}
                        </strong>
                      </div>
                    )}

                    {/* NEXT ACTION */}
                    {evaluation.next_action && (
                      <div className="next-action">
                        <span className="status-label">
                          🎯 Cynthia's Recommendation
                        </span>

                        <p>
                          {evaluation.next_action}
                        </p>
                      </div>
                    )}

                    {/* NEXT QUESTION */}
                    {evaluation.next_question && (
                      <div className="next-question-card">
                        <div>
                          <span className="status-label">
                            🚀 Ready for the next challenge?
                          </span>

                          <p>
                            Cynthia has adapted the next
                            question based on your
                            performance.
                          </p>
                        </div>

                        <button
                          className="continue-button"
                          onClick={continueLearning}
                        >
                          Continue Learning →
                        </button>
                      </div>
                    )}
                  </div>
                )}

                {/* START ANOTHER TOPIC */}
                <button
                  className="secondary-button"
                  onClick={startOver}
                >
                  ← Start Another Topic
                </button>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
