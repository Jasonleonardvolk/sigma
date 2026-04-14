# SIGMA

**Scalable detection of global inconsistencies via cellular sheaf cohomology.**

Detects contradictions that cannot be resolved by any local adjustment.

---

## The Problem

AI systems produce outputs that look locally consistent but are globally impossible. Every adjacent pair of claims checks out. The chain as a whole is contradictory. No existing verification method catches this reliably at scale.

SIGMA is a post-generation verification layer. It takes structured knowledge (a graph of entities and relationships), constructs a cellular sheaf over it, and uses first sheaf cohomology (H^1) to detect irreconcilable contradictions -- places where no assignment of local values can produce a globally consistent state. The detection is algebraic, not heuristic. If SIGMA says it's contradictory, it is.

## Key Result

| | |
|---|---|
| **Vertices validated** | 1,000,000 |
| **Per-vertex cost** | 3.55 ms (constant from 50K to 1M) |
| **Peak memory** | 28.6 GB |
| **Cells** | 8,663 bounded independent units |
| **Nerve max dimension** | 4 (stable across all scales) |
| **Crashes** | 0 |
| **Hardware** | Single laptop (i9-13900H, 64GB RAM) |

The architecture decomposes the monolithic sheaf Laplacian (8,000,000 x 8,000,000 at V=1M) into thousands of bounded cells via recursive Fiedler spectral bisection. Each cell computes its own H^1 and spectral gap independently. Global cohomology is recovered from local data via the Cech spectral sequence. Per-vertex cost does not increase with graph size.

## Demo: What SIGMA Sees

**Input:** 6 claims from an LLM reasoning chain. Every adjacent pair is consistent.

```
1. The contract requires delivery by March 15
2. Force majeure extends all deadlines by 90 days
3. The penalty clause activates on the original deadline
4. Insurance covers penalties only during extensions
5. The vendor confirmed compliance with all terms
6. No penalties have been assessed or waived
```

**SIGMA output:**

```
Contradictions detected: 3

  Claim 2 <-> Claim 3:  irreconcilable (H^1 obstruction)
                        extension vs original deadline activation

  Claim 3 <-> Claim 6:  irreconcilable (H^1 obstruction)
                        penalty triggers but none assessed

  Claim 4 <-> Claim 6:  irreconcilable (H^1 obstruction)
                        coverage scope vs no action taken

False positives:  0
Detection time:   47 ms
Obstruction dim:  H^1 = 3
```

Each contradiction is mathematically proven to be unresolvable by any local adjustment. The sheaf Laplacian identifies exactly which relationships fail to extend from local consistency to global coherence.

## Scale

```
V           Cells    Cost/Entity    Peak RAM    Crashes
------------------------------------------------------
50,000      431      3.86 ms        1.6 GB      0
100,000     890      3.37 ms        3.1 GB      0
250,000     2,200    3.66 ms        7.4 GB      0
1,000,000   8,663    3.55 ms        28.6 GB     0
```

V grew 20x. Per-entity cost: **flat.**

## How It Works (High Level)

1. **Sheaf construction.** A cellular sheaf is built over the knowledge graph. Vertices carry local vector spaces (stalks). Edges carry linear restriction maps encoding relational constraints.

2. **Cohomology detection.** First sheaf cohomology H^1 counts independent obstructions that no choice of local values can resolve. Per-edge Dirichlet energy localizes contradictions to specific relationships.

3. **Cellular decomposition.** The monolithic sheaf is partitioned into bounded cells via spectral bisection. Each cell runs independently. The nerve complex tracks cell adjacency.

4. **Global assembly.** The Cech spectral sequence recovers exact global H^1 from local cell data. Proven correct against monolithic ground truth.

5. **Spectral governance.** A density-aware spectral governor maintains structural stability (positive spectral gap, bounded edge-vertex ratio) under autonomous graph growth via Lyapunov stability in the Borkar stochastic approximation framework.

## Architecture

```
Knowledge Graph
      |
      v
  Sheaf Construction (restriction maps, Purity Gate certification)
      |
      v
  Cellular Decomposition (Fiedler spectral bisection)
      |
      v
  Per-Cell Eigensolves (H^1, lambda_2, Dirichlet energy)
      |
      v
  Nerve Assembly (Cech spectral sequence)
      |
      v
  Contradiction Report (locations, severity, algebraic proof)
```

## What This Is Not

- **Not an LLM.** SIGMA does not generate text or answer questions. It verifies structural consistency.
- **Not a constraint solver.** SAT/SMT solvers check logical satisfiability. SIGMA detects topological obstructions -- a different and complementary category.
- **Not a replacement for human oversight.** SIGMA provides structural indicators and certified mutation proposals. Domain calibration is required before deployment.

## Status

- Provisional patent filed (U.S. App# 64/023,418, March 2026)
- ICML 2026 AI4Math Workshop submission in progress
- Preprint: [Zenodo DOI 10.5281/zenodo.19360505](https://zenodo.org/records/19360505)

## Applications

- **Legal:** Detect contradictions across contract corpora, identify circuit splits in case law
- **Financial:** Verify consistency of regulatory filings, audit trail integrity
- **Medical:** Cross-reference clinical guidelines, detect conflicting treatment protocols
- **AI Safety:** Post-generation verification layer for LLM outputs and autonomous agent reasoning

## Contact

Jason Volk
[jason@invariant.pro](mailto:jason@invariant.pro)
[invariant.pro](https://invariant.pro)

## License

All rights reserved. Contact for licensing inquiries.
