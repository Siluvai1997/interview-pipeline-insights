
import re

def _normalize(text: str):
    return re.findall(r"[A-Za-z0-9+#/.]+", text.lower())

def _extract_keywords(text: str):
    words = _normalize(text)
    stop = {"and","or","the","a","to","with","in","of","for","we","are","seeking","nice","have","basics"}
    return set([w for w in words if w not in stop and len(w) > 2])

def score_candidate(skills_str: str, jd_text: str) -> float:
    jd_keys = _extract_keywords(jd_text)
    cand = _extract_keywords(skills_str.replace(";", " "))
    if not jd_keys:
        return 0.0
    overlap = len(jd_keys.intersection(cand))
    return round(overlap / len(jd_keys) * 100, 2)
