from fastapi import APIRouter
from .kg import MettaEmulator
from .models import Fact, AskRequest
from .llm import call_openai_for_answer

router = APIRouter()
kg = MettaEmulator()

# seed facts
kg.assert_fact("Basil","contains","Eugenol", source="Phytochem 2022")
kg.assert_fact("Eugenol","contraindicated_with","Lithium", source="HerbalDB 2019")
kg.run_inference_once()

@router.post("/add_fact")
def add_fact(f: Fact):
    kg.assert_fact(f.subject, f.predicate, f.obj, source=f.source)
    inferred = kg.run_inference_once()
    return {"added": (f.subject, f.predicate, f.obj), "inferred": inferred}

@router.get("/query")
def query_facts(s: str|None=None, p: str|None=None, o: str|None=None):
    res = kg.query(s,p,o)
    return {"results":[{"triple":t, "meta":kg.provenance.get(t,{})} for t in res]}

@router.get("/all_facts")
def all_facts():
    return {"facts": kg.all_facts()}

@router.post("/ask")
def ask(req: AskRequest):
    words = set(w.lower().strip("?,.!") for w in req.question.split())
    related = [t for t in kg.triples if t[0].lower() in words or t[2].lower() in words]
    if not related: related = kg.triples[:20]
    llm_text = call_openai_for_answer(req.question, related, kg)
    return {"question": req.question, "facts": related, "answer": llm_text}

