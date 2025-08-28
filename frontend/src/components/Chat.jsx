import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export default function Chat() {
  const [q, setQ] = useState("");
  const [res, setRes] = useState(null);

  const ask = async () => {
    const r = await axios.post(`${API_URL}/ask`, { question: q });
    setRes(r.data);
  };

  return (
    <div className="mb-6">
      <input
        value={q}
        onChange={e => setQ(e.target.value)}
        placeholder="Ask about herbs..."
        className="border px-2 py-1 mr-2"
      />
      <button onClick={ask} className="bg-green-600 text-white px-3 py-1 rounded">
        Ask
      </button>
      {res && (
        <div className="mt-4 border p-2">
          <pre>{JSON.stringify(res, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

