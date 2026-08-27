#!/usr/bin/env python3
"""Generate one reports/<id>/codecheck.yml per reproducibility review.

Reusable across years: the `data` dict below is the single source of truth,
assembled from `fetch_report_metadata.py` output + the report PDFs (checker,
ORCID, check date, repository and outcome come from each report's title page /
"Reproduction metadata" table - the API does not carry them). Certificates map
by ascending submission ID onto the block reserved in the register issue.
Re-run any time to regenerate; existing PDFs in the folders are left untouched.
Only depends on the Python standard library. Keep the `data` block for the year
as a record of what was written.
"""
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "reports")

data = {
 7:  dict(cert="2026-004", art=3, folder="007",
      title="Inclusive Multimodal Routing: How Behavioral Constraints Shape Accessibility",
      authors=[("Ioanna Gogousou","0009-0001-3200-7202"),("Manuela Canestrini","0009-0005-1501-8398"),("Negar Alinaghi",None),("Ioannis Giannopoulos",None)],
      checker=[("Egor Kotov","0000-0001-6690-5345")], report="https://doi.org/10.17605/OSF.IO/R2674",
      repo="https://github.com/e-kotov/agile-2026review-paper-007", date="2026-03-15",
      summary="Reproduction of the multimodal routing analysis for the city of Vienna, investigating how routing outcomes change under behavioral constraints. The full pipeline (baseline routing, inclusive baseline routing, 12 parameter-variation scenarios, data grouping and visualization) was completed in a single, fully automated run on HPC resources. The reproduction was fully successful."),
 8:  dict(cert="2026-005", art=2, folder="008",
      title="A Method for Spatializing Disturbance by Detecting Human-Wildlife Encounters from GNSS Trajectories",
      authors=[("John Dawson",None),("Veronika Peralta",None),("Ana-Maria Olteanu-Raimond",None),("Thomas Devogele",None),("Mathieu Garel",None)],
      checker=[("Franz Welscher","0000-0003-2432-1880")], report="https://doi.org/10.17605/OSF.IO/DZT8C",
      repo="https://github.com/IntForOut/Human_Wildlife_Encounter_Detection", date="2026-03-24",
      summary="The reproduction was mostly successful by following the repository README and adapting the workflow to the available environment (PostgreSQL 15 instead of 16). Several issues required manual fixes: an invalid geometry blocked the database import, a timestamp/date mismatch broke a table-creation function, the DEM file was not included and had to be requested from the authors, and the Figure 8 script contained an SQL error. After corrections, all figures and tables were reproduced, with minor discrepancies remaining in Tables 2, 3, 5 and 8."),
 10: dict(cert="2026-006", art=4, folder="010",
      title="Towards Fine-grained Relevance Scoring of Social Media Posts in Disaster Response: A Decay-based Regression Approach",
      authors=[("David Hanny",None),("Andreas Kramer",None),("Ehsaneddin Jalilian",None),("Sebastian Schmidt",None),("Bernd Resch",None)],
      checker=[("Sophie Teichmann","0000-0002-4314-8107")], report="https://doi.org/10.17605/OSF.IO/ZPURT",
      repo="https://github.com/reproducible-agile/GSAI_PUBLIC_Multimodal_Relevance_Regression", date="2026-03-19",
      summary="Full reproduction. Using the materials provided by the authors, the reported results were successfully reproduced."),
 12: dict(cert="2026-007", art=9, folder="012",
      title="Analysis of the spatial and temporal pattern of COVID-19 incidence rate across Germany",
      authors=[("Sven Lautenbach",None),("Marcel Maurer",None),("Alexander Zipf",None)],
      checker=[("Eftychia Koukouraki","0000-0003-0928-1139")], report="https://doi.org/10.17605/OSF.IO/DZURB",
      repo="https://github.com/slautenb/covid19germany", date="2026-06-09",
      summary="Partially successful reproduction. The authors shared scripts, intermediate results and documented instructions via an anonymous GitHub link. Figures 1-7 and Tables 2 and 3 were verified; the reproduced results were mostly in accordance with the reported results."),
 13: dict(cert="2026-008", art=13, folder="013",
      title="Generalizability of Foundation Models: A Case Study on Cocoa Mapping Across Countries Using Sparse Labels",
      authors=[("Ruslan Mammadov",None),("Paul Walther",None),("Julius Fricke",None),("Martin Werner",None)],
      checker=[("Joseph Shingleton","0000-0002-1628-3231")], report="https://doi.org/10.17605/OSF.IO/YH8F6",
      repo="https://github.com/osapiens-Terra-GmbH/2026-AGILE-CocoaMapping", date="2026-03-31",
      summary="Partial reproduction of the foundation-model cocoa-mapping study. The provided code and data allowed the workflow to be run, though some files in the repository were differentiated only by path rather than filename, complicating the reproduction."),
 15: dict(cert="2026-009", art=5, folder="015",
      title="Enhancing the Potential of a Tangible-Digital Planning Interface through User Evaluation",
      authors=[("Vincent Holtorf",None),("Maria Moleiro Dale",None),("Jörg Rainer Noennig",None)],
      checker=[("Jeonghwan Choi","0009-0002-5027-1151")], report="https://doi.org/10.17605/OSF.IO/KCPZE",
      repo="https://github.com/reproducible-agile/COUP-TangibleTable", date="2026-03-19",
      summary="Full reproduction. The submission is based on a qualitative framework and spreadsheet-based analysis rather than custom programming. The reviewer reviewed the materials in the repository (data and analysis materials archived at https://doi.org/10.5281/zenodo.18195076) and reproduced the reported figures."),
 16: dict(cert="2026-010", art=11, folder="016",
      title="Exploring urban polygonal representation learning for complex footprint groups",
      authors=[("Luisa Lo Presti",None),("Peter Mooney",None)],
      checker=[("Carlos Granell","0000-0003-1004-9695")], report="https://doi.org/10.17605/OSF.IO/DA3Z4",
      repo="https://github.com/reproducible-agile/BaselineBuildingRL-AGILE2026", date="2026-04-06",
      summary="Full reproduction. The reviewer was pointed to the authors' GitHub repository, cloned it into Google Colab, configured the environment and executed the code without deviations from the submitted manuscript. The study comes with a full code repository and the results were reproduced."),
 17: dict(cert="2026-011", art=18, folder="017",
      title="Towards National-Scale Ecological Applications: Harmonised Framework for LiDAR Point Cloud Processing for Vegetation Metrics Calculation",
      authors=[("Eveli Sisas",None),("Holger Virro","0000-0001-6110-5453"),("Wai Tik Chan",None),("Alexander Kmoch","0000-0003-4386-4450"),("Aveliina Helm",None),("Evelyn Uuemaa","0000-0002-0782-6740")],
      checker=[("Frank O. Ostermann","0000-0002-9317-8291")], report="https://doi.org/10.17605/OSF.IO/75PWN",
      repo="https://doi.org/10.5281/zenodo.17867739", date="2026-03-31",
      summary="Full reproduction of a sample data set. A complete reproduction was infeasible as part of the review due to the computational environment required for the national-scale workflow, but the successful reproduction of a sample data set demonstrates the overall reproducibility of the study."),
 21: dict(cert="2026-012", art=16, folder="021",
      title="Spatio-Temporal Knowledge Graph from Unstructured Texts: A Multi-Scale Approach for Food Security Monitoring",
      authors=[("Charles Abdoulaye Ngom",None),("Landy Rajaonarivo",None),("Maguelonne Teisseire",None),("Sarah Valentin",None)],
      checker=[("Sophie Teichmann","0000-0002-4314-8107")], report="https://doi.org/10.17605/OSF.IO/BV4MK",
      repo="https://github.com/reproducible-agile/STKGFS", date="2026-04-10",
      summary="Partial reproduction. The authors provided a well-documented GitHub repository with detailed instructions; Table 2 was recreated with the provided script. A full reproduction requires substantial computational resources (in particular the fine-tuning in Step 2)."),
 22: dict(cert="2026-013", art=8, folder="022",
      title="Maximizing Data Coverage: Fusing Street View and Oblique Imagery to Quantify Vertical Greenery Potential in Urban Areas",
      authors=[("Aruscha Kramm",None),("André Ludwig",None),("Bogdan Franczyk",None)],
      checker=[("Jeonghwan Choi","0009-0002-5027-1151")], report="https://doi.org/10.17605/OSF.IO/HETV8",
      repo="https://github.com/reproducible-agile/Quantify-VGS", date="2026-03-13",
      summary="Partially reproducible. The LoD2 preprocessing step (distribution of façade orientations) was reproduced successfully, confirming successful preprocessing; other manuscript outputs could be reproduced only partially."),
 26: dict(cert="2026-014", art=17, folder="026",
      title="Food Insecurity Projections for Anticipatory Action: Comparative Spatiotemporal Analysis of FEWS NET and the IPC in Somalia",
      authors=[("Ferdinand Seyffer",None),("Anne Schauss",None),("Suella Tirai",None),("Marcel Maurer",None),("Sven Lautenbach",None),("Alexander Zipf",None)],
      checker=[("Daniel Nüst","0000-0002-0024-5046")], report="https://doi.org/10.53962/pdw8-n5v0",
      repo="https://github.com/reproducible-agile/agile2026_food_insecurity_anticipatory_action", date="2026-06-11",
      summary="The article presents a comparative spatio-temporal analysis of food insecurity projections in Somalia. A workflow is provided as a collection of scripts with a Docker compose environment. The workflow as described could be executed and all figures and maps from the article were recreated with the code and data provided. The reproduction is fully successful."),
 29: dict(cert="2026-015", art=10, folder="029",
      title="Assessing the Geographic Diversity of AI's Platial Representations in Image Generation",
      authors=[("Zilong Liu",None),("Krzysztof Janowicz",None),("Mina Karimi",None)],
      checker=[("Frank O. Ostermann","0000-0002-9317-8291")], report="https://doi.org/10.17605/OSF.IO/VCGY2",
      repo="https://github.com/zilongliu-geo/image-gen-geodiversity", date="2026-04-10",
      summary="Successful but partial reproduction. The third part of the analysis reproduced smoothly, with all figures identical to the ones produced for the paper."),
 31: dict(cert="2026-016", art=6, folder="031",
      title="Geo-Alignment of Vague Cognitive Regions: Representing Uneven Cognitive Geographies of Large Language Models",
      authors=[("Mina Karimi",None),("Krzysztof Janowicz",None),("Zilong Liu",None),("Songlin Wang",None),("Annika Süß",None)],
      checker=[("Franz Welscher","0000-0003-2432-1880")], report="https://doi.org/10.17605/OSF.IO/WH6GD",
      repo="https://github.com/MinaKarimi/Geo-alignment-of-AI-in-VCRs", date="2026-04-27",
      summary="The study is partially reproducible due to external resource constraints. The provided code, data and documentation are clear and complete, but a full reproduction was not possible because data generation relied on paid APIs (OpenAI, DeepSeek, Google Gemini) that were not accessible for re-running, and indices/figures required ArcGIS/arcpy, which was unavailable on the reviewer's system."),
 33: dict(cert="2026-017", art=12, folder="033",
      title="OpenStreetMap Suitability Analysis for Wheelchair Routing",
      authors=[("Ivan Majic",None),("Thomas Gegenleithner",None),("Johannes Scholz",None)],
      checker=[("Egor Kotov","0000-0001-6690-5345")], report="https://doi.org/10.17605/OSF.IO/8C3VF",
      repo="https://doi.org/10.6084/m9.figshare.31333180", date="2026-04-25",
      summary="Reproduction using the authors' updated data package (v2), covering the full pipeline including database setup and all analysis notebooks (01 to 04). While the v2 package significantly improved structure and documentation, several surgical fixes were still required to address environment-specific dependency conflicts, undocumented tool behaviors, and logic bugs in the provided scripts. All notebooks were ultimately executed successfully."),
}

