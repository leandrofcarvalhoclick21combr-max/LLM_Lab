from pathlib import Path


def find_project_root(start: str | Path) -> Path:
    current = Path(start).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "experiments" / "index.yaml").is_file() and (
            candidate / "configs"
        ).is_dir():
            return candidate
    raise ValueError(f"Raiz do LLM Lab não encontrada a partir de: {start}")
