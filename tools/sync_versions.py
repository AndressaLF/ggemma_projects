#!/usr/bin/env python3
"""Sincroniza versões das ferramentas na vitrine a partir dos pyproject.toml irmãos.

Uso (na pasta ggemma_projects):
  python tools/sync_versions.py
  python tools/sync_versions.py --check   # só verifica; exit 1 se desatualizado
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
DOCS = ROOT / "docs"
README = ROOT / "README.md"
TOML_CFG = Path(__file__).resolve().parent / "versions.toml"
VERSIONS_JSON = DOCS / "assets" / "versions.json"

# Marcadores HTML: <span data-version="ID">...</span>
SPAN_RE = re.compile(
    r'(<span\s+[^>]*data-version=["\']([^"\']+)["\'][^>]*>)(.*?)(</span>)',
    re.IGNORECASE | re.DOTALL,
)
# Marcadores Markdown/HTML comentário: <!-- ver:ID -->...<!-- /ver -->
MD_RE = re.compile(
    r"<!--\s*ver:([a-z0-9_]+)\s*-->(.*?)<!--\s*/ver\s*-->",
    re.IGNORECASE | re.DOTALL,
)


def _parse_simple_toml(text: str) -> dict[str, dict[str, object]]:
    """Parser mínimo para o versions.toml deste projeto (sem dependência externa)."""
    tools: dict[str, dict[str, object]] = {}
    current: str | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"\[tools\.([a-z0-9_]+)\]", line, re.I)
        if m:
            current = m.group(1)
            tools[current] = {}
            continue
        if current is None or "=" not in line:
            continue
        key, val = [p.strip() for p in line.split("=", 1)]
        if val.startswith("["):
            items = re.findall(r'"([^"]+)"', val)
            tools[current][key] = items
        else:
            tools[current][key] = val.strip().strip('"').strip("'")
    return tools


def read_pyproject_version(folder: Path) -> str | None:
    py = folder / "pyproject.toml"
    if not py.is_file():
        return None
    text = py.read_text(encoding="utf-8")
    # Prefer [project] version = "x.y.z"
    m = re.search(
        r'(?m)^version\s*=\s*["\']([^"\']+)["\']',
        text,
    )
    return m.group(1).strip() if m else None


def resolve_versions(cfg: dict[str, dict[str, object]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for tool_id, meta in cfg.items():
        folders = meta.get("pastas") or []
        if isinstance(folders, str):
            folders = [folders]
        version = None
        for name in folders:
            version = read_pyproject_version(PARENT / str(name))
            if version:
                break
        if not version:
            version = str(meta.get("fallback") or meta.get("label") or "?")
        # label override (ex.: suite) — se definido, usa o rótulo em vez do número
        if meta.get("label"):
            out[tool_id] = str(meta["label"])
        else:
            out[tool_id] = version
        # versão numérica crua também (para JSON)
        out[f"{tool_id}__raw"] = version if not meta.get("label") else str(meta.get("fallback") or version)
        if meta.get("label_detail"):
            out[f"{tool_id}__detail"] = str(meta["label_detail"])
    return out


def display_version(tool_id: str, versions: dict[str, str]) -> str:
    return versions.get(tool_id, "?")


def replace_spans(text: str, versions: dict[str, str]) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        tool_id = m.group(2)
        if tool_id not in versions:
            return m.group(0)
        new_inner = versions[tool_id]
        count += 1
        return f"{m.group(1)}{new_inner}{m.group(4)}"

    return SPAN_RE.sub(repl, text), count


def replace_md_markers(text: str, versions: dict[str, str]) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        tool_id = m.group(1)
        if tool_id not in versions:
            return m.group(0)
        count += 1
        return f"<!-- ver:{tool_id} -->{versions[tool_id]}<!-- /ver -->"

    return MD_RE.sub(repl, text), count


def sync_file(path: Path, versions: dict[str, str], check_only: bool) -> bool:
    original = path.read_text(encoding="utf-8")
    if not original.strip():
        print(f"  [skip-empty] {path.relative_to(ROOT)}")
        return False
    updated, n1 = replace_spans(original, versions)
    updated, n2 = replace_md_markers(updated, versions)
    # aliases de detalhe batimetria no README
    if "batimetria_kml_shape__detail" in versions:
        detail = versions["batimetria_kml_shape__detail"]
        for key in ("batimetria_kml_shape__detail", "batimetria_kml_shape_detail"):
            updated2, n3 = re.subn(
                rf"(<!--\s*ver:{key}\s*-->)(.*?)(<!--\s*/ver\s*-->)",
                rf"\g<1>{detail}\g<3>",
                updated,
                flags=re.I | re.DOTALL,
            )
            updated = updated2
            n2 += n3
    changed = updated != original
    if changed and not check_only:
        path.write_text(updated, encoding="utf-8", newline="\n")
    if n1 or n2:
        status = "check-fail" if (check_only and changed) else ("updated" if changed else "ok")
        print(f"  [{status}] {path.relative_to(ROOT)} (spans={n1}, markers={n2})")
    return changed


def write_versions_json(versions: dict[str, str], check_only: bool) -> bool:
    payload = {
        "extrator_info_files": versions.get("extrator_info_files"),
        "surveyanchor": versions.get("surveyanchor"),
        "batimetria_kml_shape": versions.get("batimetria_kml_shape"),
        "batimetria_kml_shape_detail": versions.get("batimetria_kml_shape__detail"),
        "source": "tools/sync_versions.py",
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if VERSIONS_JSON.exists() and VERSIONS_JSON.read_text(encoding="utf-8") == text:
        print(f"  [ok] {VERSIONS_JSON.relative_to(ROOT)}")
        return False
    if check_only:
        print(f"  [check-fail] {VERSIONS_JSON.relative_to(ROOT)}")
        return True
    VERSIONS_JSON.parent.mkdir(parents=True, exist_ok=True)
    VERSIONS_JSON.write_text(text, encoding="utf-8", newline="\n")
    print(f"  [updated] {VERSIONS_JSON.relative_to(ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Não grava; falha se houver drift")
    args = parser.parse_args()

    cfg = _parse_simple_toml(TOML_CFG.read_text(encoding="utf-8"))
    versions = resolve_versions(cfg)
    print("Versões resolvidas:")
    for k, v in sorted(versions.items()):
        if k.endswith("__raw") or k.endswith("__detail"):
            continue
        print(f"  {k}: {v}")

    targets = [
        DOCS / "index.html",
        DOCS / "extrator.html",
        DOCS / "surveyanchor.html",
        DOCS / "batimetria.html",
        DOCS / "sobre.html",
        README,
    ]
    any_changed = False
    print("Arquivos:")
    for path in targets:
        if path.is_file():
            any_changed |= sync_file(path, versions, args.check)
    any_changed |= write_versions_json(versions, args.check)

    if args.check and any_changed:
        print("Drift detectado. Rode: python tools/sync_versions.py")
        return 1
    print("Pronto." if not args.check else "OK — sem drift.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
