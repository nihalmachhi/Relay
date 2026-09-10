from __future__ import annotations

import math
import re
from collections import Counter

from .models import RetrievedExample

TOKEN = re.compile(r"[a-z0-9']+")
STOPWORDS = {"a", "an", "and", "are", "at", "for", "from", "i", "in", "is", "it", "my", "of", "on", "or", "please", "the", "to", "with", "you"}


def tokens(text: str) -> list[str]:
    return [token for token in TOKEN.findall(text.lower()) if token not in STOPWORDS]


class TfidfRetriever:
    def __init__(self, rows: list[dict[str, str]]):
        self.rows = rows
        self.document_frequency: Counter[str] = Counter()
        self.documents: list[Counter[str]] = []
        for row in rows:
            counts = Counter(tokens(row["customer_text"]))
            self.documents.append(counts)
            self.document_frequency.update(counts.keys())
        self.total_docs = len(rows)

    def _weight(self, term: str, count: int) -> float:
        return (1 + math.log(count)) * math.log((self.total_docs + 1) / (self.document_frequency[term] + 1))

    def search(self, query: str, top_k: int = 3) -> list[RetrievedExample]:
        query_counts = Counter(tokens(query))
        query_vector = {term: self._weight(term, count) for term, count in query_counts.items() if term in self.document_frequency}
        query_norm = math.sqrt(sum(value * value for value in query_vector.values()))
        matches: list[RetrievedExample] = []
        for row, document in zip(self.rows, self.documents):
            doc_vector = {term: self._weight(term, count) for term, count in document.items()}
            dot = sum(query_vector.get(term, 0.0) * value for term, value in doc_vector.items())
            doc_norm = math.sqrt(sum(value * value for value in doc_vector.values()))
            score = dot / (query_norm * doc_norm) if query_norm and doc_norm else 0.0
            matches.append(RetrievedExample(row["message_id"], row["customer_text"], row["agent_reply"], row["intent"], round(score, 4)))
        return sorted(matches, key=lambda item: item.score, reverse=True)[:top_k]