# Author ORCIDs extracted from the Copernicus article PDFs (authoritative), keyed
# by submission id and the author name as used above. Applied over the (sparse)
# Crossref ORCIDs. Authors absent here have no ORCID in the published article.
AUTHOR_ORCID = {
 7:  {"Ioanna Gogousou":"0009-0001-3200-7202","Manuela Canestrini":"0009-0005-1501-8398","Negar Alinaghi":"0000-0001-6594-4481","Ioannis Giannopoulos":"0000-0002-2556-5230"},
 8:  {"John Dawson":"0009-0008-9333-7169","Veronika Peralta":"0000-0002-9236-9088","Ana-Maria Olteanu-Raimond":"0000-0002-1101-1333","Thomas Devogele":"0000-0001-9187-8385","Mathieu Garel":"0000-0002-5978-7122"},
 10: {"David Hanny":"0009-0004-8017-0786","Andreas Kramer":"0009-0006-4763-749X","Ehsaneddin Jalilian":"0000-0001-5925-5735","Sebastian Schmidt":"0000-0003-1912-9771","Bernd Resch":"0000-0002-2233-6926"},
 12: {"Sven Lautenbach":"0000-0003-1825-9996","Marcel Maurer":"0000-0002-0204-5101","Alexander Zipf":"0000-0003-4916-9838"},
 13: {"Ruslan Mammadov":"0009-0006-3516-9852","Paul Walther":"0000-0002-5101-5793","Julius Fricke":"0009-0005-7709-8178","Martin Werner":"0000-0002-6951-8022"},
 15: {"Vincent Holtorf":"0009-0008-4486-531X","Maria Moleiro Dale":"0000-0001-7655-1309","Jörg Rainer Noennig":"0000-0002-1681-7635"},
 16: {"Luisa Lo Presti":"0009-0006-1096-9108","Peter Mooney":"0000-0002-2389-3783"},
 17: {"Eveli Sisas":"0009-0002-5032-249X","Holger Virro":"0000-0001-6110-5453","Wai Tik Chan":"0009-0005-3779-139X","Alexander Kmoch":"0000-0003-4386-4450","Aveliina Helm":"0000-0003-2338-4564","Evelyn Uuemaa":"0000-0002-0782-6740"},
 21: {"Charles Abdoulaye Ngom":"0009-0007-4540-4112","Landy Rajaonarivo":"0000-0003-1831-270X","Maguelonne Teisseire":"0000-0001-9313-6414","Sarah Valentin":"0000-0002-9028-681X"},
 22: {"Aruscha Kramm":"0009-0002-7801-9388"},
 26: {"Ferdinand Seyffer":"0009-0009-8274-1462","Anne Schauss":"0009-0001-6773-0468","Marcel Maurer":"0000-0002-0204-5101","Sven Lautenbach":"0000-0003-1825-9996","Alexander Zipf":"0000-0003-4916-9838"},
 29: {"Zilong Liu":"0000-0002-7699-3366","Krzysztof Janowicz":"0009-0003-1968-887X","Mina Karimi":"0000-0003-2521-8164"},
 31: {"Mina Karimi":"0000-0003-2521-8164","Krzysztof Janowicz":"0009-0003-1968-887X","Zilong Liu":"0000-0002-7699-3366","Songlin Wang":"0009-0004-6506-2859"},
 33: {"Ivan Majic":"0000-0002-0834-3791","Johannes Scholz":"0000-0002-3212-8864"},
}
for _sub,_d in data.items():
    _ov=AUTHOR_ORCID.get(_sub,{})
    _d["authors"]=[(n,_ov.get(n,o)) for n,o in _d["authors"]]

