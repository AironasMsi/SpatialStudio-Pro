"""
Perceptual Hash (pHash) Duplicate Guardrail Engine
Computes discrete cosine transform (DCT) image hashes and validates Hamming distance.
"""
from pathlib import Path
from typing import Dict, Optional, Tuple
import imagehash
from PIL import Image

class PerceptualGuardrail:
    def __init__(self, threshold: int = 6):
        self.threshold = threshold
        self.registry: Dict[str, imagehash.ImageHash] = {}

    def compute_hash(self, image_path: Path) -> imagehash.ImageHash:
        with Image.open(image_path) as img:
            return imagehash.phash(img)

    def is_duplicate(self, image_path: Path) -> Tuple[bool, Optional[str], int]:
        new_hash = self.compute_hash(image_path)
        for existing_id, existing_hash in self.registry.items():
            dist = new_hash - existing_hash
            if dist <= self.threshold:
                return True, existing_id, dist
        return False, None, 999

    def register(self, asset_id: str, image_path: Path) -> imagehash.ImageHash:
        h = self.compute_hash(image_path)
        self.registry[asset_id] = h
        return h
