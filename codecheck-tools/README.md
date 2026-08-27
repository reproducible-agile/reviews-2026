# codecheck-tools

Helper scripts for producing the `reports/<submission-id>/codecheck.yml` files
that register each AGILE reproducibility review with the CODECHECK register
(https://github.com/codecheckers/register, see issue linked from the year's
`codecheck.yml.template`). Creating these files is a **recurring annual task**
at the end of each year's review round. Both scripts use only the Python
standard library.

## Workflow

1. **`fetch_report_metadata.py`** — edit the `REVIEWS` mapping (submission id →
   published article number, report DOI, OSF node GUID) and `GISS_VOLUME` for
   the year, then run it. It:
   - pulls paper title + author ORCIDs from **Crossref** (`api.crossref.org`)
     for each `10.5194/agile-giss-<vol>-<art>-<year>` DOI;
   - pulls codechecker(s) (OSF contributors) from the **OSF API**
     (`api.osf.io/v2`) for each report node;
   - downloads each OSF report PDF into `reports/<id>/`.

2. Read each report PDF's title page / "Reproduction metadata" table for the
   authoritative **codechecker name + ORCID, date of check, and the one-word
   reproduction outcome** — these are *not* reliably in the APIs and override
   them. (Copernicus deposits carry few author ORCIDs; OSF profiles store ORCID
   inconsistently — Crossref/OSF ORCIDs are best-effort only.)

3. **Author ORCIDs — from the Copernicus article PDF** (authoritative). Download
   `https://agile-giss.copernicus.org/articles/<vol>/<art>/<year>/agile-giss-<vol>-<art>-<year>.pdf`
   into `reports/<id>/`, then extract ORCIDs from the FlateDecode streams (they
   are link annotations, not visible text: decompress each stream and grep
   `orcid.org/<id>`), resolve each id to a name via `pub.orcid.org/v3.0/<id>/person`,
   and match to the author list.

4. **Repository — from the article's "Data and Software Availability" section**
   (the report table is often `NA`). May be GitHub, a Zenodo/Figshare DOI or
   Hugging Face; the published paper sometimes reveals a permanent repo replacing
   an anonymised review link. Prefer `github.com/reproducible-agile/<fork>` if the
   checker made one, else the authors' upstream repo, else the reviewer's repo.

5. **`gen_codecheck.py`** — put the assembled per-submission values into the
   `data` dict (with the `AUTHOR_ORCID` and `MANIFEST` override maps) and run it
   to write all `codecheck.yml` files. Certificates map by ascending submission id
   onto the block reserved in the register issue. The `data` block doubles as the
   record of what was written for the year.

6. Enrichment round for anything still missing: ORCIDs not in any PDF → query
   `pub.orcid.org/v3.0/expanded-search` and **let the maintainer pick** from
   candidates (do not auto-assign; some authors simply have none). Refine
   summaries from OSF/ResearchEquals metadata + the report PDF summary section,
   and fill each `manifest` from the report's "Summary of output files generated".

## Notes / gotchas

- Not every published paper has a review — only those with a report DOI (14 in
  2026). Reports without an OSF node (e.g. ResearchEquals) need their PDF added
  manually and `OSF node = None` in `REVIEWS`.
- **Daniel Nüst appears as an OSF contributor (project admin) on several report
  nodes without being the codechecker** — trust the PDF's "Codechecker(s)" field.
- The "Ref. certificate" cell inside some report PDFs contains a mis-pasted
  report DOI, *not* the register certificate number — ignore it.