# Output-file manifests taken from each report's "Summary of output files
# generated" table, where the report lists discrete output files. Reports that
# describe the reproduction as prose / recreated tables instead keep the NA
# placeholder (see the else branch below).
MANIFEST = {
 10: [("data/figures/decay_curves.pdf","Reproduction of Figure 2"),
      ("data/output/decay_classif_eval.csv","Reproduction of Table 4 (classification evaluation)"),
      ("data/output/regression_eval.csv","Reproduction of Table 4 (regression evaluation)"),
      ("data/figures/prediction_histogram.pdf","Reproduction of Figure 4")],
 15: [("~result/Figure_1.png","Regenerated Figure 1 (system strengths identified by the participant groups)"),
      ("~result/Figure_2.png","Regenerated Figure 2 (system strengths identified by the participant groups)"),
      ("~result/regenerate_figures.xlsx","Spreadsheet regenerating the figures; Keywords_Pro&Con.pdf holds the aggregated thematic category counts")],
 17: [("repro_rev_2026_17_notebook.html","Notebook reproducing the sample-data LiDAR vegetation-metrics workflow")],
 22: [("~result/orientation_orig.png","Distribution of facade orientations (LoD2 preprocessing)"),
      ("~result/wwr_orig.png","Window-to-wall ratio values"),
      ("~result/swa_orig.png","Surface area values"),
      ("~result/index_weighted.png","Weighted vertical greenery potential index")],
 29: [("repro_rev_2026_29_notebook.html","Notebook reproducing the third part of the analysis and its main figures")],
}

