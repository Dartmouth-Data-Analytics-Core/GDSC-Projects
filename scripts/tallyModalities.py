#!/usr/bin/env python3
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

README = Path("README.md")
START = "<!-- START: modality-counts -->"
END = "<!-- END: modality-counts -->"

ALIASES: Dict[str, str] = {
    # Bulk transcriptomics variants
    "bulk transcriptomics": "Bulk-Transcriptomics",
    "bulk transcriptomic": "Bulk-Transcriptomics",
    "bulk transcriptome": "Bulk-Transcriptomics",
    "rna-seq": "Bulk-Transcriptomics",
    "rnaseq": "Bulk-Transcriptomics",
    "rna seq": "Bulk-Transcriptomics",
    "rna seq.": "Bulk-Transcriptomics",

    # Single-cell gene expression
    "sc gex": "scRNA-Seq",
    "single cell rna-seq": "scRNA-Seq",
    "scrna-seq": "scRNA-Seq",
    "sc rna-seq": "scRNA-Seq",

    # ATAC-seq
    "bulk atacseq": "Bulk-Epigenetics",
    "bulk atac-seq": "Bulk-Epigenetics",
    "sc atac": "scATAC-Seq",
    "sc atac-seq": "scATAC-Seq",

    # Multiome and others
    "10x multiome": "10x Multiome",
    "resolveome": "ResolveOME",
    
    # Spatial platforms
    "spatial": "Spatial",
    "visium": "10x Visium",
    "10x visium": "10x Visium",
    "xenium": "10x Xenium",
    "xeniums": "10x Xenium",
    "10x xenium": "10x Xenium",

    # Misc
    "mgx": "Metagenomics",
    "workflow dev": "Workflow development",
    "other": "Other",
}

def normalize(modality: str) -> str:
    m = modality.strip()
    if not m:
        return ""
    key = m.lower()
    return ALIASES.get(key, m)

def extract_modalities_from_markdown(md_text: str) -> List[str]:
    modalities: List[str] = []
    for line in md_text.splitlines():
        if not line.startswith("|"):
            continue
        if re.match(r"^\|\s*Project\s*\|", line):
            continue
        if re.match(r"^\|\s*-+\s*\|", line):
            continue
        cells = [c.strip() for c in line.split("|")]
        # Expect at least 4 cells: leading empty, Project, Modality, Repo, Date, trailing empty
        if len(cells) < 4:
            continue
        modality_cell = cells[2]  # Modality is the second visible column
        if not modality_cell:
            continue
        parts = re.split(r"\s*,\s*", modality_cell)
        for p in parts:
            n = normalize(p)
            if n:
                modalities.append(n)
    return modalities


def build_table(counts: Counter) -> str:
    rows: List[Tuple[str, int]] = sorted(
        counts.items(), key=lambda x: (-x[1], x[0].lower())
    )
    lines = [
        "| Modality | Count |",
        "|----------|-------|",
    ]
    for modality, cnt in rows:
        lines.append(f"| {modality} | {cnt} |")
    return "\n".join(lines)

def upsert_section(md_text: str, table_md: str) -> str:
    section = (
        f"{START}\n"
        f"\n"
        f"### Modality counts\n\n"
        f"{table_md}\n"
        f"\n"
        f"{END}"
    )
    if START in md_text and END in md_text:
        return re.sub(
            re.compile(re.escape(START) + r".*?" + re.escape(END), re.S),
            section,
            md_text,
        )
    # If markers not present, append to end
    sep = "\n\n" if not md_text.endswith("\n") else "\n"
    return md_text + sep + section + "\n"

def main() -> int:
    if not README.exists():
        print("README.md not found at repo root.")
        return 1
    md_text = README.read_text(encoding="utf-8")
    modalities = extract_modalities_from_markdown(md_text)
    counts = Counter(modalities)
    table_md = build_table(counts)
    new_md = upsert_section(md_text, table_md)
    if new_md != md_text:
        README.write_text(new_md, encoding="utf-8")
        print("README.md updated with modality counts.")
    else:
        print("No changes to README.md.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
