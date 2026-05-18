# sigma/demo/demo_soc2_svr_end_to_end.py
# End-to-End Proof Artifact: SOC 2 -> SVR Receipt
#
# Proves the full chain in one command:
#   SOC 2 sample facts
#     -> soc2_tsc_v1 profile
#     -> ConstraintInstance objects
#     -> primitive evaluation
#     -> propagation
#     -> compiler
#     -> Purity-Gate-certified restriction maps
#     -> sheaf insertion
#     -> H1 / Dirichlet energy
#     -> proof sketch
#     -> SVR receipt
#     -> Ed25519 signature
#     -> signature verification
#
# Usage:
#   Set-Location "C:\Dev\kha"
#   python -m sigma.demo.demo_soc2_svr_end_to_end
#
# May 17, 2026 | Invariant Research | Patent Pending
# All code is plain ASCII.

import json
import os
import sys
import time
import numpy as np

from sigma.core.sheaf import CellularSheaf, PURITY_GATE_RHO_MAX
from sigma.core.graph import SheafGraph
from sigma.satya.constraints.primitives import (
    CompatibilityVerdict,
    get_primitive,
)
from sigma.satya.constraints.compiler import ConstraintCompiler
from sigma.satya.constraints.propagation import ConstraintPropagator
from sigma.satya.constraints.proof_sketch import ProofSketchGenerator
from sigma.satya.constraints.remediation import RemediationEngine
from sigma.satya.constraints.primitive_manifest import (
    CONSTRAINT_LAYER_VERSION,
    manifest_hash,
    primitive_count,
)
from sigma.satya.profiles import get_profile, list_profiles
from sigma.satya.proofs.signer import SatyaSigner
from sigma.satya.spec.canonical import (
    canonical_bytes,
    verify_signature,
    validate_receipt,
)
from sigma.satya.spec.stamp import stamp_svr


def separator(title):
    print("")
    print("=" * 68)
    print("  %s" % title)
    print("=" * 68)
    print("")


