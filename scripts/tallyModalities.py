#!/usr/bin/env python3
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

README = Path("README.md")
SVG_OUTPUT = Path(".github/modality-badge.svg")
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
    "workflow development": "Workflow development",
    "workflows": "Workflow development",
    "development": "Workflow development",
    "other": "Other",
}

# Color palette for modalities (GitHub-style colors)
COLORS: Dict[str, str] = {
    "Bulk-Transcriptomics": "#e34c26",
    "scRNA-Seq": "#3572A5",
    "Bulk-Epigenetics": "#178600",
    "scATAC-Seq": "#89e051",
    "10x Multiome": "#f1e05a",
    "ResolveOME": "#b07219",
    "Spatial": "#555555",
    "10x Visium": "#4F5D95",
    "10x Xenium": "#DA5B0B",
    "Metagenomics": "#701516",
    "Workflow development": "#384d54",
    "Other": "#cccccc",
}


def normalize(modality: str) -> str:
    m = modality.strip()
    if not m:
        return ""
    key = m.lower()
    return ALIASES.get(key, m)


def extract_modalities_from_markdown(md_text: str) -> List[str]:
    modalities: List[str] = []
    in_counts_section = False
    for line in md_text.splitlines():
        # Skip the generated counts section entirely
        if START in line:
            in_counts_section = True
            continue
        if END in line:
            in_counts_section = False
            continue
        if in_counts_section:
            continue
        if not line.startswith("|"):
            continue
        if re.match(r"^\|\s*Project\s*\|", line):
            continue
        if re.match(r"^\|\s*-+\s*\|", line):
            continue
        cells = [c.strip() for c in line.split("|")]
        # Expect at least 4 cells: leading empty, Project, Modality, Repo/Count, trailing empty
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


def get_color(modality: str) -> str:
    """Get color for a modality, or generate a default one."""
    return COLORS.get(modality, "#cccccc")


def build_badge_svg(counts: Counter) -> str:
    """Build an SVG badge similar to GitHub's language bar."""
    if not counts:
        return ""
    
    total = sum(counts.values())
    rows: List[Tuple[str, int]] = sorted(
        counts.items(), key=lambda x: (-x[1], x[0].lower())
    )
    
    # SVG dimensions
    width = 600
    bar_height = 8
    legend_item_height = 25
    legend_height = len(rows) * legend_item_height
    total_height = bar_height + 20 + legend_height
    
    # Build bar segments
    x_pos = 0
    bar_rects = []
    for modality, count in rows:
        percentage = (count / total) * 100
        segment_width = (count / total) * width
        color = get_color(modality)
        # Escape special characters in modality name for SVG
        modality_escaped = modality.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        bar_rects.append(
            f'    <rect x="{x_pos:.2f}" y="0" width="{segment_width:.2f}" height="{bar_height}" '
            f'fill="{color}">\n'
            f'      <title>{modality_escaped}: {count} ({percentage:.1f}%)</title>\n'
            f'    </rect>'
        )
        x_pos += segment_width
    
    # Build legend
    legend_items = []
    y_pos = bar_height + 20
    for modality, count in rows:
        percentage = (count / total) * 100
        color = get_color(modality)
        # Escape special characters in modality name for SVG
        modality_escaped = modality.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        legend_items.append(
            f'    <circle cx="6" cy="{y_pos}" r="5" fill="{color}"/>\n'
            f'    <text x="18" y="{y_pos + 4}" class="legend-text">{modality_escaped}</text>\n'
            f'    <text x="{width - 10}" y="{y_pos + 4}" class="legend-percent" text-anchor="end">'
            f'{percentage:.1f}% ({count})</text>'
        )
        y_pos += legend_item_height
    
    svg = f'''<svg width="{width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .legend-text {{ 
      font: 12px -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; 
      fill: #24292f; 
    }}
    .legend-percent {{ 
      font: 12px -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; 
      fill: #656d76; 
      font-weight: 600;
    }}
  </style>
  <g id="bar">
{chr(10).join(bar_rects)}
  </g>
  <g id="legend">
{chr(10).join(legend_items)}
  </g>
</svg>'''
    
    return svg


def build_table(counts: Counter) -> str:
    """Build a simple markdown table (fallback)."""
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
    """Insert badge reference and table into README."""
    section = (
        f"{START}\n"
        f"\n"
        f"### Modality Distribution\n\n"
        f'<p align="center">\n'
        f'  <img src=".github/modality-badge.svg" alt="Modality Distribution" />\n'
        f'</p>\n\n'
        f"<details>\n"
        f"<summary>View as table</summary>\n\n"
        f"{table_md}\n\n"
        f"</details>\n"
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
    
    # Generate SVG and save to file
    badge_svg = build_badge_svg(counts)
    SVG_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    SVG_OUTPUT.write_text(badge_svg, encoding="utf-8")
    print(f"SVG badge written to {SVG_OUTPUT}")
    
    # Generate table
    table_md = build_table(counts)
    
    # Update README
    new_md = upsert_section(md_text, table_md)
    
    if new_md != md_text:
        README.write_text(new_md, encoding="utf-8")
        print("README.md updated with modality counts.")
    else:
        print("No changes to README.md.")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
