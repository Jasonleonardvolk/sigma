# SIGMA

**Pre-commit structural verification for AI systems that mutate state.**

Detects structural contradictions that cannot be resolved by any local adjustment.
Algebraic verification via cellular sheaf cohomology. Linear cost. No GPU.

---

## AI4Math 2026 Paper

SIGMA was accepted as a poster at the **3rd AI for Math Workshop at ICML 2026** (Seoul, July 11).

The paper studies update-time structural verification for evolving agent state. SIGMA is not a replacement for Lean or proof assistants. Lean certifies formal proof artifacts; SIGMA targets the mutable pre-commit layer around memory writes, dependency proposals, claim graphs, tool traces, and structured reasoning state.

**Paper framing:**
- ProofDAG is a calibration benchmark for invariant preservation.
- Lean/mathlib validates the exact-loader path on formal structure.
- The LLM proposed-edge audit is membership-catchable and is treated as pre-commit integration validation.
- The gluing witness shows the baseline separation: membership can pass while global compatibility fails.
- The 990-lemma study identifies loader fidelity as the binding constraint.
- The 5M-vertex run demonstrates streaming maintenance at scale.

**Paper:** [arXiv 2606.04227](https://arxiv.org/abs/2606.04227) | **Project:** [invariant.pro](https://invariant.pro)

---

## The Problem

AI systems produce outputs that look locally consistent but are globally incompatible. Every adjacent pair of claims checks out. The chain as a whole is contradictory. SIGMA targets a complementary verification regime: global structural compatibility in evolving represented state.

SIGMA is a pre-commit structural verification layer. It takes structured state (a graph of entities and relationships), constructs a cellular sheaf over it, and uses sheaf cohomology to detect irreconcilable structural contradictions. The detection is algebraic, not heuristic. SIGMA detects structural inconsistency relative to the represented sheaf. It verifies the encoded structure, not semantic truth over raw text.

## Key Result: Streaming Verification at Scale

|  |  |
| --- | --- |
| **Vertices** | 5,000,000 (single commodity machine) |
| **Median per-edit latency** | 35 us |
| **Assembled-cohomology drift** | 0 |
| **Amortized cost** | O(1) in graph size |
| **Scaling exponent** | 0.19 (R^2 = 0.975, 21K to 1M) |

The sheaf Laplacian at 5M vertices is massive. A dense eigensolve is infeasible. SIGMA decomposes the graph into bounded cells so no eigensolve ever exceeds a fixed vertex limit. Global cohomology is assembled from local cell contributions via Mayer-Vietoris:

```
O(n^3) -> O(n/v_max) * O(v_max^3) = O(n) * constant
```

## Scale Validation

```
Vertices    Cells      Edit (med)   Drift
-------------------------------------------
21K         639        31 us        0
100K        890        46 us        0
1M          8,663      63 us        0
5M          25,473     35 us        0
```

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

  Claim 2 <-> Claim 3:  irreconcilable (sheaf obstruction)
                        extension vs original deadline activation

  Claim 3 <-> Claim 6:  irreconcilable (sheaf obstruction)
                        penalty triggers but none assessed

  Claim 4 <-> Claim 6:  irreconcilable (sheaf obstruction)
                        coverage scope vs no action taken

False positives:  0
Detection time:   47 ms
```

## Architecture

```
Agent / LLM proposes state update
      |
      v
  Loader builds represented state edit
      |
      v
  SIGMA structural verifier
      |
      +-> commit
      +-> block
      +-> decompose / request missing structure
      |
      v
  receipt / audit trail
```

## What This Is Not

- **Not an LLM.** SIGMA does not generate text. It verifies structural consistency.
- **Not a replacement for Lean.** Lean certifies formal proof artifacts. SIGMA targets the mutable pre-commit state layer.
- **Not a truth oracle over raw text.** SIGMA verifies the encoded representation. If the loader erases mathematical structure, the verifier cannot recover it.
- **Not a constraint solver.** SAT/SMT check logical satisfiability. SIGMA detects topological obstructions to global gluing.
- **Not a GPU product.** The architecture made the GPU irrelevant for this problem class.

## Status

- **Accepted Poster,** 3rd AI for Math Workshop at ICML 2026 (Seoul, July 11)
- Nonprovisional patent filed (U.S. App# 19/649,080, 43 claims, 8 independent)
- arXiv: [2606.04227](https://arxiv.org/abs/2606.04227)
- HuggingFace demo: [jasonlvolk/sigma-enron-demo](https://huggingface.co/spaces/jasonlvolk/sigma-enron-demo)

## Reproducibility Status

This repository contains public SIGMA code, demos, and supporting artifacts. A camera-ready artifact tag will be created for the AI4Math 2026 version.

## Applications

- **AI Safety:** Pre-commit verification for LLM outputs, agent state coherence, memory writes
- **Scientific AI:** Structural verification for evolving claim graphs, hypotheses, and evidence dependencies
- **Legal:** Contract contradiction verification, regulatory conflict detection
- **Financial:** Filing consistency, transaction graph verification

## Contact

Jason Volk <jason@invariant.pro>
[invariant.pro](https://invariant.pro)

## License

All rights reserved. Contact for licensing inquiries.
