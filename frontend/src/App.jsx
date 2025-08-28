import React from "react";
import Chat from "./components/Chat";
import Facts from "./components/Facts";

export default function App() {
  return (
    <div className="p-4 font-sans">
      <h1 className="text-2xl font-bold mb-4">🌿 Metta Chatbot</h1>
      <Chat />
      <Facts />
    </div>
  )
}
