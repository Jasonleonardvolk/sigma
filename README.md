# SIGMA

**We contained O(n^3). Structural verification via cellular sheaf cohomology.**

Detects contradictions that cannot be resolved by any local adjustment.
Mathematical proof. Not AI guessing. Linear cost. No GPU.

---

## The Problem

AI systems produce outputs that look locally consistent but are globally impossible. Every adjacent pair of claims checks out. The chain as a whole is contradictory. No existing verification method catches this reliably at scale.

SIGMA is a post-generation verification layer. It takes structured knowledge (a graph of entities and relationships), constructs a cellular sheaf over it, and uses first sheaf cohomology (H^1) to detect irreconcilable contradictions. The detection is algebraic, not heuristic. If SIGMA says it's contradictory, it is.

## Key Result: Enron Email Network

| | |
|---|---|
| **Dataset** | Stanford SNAP Enron (36,692 accounts, 183,831 edges) |
| **Topology** | Power-law (degree CV = 2.609, hub max degree 1,141) |
| **Pipeline time** | 21 seconds (warm cache, 4-seed validated) |
| **Per-vertex cost** | 0.37 ms |
| **Verification cells** | 3,760 (identical across all seeds) |
| **Nerve max dimension** | 2 |
| **Peak memory** | 641 MB |
| **Hardware** | Single laptop (i9-13900H, 64GB RAM, no GPU) |

The sheaf Laplacian is 170,472 x 170,472. A dense eigensolve takes ~14 hours. SIGMA decomposes the graph so no eigensolve ever sees more than 500 vertices. The O(n^3) doesn't disappear. It gets factored:

```
O(n^3) -> O(n/v_max) * O(v_max^3) = O(n) * constant
```

The cube is imprisoned inside a constant.

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

## Scale

Validated on both geometric (synthetic) and power-law (real-world) topologies.

```
Vertices    Topology          Cells    Cost/Entity    Peak RAM    Crashes
------------------------------------------------------------------------
21,309      Power-law (Enron) 3,760    0.37 ms        641 MB      0
50,000      Geometric         1,180    0.52 ms        1.7 GB      0
100,000     Power-law (BA)    7,028    0.60 ms        1.3 GB      0
100,000     Geometric         2,552    0.51 ms        3.2 GB      0
250,000     Geometric         5,987    0.94 ms        7.5 GB      0
1,000,000   Geometric         23,123   0.85 ms        28.3 GB     0
```

47x growth in vertices. Per-entity cost: **flat.** Zero crashes at all scales.

## Decomposition Pipeline

SIGMA decomposes the graph into bounded cells so that no
eigensolve ever exceeds a fixed vertex limit. Global
cohomology is recovered via the Cech spectral sequence on
the nerve complex.

- Decomposition cost: O(V+E)
- Per-cell eigensolve: O(constant)
- Total cost: O(n)
- Nerve max dimension: 2
- Partition determinism: topology-dependent only

The O(n^3) eigensolve is factored into bounded subproblems.
The cube is imprisoned inside a constant.

The pipeline handles power-law graphs, geometric graphs, and
mixed topologies. Validated from V=21K to V=1M with constant
per-vertex cost.

Patent pending. Pipeline details are proprietary.

## Architecture

```
Knowledge Graph
      |
      v
  Sheaf Construction (restriction maps, contractivity enforced)
      |
      v
  Multi-stage Decomposition Pipeline (O(V+E))
      |
      v
  Per-Cell Eigensolves (bounded, independent)
      |
      v
  Nerve Assembly (Cech spectral sequence)
      |
      v
  Contradiction Report (locations, severity, algebraic proof)
```

## Multi-Seed Reproducibility

```
Seed      Time     ms/vertex    Cells    Nerve Edges    Max Dim
---------------------------------------------------------------
42        34.0s    0.433        3,760    254            2
137       25.8s    0.451        3,760    254            2
2718      21.1s    0.374        3,760    254            2
31415     21.1s    0.370        3,760    254            2
```

3,760 cells, 254 nerve edges, max dim 2: **identical across all seeds.** The partition structure depends only on graph topology, not sheaf data. Deterministic. Reproducible. Every time.

## What This Is Not

- **Not an LLM.** SIGMA does not generate text. It verifies structural consistency.
- **Not a constraint solver.** SAT/SMT check logical satisfiability. SIGMA detects topological obstructions.
- **Not a GPU product.** The architecture made the GPU irrelevant for this problem class.

## Status

- Provisional patent filed (U.S. App# 64/023,418, March 2026)
- ICML 2026 AI4Math Workshop submission in progress (deadline May 25)
- Preprint: [Zenodo DOI 10.5281/zenodo.19598076](https://zenodo.org/records/19598076)
- HuggingFace demo: [jasonlvolk/sigma-enron-demo](https://huggingface.co/spaces/jasonlvolk/sigma-enron-demo)

## Applications

- **Legal:** Circuit split detection, contract contradiction verification, eDiscovery
- **Financial:** Regulatory filing consistency, AML/KYC transaction graph verification
- **Compliance:** Cross-jurisdictional regulatory conflict detection
- **AI Safety:** Post-generation verification for LLM outputs, agent belief coherence

## Contact

Jason Volk
[jason@invariant.pro](mailto:jason@invariant.pro)
[invariant.pro](https://invariant.pro)

## License

All rights reserved. Contact for licensing inquiries.
