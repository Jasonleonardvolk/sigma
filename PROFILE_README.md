## Jason Leonard Volk

Founder, [Invariant Research](https://invariant.pro). I build deterministic verification infrastructure for AI systems that mutate state.

Most AI verification is probabilistic: a model judges whether another model's output looks right. Invariant takes a different path. SIGMA computes structural admissibility with cellular sheaf cohomology, SATYA wraps runtime outputs and workflow transitions, and SVR records the result as a signed, independently checkable JSON receipt. Every verdict is deterministic and reproducible, with no ML and no GPU in the verification path.

### Selected work

- [sigma-guard](https://github.com/Jasonleonardvolk/sigma-guard): structural contradiction detection for knowledge graphs, agent state, and LLM output. 35 microsecond median per-edit at 5M vertices, zero drift, zero ML. Python library, CLI, and MCP server. On PyPI as `sigma-guard`.
- [svr-verify](https://github.com/Jasonleonardvolk/svr-verify): the standalone Signed Verification Receipt (SVR) verifier. Checks the Ed25519 signature and structure of a receipt with zero engine dependency. On PyPI as `svr-verify`.
- [Incremental Sheaf Cohomology on Cellular Complexes](https://arxiv.org/abs/2606.04227) (arXiv:2606.04227): the O(1)-in-n lazy edit-processing result behind the engine.
- Hugging Face: [SATYA SVR Verifier](https://huggingface.co/spaces/jasonlvolk/satya-svr-verifier) (also an MCP tool), [receipt fixtures](https://huggingface.co/datasets/jasonlvolk/svr-receipts-examples), and the [SIGMA Enron demo](https://huggingface.co/spaces/jasonlvolk/sigma-enron-demo).

### Contact

[invariant.pro](https://invariant.pro) | jason@invariant.pro
