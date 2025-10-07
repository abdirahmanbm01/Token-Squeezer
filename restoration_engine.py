import hashlib
from typing import Dict, Tuple, List
from compression_engine import Placeholder, CompressionResult

class RestorationEngine:
    @staticmethod
    def restore(compressed_text: str, placeholders: Dict[str, Placeholder]) -> Tuple[str, bool, List[str]]:
        restored_text = compressed_text
        integrity_passed = True
        errors = []

        for placeholder_id, placeholder in placeholders.items():
            if placeholder_id in restored_text:
                restored_text = restored_text.replace(placeholder_id, placeholder.original)
                current_checksum = hashlib.sha256(placeholder.original.encode()).hexdigest()[:8]
                if current_checksum != placeholder.checksum:
                    integrity_passed = False
                    errors.append(
                        f"Checksum mismatch for {placeholder_id}: expected {placeholder.checksum}, got {current_checksum}"
                    )
            else:
                integrity_passed = False
                errors.append(f"Placeholder {placeholder_id} not found in text")
        return restored_text, integrity_passed, errors

    @staticmethod
    def verify_integrity(result: CompressionResult) -> Tuple[bool, List[str]]:
        _, integrity, errors = RestorationEngine.restore(result.compressed_text, result.placeholders)
        return integrity, errors