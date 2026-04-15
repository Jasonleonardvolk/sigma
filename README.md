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

Six layers, each enabling the next:

1. **Hub Extraction** -- Remove vertices with degree > mean + 2*std. Makes graph spectrally tractable by removing vertices whose degree dominates the Fiedler vector.

2. **Hub Neighbor Freeze** -- Freeze 1-hop non-hub neighbors during boundary expansion. Prevents the "density shadow" from inflating cells past v_max.

3. **Connected Components** -- BFS detection of disconnected islands after hub removal. On Enron, hub removal shatters the graph into 1,209 components (1 giant at 17,011, 1,208 tiny).

4. **BFS Balanced Partitioning** -- For large components (V > 5,000), carve connected chunks of ~v_max via BFS instead of spectral bisection. O(V+E). Eliminates the spectral bottleneck entirely.

5. **K-Doubling Cap** -- For cells with sheaf Laplacian dim > 1,600, one ARPACK attempt at k=30, immediate fallback if ill-conditioned.

6. **Clean Split** -- Post-expansion re-splits with no boundary vertex duplication. Nerve stays at max dimension 2.

The pipeline is a dependency chain: hub extraction creates disconnection, connected components detect it, BFS resolves it.

## Architecture

```
Knowledge Graph
      |
      v
  Sheaf Construction (restriction maps, Purity Gate: sigma_max <= 0.99)
      |
      v
  Hub Extraction (degree > mean + 2*std)
      |
      v
  Connected Components (BFS, O(V+E))
      |
      v
  BFS Balanced Partitioning (giant component -> bounded chunks)
      |
      v
  Per-Cell Eigensolves (H^1, lambda_2, Dirichlet energy)
      |
      v
  Nerve Assembly (Cech spectral sequence, max dim 2)
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
- Preprint: [Zenodo DOI 10.5281/zenodo.19360505](https://zenodo.org/records/19360505)
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
