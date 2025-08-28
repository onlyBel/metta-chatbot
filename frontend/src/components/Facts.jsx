import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export default function Facts() {
  const [facts, setFacts] = useState([]);

  useEffect(() => {
    axios.get(`${API_URL}/all_facts`).then(r => setFacts(r.data.facts));
  }, []);

  return (
    <div>
      <h2 className="font-semibold mb-2">Knowledge Graph Facts</h2>
      <ul className="list-disc pl-5">
        {facts.map((f,i) => (
          <li key={i}>{f.triple[0]} --{f.triple[1]}--> {f.triple[2]}</li>
        ))}
      </ul>
    </div>
  );
}

