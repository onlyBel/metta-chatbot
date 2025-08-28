from typing import List, Tuple, Dict, Any, Optional

Triple = Tuple[str, str, str]

class MettaEmulator:
    def __init__(self):
        self.triples: List[Triple] = []
        self.provenance: Dict[Triple, Dict[str, Any]] = {}

    def assert_fact(self, s: str, p: str, o: str, source: Optional[str] = None):
        t = (s.strip(), p.strip(), o.strip())
        if t not in self.triples:
            self.triples.append(t)
            if source:
                self.provenance[t] = {"source": source}

    def query(self, s=None, p=None, o=None) -> List[Triple]:
        results = []
        for (a, b, c) in self.triples:
            if (s is None or s == a) and (p is None or p == b) and (o is None or o == c):
                results.append((a, b, c))
        return results

    def run_inference_once(self) -> List[Triple]:
        """
        Rule: contains(Herb, Compound) & contraindicated_with(Compound, Med)
              -> contraindicated_with(Herb, Med)
        """
        new_facts = []
        for herb, _, compound in self.query(p='contains'):
            for cmpd, _, med in self.query(s=compound, p='contraindicated_with'):
                derived = (herb, 'contraindicated_with', med)
                if derived not in self.triples and derived not in new_facts:
                    self.provenance[derived] = {
                        "derived_from": [(herb, 'contains', compound), (compound, 'contraindicated_with', med)],
                        "sources": [
                            self.provenance.get((herb,'contains',compound),{}).get("source"),
                            self.provenance.get((compound,'contraindicated_with',med),{}).get("source")
                        ]
                    }
                    new_facts.append(derived)
        for f in new_facts:
            self.triples.append(f)
        return new_facts

    def all_facts(self):
        return [{"triple": t, "meta": self.provenance.get(t, {})} for t in self.triples]

