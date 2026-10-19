import { useState } from "react";
import { getRecommendations } from "./api.js";

export default function App() {
  const [userId, setUserId] = useState("42");
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [shownFor, setShownFor] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await getRecommendations(userId);
      setRecs(data.recommendations);
      setShownFor(data.user_id);
    } catch (err) {
      setError(err.message);
      setRecs([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="card">
      <h1>Movie recommendations</h1>
      <p className="subtitle">Enter a user ID (1 to 943) to see suggested titles</p>

      <form onSubmit={handleSubmit} className="row">
        <input
          type="number"
          min="1"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="e.g. 42"
        />
        <button type="submit" disabled={loading || !userId}>
          {loading ? "Loading..." : "Get picks"}
        </button>
      </form>

      {loading && (
        <p className="note">
          The first request can take up to 30 seconds while the server wakes up.
        </p>
      )}
      {error && <p className="error">{error}</p>}

      {recs.length > 0 && (
        <section>
          <h2>Top picks for user {shownFor}</h2>
          <ol className="list">
            {recs.map((r, i) => (
              <li key={r.item_id}>
                <span className="rank">{i + 1}</span>
                <span className="title">{r.title}</span>
                <span className="score">{r.score.toFixed(2)}</span>
              </li>
            ))}
          </ol>
        </section>
      )}
    </main>
  );
}