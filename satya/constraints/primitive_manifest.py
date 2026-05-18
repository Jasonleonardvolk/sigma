# sigma/satya/constraints/primitive_manifest.py
# Algebraic Compatibility Layer: Primitive Manifest
#
# Formal registry of all constraint primitives with their
# algebraic properties, determinism guarantees, and SVR
# receipt metadata. The manifest hash is included in SVR
# receipts to prove which primitive set was active at audit time.
#
# May 17, 2026 | Invariant Research | Patent Pending
# All code is plain ASCII.

import hashlib
import json


CONSTRAINT_LAYER_VERSION = "1.0.0"


PRIMITIVE_MANIFEST = {
    "IntervalContains": {
        "category": "interval",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "ordered intervals over reals",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE", "AMBIGUOUS_WITH_BOUNDS"],
        "params": ["tolerance"],
    },
    "IntervalOverlap": {
        "category": "interval",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "interval intersection with Jaccard metric",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE"],
        "params": [],
    },
    "MoneyEquals": {
        "category": "financial",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "decimal arithmetic with absolute and relative tolerance",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE"],
        "params": ["abs_tol", "rel_tol"],
    },
    "MoneyLessThan": {
        "category": "financial",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "strict ordering over decimals with tolerance band",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE", "AMBIGUOUS_WITH_BOUNDS"],
        "params": ["tolerance"],
    },
    "DateBefore": {
        "category": "temporal",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "strict ordering over date ordinals",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE", "AMBIGUOUS_WITH_BOUNDS"],
        "params": [],
    },
    "DateAfter": {
        "category": "temporal",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "strict ordering over date ordinals (reversed)",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE", "AMBIGUOUS_WITH_BOUNDS"],
        "params": [],
    },
    "DateWithin": {
        "category": "temporal",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "bounded distance over date ordinals",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE"],
        "params": ["window_days"],
    },
    "QuantitySum": {
        "category": "arithmetic",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "summation equality with tolerance",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE"],
        "params": ["abs_tol", "rel_tol"],
    },
    "PercentBound": {
        "category": "arithmetic",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "interval containment with auto-scale detection",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE"],
        "params": ["tolerance"],
    },
    "StringPrefix": {
        "category": "textual",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "prefix matching with partial overlap metric",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE", "AMBIGUOUS_WITH_BOUNDS"],
        "params": [],
    },
    "StringSuffix": {
        "category": "textual",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "suffix matching",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE"],
        "params": [],
    },
    "EnumInclusion": {
        "category": "set_theoretic",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "membership test over finite enumeration",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE"],
        "params": [],
    },
    "SetSubset": {
        "category": "set_theoretic",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "subset relation with coverage metric",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE", "AMBIGUOUS_WITH_BOUNDS"],
        "params": [],
    },
    "SetDisjoint": {
        "category": "set_theoretic",
        "arity": 2,
        "deterministic": True,
        "bounded": True,
        "receipt_safe": True,
        "theory": "disjointness test with overlap metric",
        "verdict_set": ["PASS", "FAIL", "INSUFFICIENT_EVIDENCE"],
        "params": [],
    },
}


def manifest_hash():
    """Compute a deterministic SHA-256 hash of the manifest.

    This hash is included in SVR receipts to prove which
    primitive set was active when the receipt was issued.
    Any change to the manifest (adding, removing, or modifying
    a primitive) changes the hash.

    Returns:
        16-character hex string (first 16 chars of SHA-256).
    """
    canonical = json.dumps(
        PRIMITIVE_MANIFEST,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()[:16]


def primitive_count():
    """Total number of registered primitives."""
    return len(PRIMITIVE_MANIFEST)


def primitives_by_category():
    """Group primitive names by category.

    Returns:
        Dict mapping category name to list of primitive names.
    """
    groups = {}
    for name, meta in PRIMITIVE_MANIFEST.items():
        cat = meta["category"]
        if cat not in groups:
            groups[cat] = []
        groups[cat].append(name)
    return groups


def validate_manifest():
    """Check that every manifest entry corresponds to a registered primitive.

    Returns:
        List of error strings. Empty list means valid.
    """
    from sigma.satya.constraints.primitives import PRIMITIVE_REGISTRY

    errors = []
    for name in PRIMITIVE_MANIFEST:
        if name not in PRIMITIVE_REGISTRY:
            errors.append(
                "Manifest entry '%s' has no matching primitive class"
                % name
            )
    for name in PRIMITIVE_REGISTRY:
        if name not in PRIMITIVE_MANIFEST:
            errors.append(
                "Primitive class '%s' is not in the manifest"
                % name
            )
    return errors
