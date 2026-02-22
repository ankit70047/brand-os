# Using uv with this monorepo

This repository is a multi-package monorepo. `uv` can manage environments per
project or at the repository root.

Common workflows

- Sync/install dependencies for the repo root (current directory):

```powershell
uv sync
```

- Run a command inside the uv-managed environment without activating the shell:

```powershell
uv run -- python -V
uv run -- pip list
```

- Sync or operate on a subpackage (for example `generation`):

```powershell
uv --project generation sync
uv --project generation run -- python -m generation.engine.main
```

Activation (PowerShell)

To activate the environment in your interactive PowerShell session, run:

```powershell
.\.venv\Scripts\Activate.ps1
```

Notes

- If you prefer not to activate a shell, `uv run -- <command>` runs commands
  inside the environment directly.
- To pin dependencies, use `uv lock` to update `uv.lock` and commit it.