def q(s): return '"' + s.replace('"','\\"') + '"'

def main():
  for sub,d in data.items():
    lines=[]
    lines.append("---")
    lines.append("version: https://codecheck.org.uk/spec/config/1.0/")
    lines.append("")
    lines.append("manifest:")
    if sub in MANIFEST:
        for fname,comment in MANIFEST[sub]:
            lines.append(f"  - file: {fname}")
            lines.append(f"    comment: {q(comment)}")
    else:
        lines.append("  - file: NA")
        lines.append('    comment: "The AGILE 2026 Reproducibility Review report does not list discrete output files, see https://github.com/codecheckers/register/issues/186 for more information"')
    lines.append("")
    lines.append("paper:")
    lines.append(f"  title: {q(d['title'])}")
    lines.append("  authors:")
    for name,orcid in d["authors"]:
        lines.append(f"    - name: {name}")
        if orcid: lines.append(f"      ORCID: {orcid}")
    lines.append(f"  reference: https://doi.org/10.5194/agile-giss-7-{d['art']}-2026")
    lines.append("")
    lines.append("codechecker:")
    for name,orcid in d["checker"]:
        lines.append(f"  - name: {name}")
        if orcid: lines.append(f"    ORCID: {orcid}")
    lines.append("")
    lines.append(f"report: {d['report']}")
    lines.append("summary: |")
    for para in d["summary"].split("\n"):
        lines.append("  " + para)
    lines.append(f"repository: {d['repo']}")
    lines.append(f'check_time: "{d["date"]} 12:00:00"')
    lines.append(f"certificate: {d['cert']}")
    lines.append("")
    folder=os.path.join(R,d["folder"])
    os.makedirs(folder,exist_ok=True)
    path=os.path.join(folder,"codecheck.yml")
    with open(path,"w") as f: f.write("\n".join(lines))
    print("wrote",path)
  print("TOTAL",len(data))

if __name__ == "__main__":
    main()
