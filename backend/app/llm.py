import os
import openai
from .kg import Triple, MettaEmulator

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
USE_OPENAI = bool(OPENAI_KEY)

if USE_OPENAI:
    openai.api_key = OPENAI_KEY

def format_facts_for_prompt(facts: list[Triple], provenance: dict) -> str:
    lines = []
    for t in facts:
        meta = provenance.get(t, {})
        src = meta.get("source") or meta.get("sources") or "unknown"
        lines.append(f"- {t[0]} --{t[1]}--> {t[2]} (source: {src})")
    return "\n".join(lines)

def call_openai_for_answer(question: str, context_facts: list[Triple], kg: MettaEmulator):
    if not USE_OPENAI:
        return "OpenAI not configured. Set OPENAI_API_KEY in env."

    facts_text = format_facts_for_prompt(context_facts, kg.provenance)
    system = "You are a helpful herbal knowledge assistant. Use facts to support your answers."
    user = (
        f"QUESTION: {question}\n\n"
        f"FACTS:\n{facts_text}\n\n"
        "Reply with:\n"
        "1. One sentence short answer.\n"
        "2. Explanation citing facts.\n"
        "3. Recommended next action.\n"
        "4. JSON with keys: answer, explanation, citations, recommended_action"
    )
    resp = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=[
            {"role":"system", "content":system},
            {"role":"user", "content":user}
        ],
        max_tokens=500,
        temperature=0
    )
    return resp["choices"][0]["message"]["content"]

