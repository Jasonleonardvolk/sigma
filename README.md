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
| **Analyzed core** | 21,309 vertices, 166,039 edges (3-core) |
| **Topology** | Power-law (degree CV = 2.609, hub max degree 1,141) |
| **Verification cells** | 446 (bit-identical across 4 seeds) |
| **Nerve edges** | 70 |
| **Nerve max dimension** | 2 |
| **Sheaf Laplacian** | 170,472 x 170,472 |
| **Full decomposition time** | ~2m15s (4-seed validated) |
| **Peak memory** | ~700 MB |
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

Streaming-from-zero incremental verification on synthetic scale-free graphs,
validated to 5 million vertices. The real-world power-law result is the Enron
decomposition above.

```
Vertices    Edit Mean    Query p99    Drift    Cells
----------------------------------------------------------
100,000     0.046 ms     0.010 ms     0        421
250,000     0.051 ms     0.010 ms     0        1,096
1,000,000   0.063 ms     0.013 ms     0        4,611
5,000,000   0.035 ms     --           0        25,473
```

V grew 50x. Per-edit cost stayed **flat.** Zero drift at every checkpoint,
verified by full recomputation at 5M (incremental H^1 = 103,690 equals batch
recomputation H^1 = 103,690).

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
mixed topologies. Validated from V=21K to V=5M, with constant
per-edit cost in the streaming path.

Patent protection is being pursued. Pipeline details are proprietary.

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
Seed      Cells    Nerve Edges    Max Dim
------------------------------------------
42        446      70             2
137       446      70             2
2718      446      70             2
31415     446      70             2
```

446 cells, 70 nerve edges, max dim 2: **bit-identical across all four seeds.**
Full decomposition ran about 2m7s to 2m28s across seeds. The partition
structure depends only on graph topology, not sheaf data. Deterministic.
Reproducible. Every time.

## What This Is Not

- **Not an LLM.** SIGMA does not generate text. It verifies structural consistency.
- **Not a constraint solver.** SAT/SMT check logical satisfiability. SIGMA detects topological obstructions.
- **Not a GPU product.** The architecture made the GPU irrelevant for this problem class.

## Status

- **Patent protection:** patent applications are on file covering the methods described here (details under NDA)
- Paper: [Incremental Sheaf Cohomology on Cellular Complexes (arXiv:2606.04227)](https://arxiv.org/abs/2606.04227)
- Submitted to the ICML 2026 AI4Math Workshop (Submission #192)
- Preprint: [Zenodo DOI 10.5281/zenodo.19598076](https://zenodo.org/records/19598076)
- Open source: [sigma-guard](https://github.com/Jasonleonardvolk/sigma-guard) and [svr-verify](https://github.com/Jasonleonardvolk/svr-verify), both on PyPI
- Hugging Face: [SATYA SVR Verifier](https://huggingface.co/spaces/jasonlvolk/satya-svr-verifier) (also an MCP tool) and the [SIGMA Enron demo](https://huggingface.co/spaces/jasonlvolk/sigma-enron-demo)

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
