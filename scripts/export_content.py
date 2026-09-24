"""Export the editable Excel content sheet as static site data.

Usage: python3 scripts/export_content.py
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "content" / "homepage_content.xlsx"
OUTPUT = ROOT / "content-data.js"
NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with zipfile.ZipFile(path) as archive:
        try:
            strings_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            strings = ["".join(node.itertext()) for node in strings_root.findall("x:si", NS)]
        except KeyError:
            strings = []

        worksheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        rows = []
        for row in worksheet.findall(".//x:sheetData/x:row", NS):
            if int(row.attrib.get("r", "0")) < 6:
                continue
            values: dict[str, str] = {}
            for cell in row.findall("x:c", NS):
                column = re.match(r"[A-Z]+", cell.attrib.get("r", ""))
                if not column:
                    continue
                value = cell.find("x:v", NS)
                if cell.attrib.get("t") == "s" and value is not None:
                    text = strings[int(value.text or "0")]
                elif cell.attrib.get("t") == "inlineStr":
                    inline = cell.find("x:is", NS)
                    text = "".join(inline.itertext()) if inline is not None else ""
                else:
                    text = value.text if value is not None and value.text is not None else ""
                values[column.group()] = text
            if values.get("A"):
                rows.append(values)
        return rows


def main() -> None:
    rows = read_rows(WORKBOOK)
    translations: dict[str, dict[str, str]] = {"en": {}, "zh": {}, "ko": {}}
    assets: dict[str, str] = {}
    links: dict[str, str] = {}
    project_tasks: list[tuple[float, str]] = []
    seen: set[str] = set()

    for row in rows:
        key = row["A"].strip()
        if key in seen:
            raise ValueError(f"Duplicate content ID: {key}")
        seen.add(key)
        kind = row.get("D", "").strip()
        if kind in {"Text", "Link"}:
            for lang, col in (("en", "E"), ("zh", "F"), ("ko", "G")):
                value = row.get(col, "").strip()
                if not value:
                    raise ValueError(f"Missing {lang} copy for {key}")
                translations[lang][key] = value
            if row.get("C") == "Project bullet list":
                project_tasks.append((float(row.get("I") or 0), key))
            if kind == "Link":
                target = row.get("H", "").strip()
                if not (target.startswith("#") or target.startswith("https://")):
                    raise ValueError(f"Invalid link for {key}: {target}")
                links[key] = target
        elif kind == "Image":
            target = row.get("H", "").strip()
            if not target.startswith("assets/"):
                raise ValueError(f"Image must be in assets/: {key}")
            if not (ROOT / target).is_file():
                raise ValueError(f"Image file missing: {target}")
            assets[key] = target
        else:
            raise ValueError(f"Unknown content type for {key}: {kind}")

    all_text = " ".join(value for copy in translations.values() for value in copy.values())
    if re.search(r"\bGPA\b|3[.]12", all_text, re.IGNORECASE):
        raise ValueError("GPA content must not be published")

    payload = {
        "translations": translations,
        "assets": assets,
        "links": links,
        "lists": {"projectTasks": [key for _, key in sorted(project_tasks)]},
    }
    OUTPUT.write_text(
        "// Generated from content/homepage_content.xlsx. Edit the workbook, then rerun scripts/export_content.py.\n"
        "window.SITE_CONTENT = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"Exported {len(rows)} content rows to {OUTPUT.name}")


if __name__ == "__main__":
    main()
