# SIGMA Guard

**Structural verification for graph databases.**

Your graph can pass every schema check and still contradict itself.
SIGMA Guard catches that before the write commits.

**5M vertices. 35 microseconds. Zero drift. Zero ML.**

> Note: This project is unrelated to SigmaHQ detection rules.
> SIGMA Guard is a graph consistency verification layer from
> [Invariant Research](https://invariant.pro).

## The problem no one else solves

Schema validators check shape. Constraint engines check rules.
Neither one checks whether the graph tells one consistent story.

Two nodes can individually pass every validation and still
contradict each other. In a knowledge graph, that is a
hallucination waiting to happen. In a compliance graph, that
is a regulatory finding. In an agent memory graph, that is
a wrong answer your users will see.

SIGMA Guard detects structural contradictions using sheaf
cohomology: a mathematical framework that proves whether
local claims can glue into one globally consistent assignment.
If they cannot, you get the exact edges where the contradiction
lives, a severity ranking, and a deterministic proof receipt.

Not a probability. Not a confidence score. A proof.

## Why this matters now

Every AI system that builds or mutates a graph needs this.

- **GraphRAG pipelines** retrieve contradictory facts into the same
  context window. SIGMA Guard catches that before retrieval.
- **Agentic systems** accumulate state across tool calls, memory
  writes, and dependency insertions. SIGMA Guard verifies each
  mutation before commit.
- **Legal and compliance AI** must prove their outputs are
  structurally sound. SIGMA Guard produces cryptographic
  verification receipts on every check.
- **Knowledge graph ETL** merges data from multiple sources that
  may disagree. SIGMA Guard finds the disagreements that schema
  validation misses.

Colorado SB 24-205 and EU AI Act Article 15 require documentation
of AI system reliability. A SIGMA Guard receipt is a compliance
artifact.

## Performance

This is not a research prototype. This is production infrastructure.

| Metric | Value |
| --- | --- |
| Per-edit latency (median) | **35 microseconds** |
| Per-query latency | 13 microseconds |
| Validated scale | **5,000,000 vertices** |
| Cells at 5M | 25,473 |
| Scaling exponent | 0.19 (sub-linear in graph size) |
| Cohomology drift | **0 (mathematically exact)** |
| RestrictionStore memory at 5M | 0.50 MB |
| ML required | None |
| GPU required | None |
| Training data required | None |

Single machine. Intel i9-13900H, 64 GB RAM. No cluster. No cloud
dependency. Cellular Mayer-Vietoris streaming architecture reduces
per-edit verification from O(n^3) to O(1) amortized. Every edit
touches only the bounded local cell, not the global graph.

Classical sheaf cohomology recomputation costs O(n^3) per mutation.
At 5M vertices, that is mass-of-the-sun expensive. SIGMA does it
in 35 microseconds because it never recomputes the global matrix.
The partition localizes every edit to a constant-size subproblem.
The rest of the graph stays cached. Zero drift. Exact agreement
with batch recomputation at every checkpoint.

That is not an approximation. That is a theorem.

## Try it in 60 seconds

```
git clone https://github.com/Jasonleonardvolk/sigma-guard.git
cd sigma-guard
python -m venv .venv
.\.venv\Scripts\Activate.ps1       # Windows
# source .venv/bin/activate        # Mac/Linux
pip install -e .
python examples/tiny_contradiction.py
```

```
Tiny Contradiction Demo
========================================

Graph: 2 vertices, 1 edge
Policy says approved_vendor = Supplier_A
Procurement says approved_vendor = Supplier_B

Verdict: INCONSISTENT

  [CRITICAL] Policy <-> Procurement
  Structural contradiction: 'Policy' and 'Procurement' disagree
  on: approved_vendor. These claims are individually valid but
  structurally incompatible.
  Proof: sigma:proof:a1dc661d...

Elapsed: 0.59ms
```

Then run the full supply-chain demo:

```
python examples/basic_usage.py
```

Detects 7 structural contradictions, separates critical from
low-energy tension, allows a safe write, blocks a contradictory
write in under 1ms, emits proof IDs.

### With Docker

```
docker run jasonvolk/sigma-guard demo supply_chain
docker run jasonvolk/sigma-guard demo cybersecurity
docker run jasonvolk/sigma-guard demo knowledge_graph
```
