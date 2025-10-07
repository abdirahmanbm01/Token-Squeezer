import hashlib
import re
from dataclasses import dataclass, field
from typing import Dict, List
from collections import Counter
from pattern_detector import PatternDetector, ContentType

@dataclass
class Placeholder:
    id: str
    original: str
    content_type: ContentType
    start_pos: int
    end_pos: int
    checksum: str

@dataclass
class CompressionResult:
    original_text: str
    compressed_text: str
    placeholders: Dict[str, Placeholder]
    original_tokens: int
    compressed_tokens: int
    savings_ratio: float
    content_type_counts: Dict[ContentType, int] = field(default_factory=dict)

class CompressionEngine:
    def __init__(self, detector: PatternDetector):
        self.detector = detector
        self.placeholder_counter = 0

    def compress(self, text: str) -> CompressionResult:
        matches = self.detector.detect_all(text)
        placeholders = {}
        compressed_text = text
        offset = 0
        content_type_counts = Counter()

        for content_type, start, end, content in matches:
            placeholder_id = f"@@P{self.placeholder_counter}@@"
            self.placeholder_counter += 1
            checksum = hashlib.sha256(content.encode()).hexdigest()[:8]

            placeholder = Placeholder(
                id=placeholder_id,
                original=content,
                content_type=content_type,
                start_pos=start - offset,
                end_pos=start - offset + len(placeholder_id),
                checksum=checksum
            )

            placeholders[placeholder_id] = placeholder
            content_type_counts[content_type] += 1

            adjusted_start = start - offset
            adjusted_end = end - offset
            compressed_text = (
                compressed_text[:adjusted_start] +
                placeholder_id +
                compressed_text[adjusted_end:]
            )
            offset += (end - start) - len(placeholder_id)

        original_tokens = self._estimate_tokens(text)
        compressed_tokens = self._estimate_tokens(compressed_text)
        savings_ratio = 1 - (compressed_tokens / original_tokens) if original_tokens > 0 else 0

        return CompressionResult(
            original_text=text,
            compressed_text=compressed_text,
            placeholders=placeholders,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            savings_ratio=savings_ratio,
            content_type_counts=dict(content_type_counts)
        )

    def _estimate_tokens(self, text: str) -> int:
        return len(text.split()) + len(re.findall(r'[^\w\s]', text))

    def reset_counter(self):
        self.placeholder_counter = 0