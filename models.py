from dataclasses import dataclass

@dataclass
class SearchResult:

    found: bool

    path: list

    visited: set

    order: list