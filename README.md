# brand-os (Spec-Driven Mono-Repo)

This repository is a minimal, production-oriented spec-driven mono-repo for content generation.

Spec-Driven Development
- All runtime behavior is driven by YAML specs (see `specs/generation.spec.yaml`).
- Specs declare `model`, `temperature`, `input_dir`, `output_dir`, and templates.

Constitution (AppSec)
- `shared/constitution.yaml` contains rules such as `max_input_file_size_mb`, `max_tokens_allowed`, and flags to restrict prompt injection and path traversal.
- `shared/security.py` enforces file safety, masks secrets, and sanitizes inputs.

How to run (uv)
1. Create a virtual env: `uv venv`.
2. Add deps: `uv add`.
3. Run generation: `uv run brand-generate --spec specs/generation.spec.yaml`

Extending to publishing
- Add a `publishing` package and declare publishing steps in a spec. Keep enforcement via constitution.

Enforcing security rules
- Always validate new specs against `shared/constitution.yaml`.
- Use `shared/security.py` helpers when handling file paths and user inputs.
