import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple
from collections import Counter

class ContentType(Enum):
    URL = "url"
    EMAIL = "email"
    CODE_BLOCK = "code_block"
    INLINE_CODE = "inline_code"
    FILE_PATH = "file_path"
    JSON = "json"
    IDENTIFIER = "identifier"
    VERSION = "version"
    HASH = "hash"
    QUOTED = "quoted"

class PatternDetector:
    PATTERNS = {
        ContentType.URL: r'https?://[^\s<>"{}|\\^`\[\]]+',
        ContentType.EMAIL: r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        ContentType.CODE_BLOCK: r'```[\s\S]*?```',
        ContentType.INLINE_CODE: r'`[^`\n]+`',
        ContentType.FILE_PATH: r'(?:/[a-zA-Z0-9_.-]+)+/?|(?:[A-Z]:\\(?:[^\\/*?"<>|\r\n]+\\)*[^\\/*?"<>|\r\n]*)',
        ContentType.JSON: r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',
        ContentType.IDENTIFIER: r'\b[a-z]+(?:[A-Z][a-z]*){2,}\b|\b[a-z]+(?:_[a-z]+){2,}\b',
        ContentType.VERSION: r'\b\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+)?\b',
        ContentType.HASH: r'\b[a-f0-9]{32,64}\b',
        ContentType.QUOTED: r'"[^"]{20,}"',
    }

    def __init__(self, min_length: int = 15):
        self.min_length = min_length
        self.compiled_patterns = {
            ctype: re.compile(pattern)
            for ctype, pattern in self.PATTERNS.items()
        }

    def detect_all(self, text: str) -> List[Tuple[ContentType, int, int, str]]:
        matches = []
        for content_type, pattern in self.compiled_patterns.items():
            for match in pattern.finditer(text):
                content = match.group()
                if len(content) >= self.min_length:
                    matches.append((content_type, match.start(), match.end(), content))
        matches.sort(key=lambda x: (x[1], -x[2]))
        return self._remove_overlaps(matches)

    def _remove_overlaps(self, matches: List[Tuple]) -> List[Tuple]:
        if not matches:
            return []
        filtered = [matches[0]]
        for match in matches[1:]:
            last_end = filtered[-1][2]
            current_start = match[1]
            if current_start >= last_end:
                filtered.append(match)
        return filtered