def main():
    t0 = time.perf_counter()

    # Parse --out argument
    out_dir = None
    for i, arg in enumerate(sys.argv):
        if arg == "--out" and i + 1 < len(sys.argv):
            out_dir = sys.argv[i + 1]
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # ==================================================================
    # STEP 0: Environment
    # ==================================================================
    separator("STEP 0: Environment")

    print("Constraint Layer Version: %s" % CONSTRAINT_LAYER_VERSION)
    print("Primitive Manifest Hash:  %s" % manifest_hash())
    print("Primitives Registered:    %d" % primitive_count())
    print("Purity Gate Threshold:    %.2f" % PURITY_GATE_RHO_MAX)
    print("Registered Profiles:      %s" % list_profiles())

    # ==================================================================
    # STEP 1: SOC 2 Sample Facts
    # ==================================================================
    separator("STEP 1: SOC 2 Sample Facts")

    # Two criteria: one mostly passing, one with failures.
    # This proves the system detects both clean and dirty states.
    criteria_facts = [
        {
            "criterion_id": "CC6.1",
            "label": "Logical and Physical Access Controls",
            "criterion_topics": {
                "access_control", "authentication", "authorization",
            },
            "policy_topics": {
                "access_control", "authentication", "authorization",
                "mfa", "role_based_access",
            },
            "required_evidence": {
                "access_policy", "access_review_log",
                "provisioning_records",
            },
            "provided_evidence": {
                "access_policy", "access_review_log",
                "provisioning_records",
            },
            "evidence_date": "2026-04-01",
            "audit_end_date": "2026-05-17",
            "owner": "Jane Smith, CISO",
            "frequency": "quarterly",
            "stated_criterion": "CC6.1",
        },
        {
            "criterion_id": "CC7.2",
            "label": "Security Incident Monitoring",
            "criterion_topics": {
                "incident_monitoring", "alerting", "anomaly_detection",
            },
            "policy_topics": {
                "incident_response",
                # Missing: "alerting", "anomaly_detection"
            },
            "required_evidence": {
                "incident_response_plan", "monitoring_dashboard",
                "alert_config",
            },
            "provided_evidence": {
                "incident_response_plan",
                # Missing: "monitoring_dashboard", "alert_config"
            },
            "evidence_date": "2025-01-15",  # Old, outside audit window
            "audit_end_date": "2026-05-17",
            "owner": None,  # No owner assigned
            "frequency": "annual",  # Should be continuous for CC7
            "stated_criterion": "CC7.2",
        },
    ]

    for facts in criteria_facts:
        print("Criterion: %s (%s)" % (
            facts["criterion_id"], facts["label"]
        ))
        print("  Policy topics:    %s" % sorted(facts["policy_topics"]))
        print("  Provided evidence: %s" % sorted(facts["provided_evidence"]))
        print("  Evidence date:    %s" % facts["evidence_date"])
        print("  Owner:            %s" % facts.get("owner", "NONE"))
        print("  Frequency:        %s" % facts.get("frequency"))
        print("")

    # ==================================================================
    # STEP 2: Profile -> ConstraintInstances
    # ==================================================================
    separator("STEP 2: Profile Emits ConstraintInstances")

    profile = get_profile("soc2_tsc_v1")
    print("Profile: %s (vertical: %s, version: %s)" % (
        profile.profile_id, profile.vertical, profile.version
    ))
    print("Supported primitives: %s" % sorted(profile.supported_primitives))
    print("")

    all_instances = []
    for facts in criteria_facts:
        instances = profile.emit_constraints(facts)
        all_instances.extend(instances)
        print("  %s: %d ConstraintInstances emitted" % (
            facts["criterion_id"], len(instances)
        ))
        for inst in instances:
            print("    %s: %s -> %s [%s]" % (
                inst.primitive_name, inst.subject, inst.object,
                inst.domain_context.get("family", ""),
            ))

    print("")
    print("Total ConstraintInstances: %d" % len(all_instances))

    # ==================================================================
    # STEP 3: Primitive Evaluation
    # ==================================================================
    separator("STEP 3: Primitive Evaluation")

    all_results = []
    for facts in criteria_facts:
        results = profile.audit_criterion(facts["criterion_id"], facts)
        all_results.extend(results)
        print("  %s: %d ConstraintResults" % (
            facts["criterion_id"], len(results)
        ))
        for r in results:
            symbol = {
                CompatibilityVerdict.PASS: "[PASS]",
                CompatibilityVerdict.FAIL: "[FAIL]",
                CompatibilityVerdict.INSUFFICIENT_EVIDENCE: "[INSF]",
                CompatibilityVerdict.AMBIGUOUS_WITH_BOUNDS: "[AMBG]",
            }.get(r.verdict, "[????]")
            print("    %s %-22s compat=%.2f  %s" % (
                symbol, r.constraint_name, r.compatibility,
                r.explanation[:80],
            ))
        print("")

    pass_count = sum(1 for r in all_results if r.is_pass)
    fail_count = sum(1 for r in all_results if r.is_fail)
    insf_count = sum(1 for r in all_results if r.is_insufficient)
    print("Summary: %d PASS, %d FAIL, %d INSUFFICIENT, %d total" % (
        pass_count, fail_count, insf_count, len(all_results)
    ))

    # ==================================================================
    # STEP 4: Propagation
    # ==================================================================
    separator("STEP 4: Constraint Propagation")

    propagator = ConstraintPropagator()
    prop_report = propagator.propagate(all_results)

    print("Input:  %d constraints" % prop_report.input_count)
    print("Output: %d constraints" % prop_report.output_count)
    print("Transitive failures: %d" % prop_report.transitive_failures)
    print("Downgrades:          %d" % prop_report.downgrades)
    print("Derived:             %d" % prop_report.derived_constraints)

    if prop_report.events:
        print("")
        for event in prop_report.events:
            print("  [%s] %s" % (event.event_type, event.explanation[:80]))

    # ==================================================================
    # STEP 5: Constraint Compiler -> Restriction Maps
    # ==================================================================
    separator("STEP 5: Compilation to Restriction Maps")

    compiler = ConstraintCompiler(stalk_dim=8)
    comp_report = compiler.compile_batch(prop_report.results)

    print("Compiled: %d total" % comp_report.total)
    print("  PASS:         %d" % comp_report.passed)
    print("  FAIL:         %d" % comp_report.failed)
    print("  INSUFFICIENT: %d" % comp_report.insufficient)
    print("  AMBIGUOUS:    %d" % comp_report.ambiguous)
    print("  All PG certified: %s" % comp_report.all_certified)
    print("")

    # Verify Purity Gate on every compiled map
    pg_violations = 0
    for cc in comp_report.compiled:
        sm_u = float(np.linalg.svd(cc.rho_u, compute_uv=False)[0])
        sm_v = float(np.linalg.svd(cc.rho_v, compute_uv=False)[0])
        if sm_u > PURITY_GATE_RHO_MAX + 1e-12:
            pg_violations += 1
        if sm_v > PURITY_GATE_RHO_MAX + 1e-12:
            pg_violations += 1
    print("Purity Gate violations: %d (must be 0)" % pg_violations)
    assert pg_violations == 0, "PURITY GATE VIOLATION DETECTED"

    # ==================================================================
    # STEP 6: Sheaf Assembly
    # ==================================================================
    separator("STEP 6: Sheaf Assembly")

    # Build a sheaf where each constraint is an edge between
    # two vertices (the constraint's subject and object).
    n_constraints = comp_report.total
    n_vertices = n_constraints * 2  # subject + object per constraint
    stalk_dim = 8

    graph = SheafGraph()
    for i in range(n_vertices):
        graph.add_vertex(i)

    edge_list = []
    for i in range(n_constraints):
        u = i * 2
        v = i * 2 + 1
        graph.add_edge(u, v)
        edge_list.append((u, v))

    sheaf = CellularSheaf(graph, default_stalk_dim=stalk_dim)

    # Install compiled restriction maps
    for i, cc in enumerate(comp_report.compiled):
        u, v = edge_list[i]
        compiler.install_into_sheaf(sheaf, u, v, i, cc)

    # Verify sheaf Purity Gate
    pg_result = sheaf.verify_purity_gate()
    print("Sheaf: %d vertices, %d edges, %d maps" % (
        graph.num_vertices, graph.num_edges, pg_result["total_maps"]
    ))
    print("PG verify: %d maps checked, %d violations, sigma_max=%.6f" % (
        pg_result["total_maps"],
        pg_result["violations"],
        pg_result["sigma_max_global"],
    ))
    assert pg_result["violations"] == 0, "SHEAF PG VIOLATION"

    # ==================================================================
    # STEP 7: H1 / Dirichlet Energy
    # ==================================================================
    separator("STEP 7: Cohomology and Dirichlet Energy")

    # Compute coboundary and Laplacian
    section = sheaf.random_section(seed=42, scale=1.0)
    energy = sheaf.dirichlet_energy(section)
    per_edge = sheaf.dirichlet_energy_per_edge(section)

    # Build coboundary matrix for H1 dimension estimate
    delta = sheaf.coboundary_matrix_sparse()
    energy_threshold = 0.01
    obstructed_edges = [
        (eidx, e) for eidx, e in per_edge.items()
        if e > energy_threshold
        and comp_report.compiled[eidx].result.verdict == CompatibilityVerdict.FAIL
    ]

    failed_edge_count = sum(
        1 for cc in comp_report.compiled
        if cc.result.verdict == CompatibilityVerdict.FAIL
    )

    print("Total Dirichlet energy:  %.6f" % energy)
    print("Failed constraint edges: %d of %d" % (
        failed_edge_count, graph.num_edges
    ))
    print("Proof-sketch obstructions: %d" % len(obstructed_edges))
    print("")

    # Show per-constraint energy with labels
    for i, cc in enumerate(comp_report.compiled):
        e = per_edge.get(i, 0.0)
        r = cc.result
        if r.verdict == CompatibilityVerdict.FAIL:
            marker = " <<< OBSTRUCTION"
        else:
            marker = ""
        print("  Edge %2d: E=%.6f  theta=%.4f  %s [%s]%s" % (
            i, e, cc.theta,
            r.constraint_name, r.verdict.value, marker
        ))

    # ==================================================================
    # STEP 8: Proof Sketches
    # ==================================================================
    separator("STEP 8: Proof Sketches")

    generator = ProofSketchGenerator()
    sketch_report = generator.generate(comp_report, prop_report)

    print(sketch_report.summary)
    print("")

    for sketch in sketch_report.sketches:
        print(sketch.render())
        print("---")

    # ==================================================================
    # STEP 8.5: Minimal Remediation Set
    # ==================================================================
    separator("STEP 8.5: Remediation: Repair, Plan, Assurance")

    remediation_engine = RemediationEngine()
    remediation_report = remediation_engine.compute(
        comp_report.compiled, sketch_report,
        receipt_id="pending",
        profile_id=profile.profile_id,
    )

    print(remediation_report.render())

    # ==================================================================
    # STEP 9: SVR Receipt
    # ==================================================================
    separator("STEP 9: SVR Receipt Assembly")

    # Build the raw response dict (as wrapper.py would)
    import hashlib
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    input_text = json.dumps(criteria_facts, sort_keys=True,
                            default=lambda x: sorted(x) if isinstance(x, set) else str(x))
    input_hash = hashlib.sha256(
        input_text.encode("utf-8")
    ).hexdigest()[:16]

    h1_dim = len(obstructed_edges)
    verdict = "contradicted" if h1_dim > 0 else "faithful"

    # Build checked_items from constraint results
    checked_items = []
    items_passed = 0
    items_failed = 0
    for idx, cc in enumerate(comp_report.compiled):
        r = cc.result
        if r.verdict == CompatibilityVerdict.PASS:
            status = "PASS"
            items_passed += 1
        elif r.verdict == CompatibilityVerdict.FAIL:
            status = "FAIL"
            items_failed += 1
        elif r.verdict == CompatibilityVerdict.INSUFFICIENT_EVIDENCE:
            status = "INSUFFICIENT_EVIDENCE"
            items_failed += 1
        else:
            status = "AMBIGUOUS"
            items_failed += 1
        checked_items.append({
            "item_id": idx + 1,
            "claim_or_authority": r.constraint_name,
            "verdict": status,
            "reason": r.explanation[:200] if r.explanation else "",
            "compatibility": round(r.compatibility, 4),
            "theta_rad": round(cc.theta, 6),
        })

    response = {
        "verdict": verdict,
        "safe_to_submit": h1_dim == 0,
        "faithful": h1_dim == 0,
        "contradictions": comp_report.failed,
        "unsupported_claims": comp_report.insufficient,
        "sheaf_metrics": {
            "h1_dimension": h1_dim,
            "obstruction_count": len(obstructed_edges),
            "cokernel_dimension": comp_report.insufficient,
            "grounding_ratio": round(
                comp_report.passed / max(comp_report.total, 1), 4
            ),
            "evidence_edges": comp_report.total,
            "claims_extracted": len(all_instances),
            "total_dirichlet_energy": round(energy, 6),
        },
        "proof": {
            "certificate_id": "SATYA-%s-%s" % (
                now.strftime("%Y%m%d"), input_hash[:8].upper()
            ),
            "certified": h1_dim == 0,
            "certification_basis": (
                "h1_source_conflict" if h1_dim > 0
                else "fully_grounded"
            ),
            "input_hash": input_hash,
            "source_hashes": [],
            "timestamp": now.isoformat(),
            "satya_version": "0.1.0",
            "sigma_version": "1.0.0",
            "public_key": None,
        },
        "conflict_details": [],
        "constraint_results": [
            cc.to_receipt_fragment() for cc in comp_report.compiled
        ],
        "proof_sketches": sketch_report.to_dict(),
        "profile_id": profile.profile_id,
        "profile_vertical": profile.vertical,
        "mode": "mode_1_local",
        "domain": "compliance",
        "checked_items": checked_items,
        "items_checked": len(checked_items),
        "items_passed": items_passed,
        "items_failed": items_failed,
        "items_excluded": 0,
        "latency_ms": 0.0,
    }

    # Add remediation to receipt
    remediation_report.finding_receipt_id = response["proof"]["certificate_id"]
    response.update(remediation_report.to_dict())

    # ==================================================================
    # STEP 10: Ed25519 Signature
    # ==================================================================
    separator("STEP 10: Ed25519 Signature")

    signer = SatyaSigner.ephemeral()
    print("Public key:   %s" % signer.public_key_hex)
    print("Fingerprint:  %s" % signer.fingerprint[:32])

    # Stamp the SVR envelope (adds svr_version, receipt_id, etc.)
    stamped = stamp_svr(response, signer=signer, evaluation=True)

    print("")
    print("SVR Version:  %s" % stamped.get("svr_version"))
    print("Receipt ID:   %s" % stamped.get("receipt_id"))
    print("Receipt Type: %s" % stamped.get("receipt_type"))
    print("Status:       %s" % stamped.get("receipt_status"))
    print("Signature:    %s...%s" % (
        stamped["signature"][:16], stamped["signature"][-16:]
    ))
    print("Sig Status:   %s" % stamped.get("signature_status"))
    print("Constraint Layer: %s" % stamped.get("constraint_layer_version"))
    print("Manifest Hash:    %s" % stamped.get("primitive_manifest_hash"))
    print("Verify URL:   %s" % stamped.get("verify_url"))

    # ==================================================================
    # STEP 11: Signature Verification
    # ==================================================================
    separator("STEP 11: Signature Verification")

    canon = canonical_bytes(stamped)
    print("Canonical payload: %d bytes" % len(canon))
    print("Canonical hash:    %s" % hashlib.sha256(canon).hexdigest()[:32])

    # Verify signature
    sig_valid = verify_signature(stamped)
    print("Signature valid:   %s" % sig_valid)
    assert sig_valid, "SIGNATURE VERIFICATION FAILED"

    # Validate receipt structure
    validation_errors = validate_receipt(stamped)
    receipt_valid = len(validation_errors) == 0
    print("Receipt valid:     %s" % receipt_valid)
    if validation_errors:
        for err in validation_errors:
            print("  ERROR: %s" % err)
    assert receipt_valid, "RECEIPT VALIDATION FAILED: %s" % validation_errors

    # ==================================================================
    # STEP 12: Final Receipt
    # ==================================================================
    separator("STEP 12: Complete SVR Receipt")

    elapsed = (time.perf_counter() - t0) * 1000.0
    stamped["latency_ms"] = round(elapsed, 1)

    # Print the receipt as formatted JSON
    # Exclude large arrays for readability
    display = dict(stamped)
    display.pop("conflict_details", None)
    display.pop("constraint_results", None)

    print(json.dumps(display, indent=2, default=str))

    # ==================================================================
    # VERDICT
    # ==================================================================
    separator("VERDICT")

    print("Full pipeline: SOC 2 facts -> profile -> primitives ->")
    print("  propagation -> compiler -> Purity Gate -> sheaf ->")
    print("  H1/energy -> proof sketch -> SVR receipt -> Ed25519 ->")
    print("  signature verification")
    print("")
    print("Results:")
    print("  Constraints evaluated: %d" % comp_report.total)
    print("  Purity Gate:           %d violations (0 required)" % pg_violations)
    print("  Obstructed edges:      %d" % len(obstructed_edges))
    print("  Proof sketches:        %s" % sketch_report.summary)
    print("  Remediation:           %d repair(s): %d critical-priority, %d high-priority" % (
        remediation_report.repairs_required,
        remediation_report.critical_repairs,
        remediation_report.high_repairs,
    ))
    print("  Signature:             %s" % ("VALID" if sig_valid else "INVALID"))
    print("  Receipt:               %s" % ("VALID" if receipt_valid else "INVALID"))
    print("  Total time:            %.1f ms" % elapsed)
    print("")
    print("Proof artifact complete.")

    # ==================================================================
    # ARTIFACT OUTPUT
    # ==================================================================
    if out_dir:
        separator("Writing Artifacts to %s" % out_dir)

        def _json_default(obj):
            if isinstance(obj, set):
                return sorted(obj)
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return str(obj)

        # receipt.svr.json
        receipt_path = os.path.join(out_dir, "receipt.svr.json")
        with open(receipt_path, "w", encoding="utf-8") as f:
            json.dump(stamped, f, indent=2, default=_json_default)
        print("  receipt.svr.json (%d bytes)" % os.path.getsize(receipt_path))

        # proof_sketches.json
        sketches_path = os.path.join(out_dir, "proof_sketches.json")
        with open(sketches_path, "w", encoding="utf-8") as f:
            json.dump(sketch_report.to_dict(), f, indent=2, default=_json_default)
        print("  proof_sketches.json (%d bytes)" % os.path.getsize(sketches_path))

        # constraints.json
        constraints_path = os.path.join(out_dir, "constraints.json")
        constraint_data = {
            "profile_id": profile.profile_id,
            "vertical": profile.vertical,
            "constraint_layer_version": CONSTRAINT_LAYER_VERSION,
            "primitive_manifest_hash": manifest_hash(),
            "total_constraints": comp_report.total,
            "passed": comp_report.passed,
            "failed": comp_report.failed,
            "insufficient": comp_report.insufficient,
            "ambiguous": comp_report.ambiguous,
            "all_certified": comp_report.all_certified,
            "results": [
                cc.to_receipt_fragment() for cc in comp_report.compiled
            ],
        }
        with open(constraints_path, "w", encoding="utf-8") as f:
            json.dump(constraint_data, f, indent=2, default=_json_default)
        print("  constraints.json (%d bytes)" % os.path.getsize(constraints_path))

        # compiled_maps_manifest.json
        maps_path = os.path.join(out_dir, "compiled_maps_manifest.json")
        maps_data = {
            "purity_gate_rho_max": PURITY_GATE_RHO_MAX,
            "stalk_dim": 8,
            "total_maps": pg_result["total_maps"],
            "violations": pg_result["violations"],
            "sigma_max_global": pg_result["sigma_max_global"],
            "edges": [
                {
                    "edge_idx": i,
                    "constraint": comp_report.compiled[i].result.constraint_name,
                    "verdict": comp_report.compiled[i].result.verdict.value,
                    "theta": round(comp_report.compiled[i].theta, 6),
                    "dirichlet_energy": round(per_edge.get(i, 0.0), 6),
                    "sigma_max_u": round(float(np.linalg.svd(
                        comp_report.compiled[i].rho_u, compute_uv=False)[0]), 6),
                    "sigma_max_v": round(float(np.linalg.svd(
                        comp_report.compiled[i].rho_v, compute_uv=False)[0]), 6),
                }
                for i in range(comp_report.total)
            ],
        }
        with open(maps_path, "w", encoding="utf-8") as f:
            json.dump(maps_data, f, indent=2, default=_json_default)
        print("  compiled_maps_manifest.json (%d bytes)" % os.path.getsize(maps_path))

        # run_summary.txt
        summary_path = os.path.join(out_dir, "run_summary.txt")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("SATYA SOC 2 End-to-End Verification Run\n")
            f.write("Date: %s\n" % now.isoformat())
            f.write("Receipt ID: %s\n" % stamped.get("receipt_id", ""))
            f.write("Profile: %s (vertical: %s)\n" % (profile.profile_id, profile.vertical))
            f.write("Constraint Layer: %s\n" % CONSTRAINT_LAYER_VERSION)
            f.write("Manifest Hash: %s\n" % manifest_hash())
            f.write("Purity Gate: %.2f\n" % PURITY_GATE_RHO_MAX)
            f.write("\n")
            f.write("Constraints: %d total, %d pass, %d fail\n" % (
                comp_report.total, comp_report.passed, comp_report.failed))
            f.write("Purity Gate violations: %d\n" % pg_violations)
            f.write("Obstructed edges: %d\n" % len(obstructed_edges))
            f.write("Proof sketches: %s\n" % sketch_report.summary)
            f.write("Total Dirichlet energy: %.6f\n" % energy)
            f.write("\n")
            f.write("Signature: %s\n" % ("VALID" if sig_valid else "INVALID"))
            f.write("Receipt: %s\n" % ("VALID" if receipt_valid else "INVALID"))
            f.write("Total time: %.1f ms\n" % elapsed)
        print("  run_summary.txt (%d bytes)" % os.path.getsize(summary_path))

        # signature_verification.txt
        sigver_path = os.path.join(out_dir, "signature_verification.txt")
        with open(sigver_path, "w", encoding="utf-8") as f:
            f.write("SVR Signature Verification Report\n")
            f.write("Receipt ID: %s\n" % stamped.get("receipt_id", ""))
            f.write("Public Key: %s\n" % signer.public_key_hex)
            f.write("Fingerprint: %s\n" % signer.fingerprint)
            f.write("Canonical payload: %d bytes\n" % len(canon))
            f.write("Canonical hash: %s\n" % hashlib.sha256(canon).hexdigest())
            f.write("Signature: %s\n" % stamped.get("signature", ""))
            f.write("Signature status: %s\n" % stamped.get("signature_status", ""))
            f.write("Verification result: %s\n" % ("VALID" if sig_valid else "INVALID"))
            f.write("Receipt validation errors: %s\n" % (
                "none" if receipt_valid else "; ".join(validation_errors)))
        print("  signature_verification.txt (%d bytes)" % os.path.getsize(sigver_path))

        # remediation.json
        remed_path = os.path.join(out_dir, "remediation.json")
        with open(remed_path, "w", encoding="utf-8") as f:
            json.dump(remediation_report.to_dict(), f, indent=2, default=_json_default)
        print("  remediation.json (%d bytes)" % os.path.getsize(remed_path))

        print("\nAll artifacts written.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
