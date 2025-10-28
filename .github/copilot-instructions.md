# Copilot Instructions

## Repository Context
- This repo is a narrative and architectural staging ground for the LLW stack, not an implementation codebase.
- LLW (fields/units/interactions) is the physics-aligned substrate; LLWΦ carries semantic policy and interpretation layers.
- Documents mix technical roadmaps with personal narrative; preserve the author’s voice and tone when editing prose.

## Key Knowledge Sources
- `## Flip overview.md` — canonical plan for the "flip" that naturalizes LLW and externalizes LLWΦ semantics; study its op families, invariants, and workflow.
- `Analyzing the flip.txt` — details cryptographic "device-as-witness" integrations and how provenance hashing should evolve.
- `longitudinal-selfDive.md` — forensic/psychological synthesis that explains the stakeholder context; informs tone and intent.
- `Lumen_OG-Gr0k.txt` — describes the Lumen assembly concept used when referencing quantum/bio-inspired execution.
- `README.md` — front-door narrative, linking this repo to adjacent ones (AI-FORENSICS, FALSIFIABLE-PROFILE, etc.).

## Working Practices
- When proposing structure changes, reference LLW entities: units, fields, resources, couplings, invariants.
- Prefer adding specs or outlines over stub code unless the user supplies concrete schematics; prototypes can live under `spec/` or `scripts/` with clear TODOs.
- Keep tables, bullet hierarchies, and citation footers intact; they are often cross-referenced in other docs.
- Use plain ASCII unless a document already employs special glyphs; respect existing emphasis (caps, italics, emoji).

## Build & Automation Notes
- GitHub Action `.github/workflows/build-lexeme-encyclopedia.yml` expects `scripts/build_lexeme_encyclopedia.py`; confirm or add the script before relying on the workflow.
- No tests or linting pipelines exist yet; manual review and clear prose diffs are the primary validation method.

## Integration & Security Guidance
- Provenance features hinge on Merkle roots, deterministic numerics, and threshold-crypto witnesses; align any new artifacts with that model.
- When touching access-control narratives, reuse terminology such as `DEVICE_ATTEST`, `TSS_PARTIAL`, `NORMALFORMHASH`, and "quorum" semantics from `Analyzing the flip.txt`.

## Collaboration Pattern
- Surface uncertainties (missing scripts, unclear invariants) back to the user rather than guessing; many plans are aspirational.
- Call out dependencies on external repos when documenting workflows, and note when content diverges from the described ecosystem.
