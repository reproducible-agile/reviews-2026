#!/usr/bin/env python3
"""Harvest metadata needed for codecheck.yml files of AGILE reproducibility reviews.

Reusable across years. Given a mapping of submissions to their published article
number, report DOI and (for OSF-hosted reports) the OSF node GUID, this script:

  1. queries Crossref for each paper DOI  -> title + authors + author ORCIDs
  2. queries the OSF API for each report node -> codechecker(s) (contributors)
     and, where available, their ORCID (note: OSF stores ORCID inconsistently -
     often NOT in `social.orcid`; treat OSF ORCIDs as best-effort only)
  3. downloads the report PDF from each OSF node into reports/<id>/

The authoritative codechecker name, ORCID, check date, repository and one-word
reproduction outcome are printed on the title page / "Reproduction metadata"
table of each report PDF - always cross-check the PDF, it wins over the API.

Copernicus/Crossref deposits carry few author ORCIDs and OSF profiles few
reviewer ORCIDs, so a manual enrichment round (ORCID API lookups, author
landing pages) is expected afterwards - see CLAUDE.md.

Usage: edit REVIEWS below for the current year, then `python3 fetch_report_metadata.py`.
Only depends on the Python standard library.
"""
import json, os, time, urllib.request

MAILTO = "daniel.nuest@tu-dresden.de"
UA = f"codecheck-agile/1.0 (mailto:{MAILTO})"
REPORTS_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "reports")
GISS_VOLUME = 7  # AGILE GIScience Series volume for the year (2026 -> 7)

# submission_id -> (published article number, report DOI, OSF node GUID or None)
# None GUID = report not on OSF (e.g. ResearchEquals) -> handle its PDF manually.
REVIEWS = {
    7:  (3,  "https://doi.org/10.17605/OSF.IO/R2674", "r2674"),
    8:  (2,  "https://doi.org/10.17605/OSF.IO/DZT8C", "dzt8c"),
    10: (4,  "https://doi.org/10.17605/OSF.IO/ZPURT", "zpurt"),
    12: (9,  "https://doi.org/10.17605/OSF.IO/DZURB", "dzurb"),
    13: (13, "https://doi.org/10.17605/OSF.IO/YH8F6", "yh8f6"),
    15: (5,  "https://doi.org/10.17605/OSF.IO/KCPZE", "kcpze"),
    16: (11, "https://doi.org/10.17605/OSF.IO/DA3Z4", "da3z4"),
    17: (18, "https://doi.org/10.17605/OSF.IO/75PWN", "75pwn"),
    21: (16, "https://doi.org/10.17605/OSF.IO/BV4MK", "bv4mk"),
    22: (8,  "https://doi.org/10.17605/OSF.IO/HETV8", "hetv8"),
    26: (17, "https://doi.org/10.53962/pdw8-n5v0",    None),   # ResearchEquals
    29: (10, "https://doi.org/10.17605/OSF.IO/VCGY2", "vcgy2"),
    31: (6,  "https://doi.org/10.17605/OSF.IO/WH6GD", "wh6gd"),
    33: (12, "https://doi.org/10.17605/OSF.IO/8C3VF", "8c3vf"),
}


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return json.load(urllib.request.urlopen(req, timeout=30))


def crossref_authors(doi):
    m = _get(f"https://api.crossref.org/works/{doi}")["message"]
    authors = [{
        "name": (a.get("given", "") + " " + a.get("family", "")).strip(),
        "orcid": (a.get("ORCID") or "").replace("https://orcid.org/", ""),
    } for a in m.get("author", [])]
    return {"title": (m.get("title") or [""])[0], "authors": authors}


def osf_checkers(guid):
    out = []
    c = _get(f"https://api.osf.io/v2/nodes/{guid}/contributors/")
    for co in c.get("data", []):
        u = co["embeds"]["users"]["data"]
        social = u["attributes"].get("social") or {}
        out.append({"name": u["attributes"]["full_name"], "osf": u["id"],
                    "orcid": social.get("orcid", "")})
    return out


def osf_download_pdf(guid, dest_folder):
    f = _get(f"https://api.osf.io/v2/nodes/{guid}/files/osfstorage/")
    pdfs = [d for d in f.get("data", [])
            if d["attributes"]["kind"] == "file" and d["attributes"]["name"].lower().endswith(".pdf")]
    if not pdfs:
        return None
    pdfs.sort(key=lambda d: -(d["attributes"].get("size") or 0))
    p = pdfs[0]
    os.makedirs(dest_folder, exist_ok=True)
    dest = os.path.join(dest_folder, p["attributes"]["name"])
    req = urllib.request.Request(p["links"]["download"], headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r, open(dest, "wb") as fh:
        fh.write(r.read())
    return dest


def main():
    result = {}
    for sid, (art, report_doi, guid) in sorted(REVIEWS.items()):
        paper_doi = f"10.5194/agile-giss-{GISS_VOLUME}-{art}-{2026}"
        entry = {"article": art, "paper_doi": paper_doi, "report_doi": report_doi, "osf": guid}
        try:
            entry.update(crossref_authors(paper_doi))
        except Exception as e:
            entry["crossref_error"] = str(e)
        if guid:
            folder = os.path.join(REPORTS_DIR, f"{sid:03d}")
            try:
                entry["checkers"] = osf_checkers(guid)
            except Exception as e:
                entry["osf_error"] = str(e)
            if not any(n.lower().endswith(".pdf") for n in (os.listdir(folder) if os.path.isdir(folder) else [])):
                try:
                    entry["pdf"] = osf_download_pdf(guid, folder)
                except Exception as e:
                    entry["pdf_error"] = str(e)
        result[sid] = entry
        time.sleep(0.3)
    print(json.dumps(result, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
