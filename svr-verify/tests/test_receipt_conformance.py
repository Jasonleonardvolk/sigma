# tests/test_receipt_conformance.py
# Conformance matrix: drive each documented receipt case through the public
# verify() entry point and assert the outcome.
#
# This mirrors the truth table published in the svr-receipts-examples dataset
# (fixtures_index.jsonl) and the verifier Space README: exactly one clean pass
# and four distinct failure modes. The cases are constructed from the shared
# conftest helpers so the test is self-contained and does not depend on any
# checked-in fixture files.

from __future__ import annotations

import json

import pytest

from svr_verify import verify
from conftest import make_unsigned_receipt, sign


def _write(tmp_path, receipt, name="receipt.svr.json"):
    path = tmp_path / name
    path.write_text(json.dumps(receipt), encoding="utf-8")
    return str(path)


def case_valid_signed():
    """Signed with an embedded key, structure clean. The only fully valid case."""
    receipt, _key = sign(make_unsigned_receipt())
    return receipt


def case_unsigned():
    """Structurally valid but unsigned: the signature gate fails."""
    return make_unsigned_receipt()


def case_invalid_schema():
    """Count invariant broken: items_checked says 4, only 2 items present."""
    receipt = make_unsigned_receipt()
    receipt["items_checked"] = 4
    return receipt


def case_invalid_signature():
    """Structure valid, but the signature does not verify under the embedded key."""
    receipt, _key = sign(make_unsigned_receipt())
    sig = bytearray(bytes.fromhex(receipt["signature"]))
    sig[0] ^= 0xFF
    receipt["signature"] = sig.hex()
    return receipt


def case_tampered_payload():
    """Signed content edited after signing: structure stays valid, signature breaks."""
    receipt, _key = sign(make_unsigned_receipt())
    receipt["checked_items"][0]["reason"] = "edited after signing"
    return receipt


# (name, builder, expected_valid, expected_structure_clean)
CASES = [
    ("valid_signed", case_valid_signed, True, True),
    ("unsigned", case_unsigned, False, True),
    ("invalid_schema", case_invalid_schema, False, False),
    ("invalid_signature", case_invalid_signature, False, True),
    ("tampered_payload", case_tampered_payload, False, True),
]


@pytest.mark.parametrize(
    "name,build,expected_valid,expected_structure_clean",
    CASES,
    ids=[c[0] for c in CASES],
)
def test_conformance_outcome(tmp_path, name, build, expected_valid, expected_structure_clean):
    path = _write(tmp_path, build())
    result = verify(path)

    assert result["valid"] is expected_valid, (
        "%s: expected valid=%s, got valid=%s (structure_errors=%s)"
        % (name, expected_valid, result.get("valid"), result.get("structure_errors"))
    )

    structure_clean = len(result.get("structure_errors", [])) == 0
    assert structure_clean is expected_structure_clean, (
        "%s: expected structure_clean=%s, got %s"
        % (name, expected_structure_clean, result.get("structure_errors"))
    )


def test_exactly_one_case_is_fully_valid(tmp_path):
    """Of the five documented cases, exactly one verifies."""
    valid_count = 0
    for _name, build, _ev, _esc in CASES:
        if verify(_write(tmp_path, build()))["valid"]:
            valid_count += 1
    assert valid_count == 1
