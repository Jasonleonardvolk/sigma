# SOC 2 Verification Receipt Demo

This demo runs the complete SATYA/SIGMA verification chain:
SOC 2 facts -> domain profile -> algebraic constraints -> propagation ->
Purity-Gate-certified restriction maps -> sheaf assembly ->
H1/Dirichlet obstruction localization -> proof sketches -> SVR receipt ->
Ed25519 signature verification.

## Quick Run

    Set-Location "C:\Dev\kha"
    python -m sigma.demo.demo_soc2_svr_end_to_end

## Run with Artifact Output

    python -m sigma.demo.demo_soc2_svr_end_to_end --out sigma\demo\artifacts\soc2_svr_e2e_20260517

Writes six files:

    receipt.svr.json              Complete signed SVR receipt
    proof_sketches.json           Human-readable obstruction explanations
    constraints.json              Per-constraint evaluation results
    compiled_maps_manifest.json   Purity-Gate-certified map diagnostics
    run_summary.txt               One-page run summary
    signature_verification.txt    Ed25519 verification report

## Observed Run (May 17, 2026)

    12 constraints evaluated
    0 Purity Gate violations
    12 obstructed edges (5 from FAIL constraints on CC7.2)
    5 proof sketches: 4 critical, 1 high
    VALID signature
    VALID receipt
    43.4 ms total runtime

## What It Proves

CC6.1 (Logical and Physical Access Controls) passes all six constraint
families: policy coverage, evidence coverage, audit period, owner
assignment, frequency match, and criterion mapping. All restriction
maps enter the sheaf as near-identity matrices with zero Dirichlet
energy. Clean gluing.

CC7.2 (Security Incident Monitoring) fails five of six families:
policy topics missing, evidence incomplete, evidence date outside
audit window, no control owner, operating frequency too low. Each
failure compiles into a Givens-rotated restriction map with theta
near pi/2. The sheaf concentrates Dirichlet energy on these edges.
Proof sketches explain each obstruction with severity, constraint
chain, energy concentration, verdict, and remediation.

The SVR receipt carries canonical Ed25519 signature, constraint
layer version, primitive manifest hash, and the full proof sketch
report. Any third party can verify the signature using the public
key and the canonical serialization procedure from SVR_SPEC_v1.

## Architecture

    Raw SOC 2 facts (policy docs, evidence inventory, dates, owners)
        |
    soc2_tsc_v1 profile (C:\Dev\kha\sigma\satya\profiles\soc2_tsc_constraints.py)
        |
    ConstraintInstance objects (universal interface)
        |
    14 certified primitives (C:\Dev\kha\sigma\satya\constraints\primitives.py)
        |
    ConstraintPropagator (transitive detection, domain tightening)
        |
    ConstraintCompiler (Givens rotation, Purity Gate by construction)
        |
    CellularSheaf assembly (C:\Dev\kha\sigma\core\sheaf.py)
        |
    H1 / Dirichlet energy / obstruction localization
        |
    ProofSketchGenerator (human-readable explanations)
        |
    stamp_svr() -> SVR v1.0 receipt -> Ed25519 signature

## Buyer Line

Before you pay for the SOC 2 audit, SATYA can verify whether your
policy/evidence package actually glues into a coherent control state.
In this demo, the full signed verification receipt was produced in
43.4 ms.

## Technical Line

SATYA compiles domain-specific SOC 2 constraints into Purity-Gate-certified
sheaf restriction maps, detects non-gluing through H1/Dirichlet energy,
and emits a canonically signed SVR receipt. Zero ML. Zero GPU.
Zero parameters. Fully deterministic. Patent pending.
