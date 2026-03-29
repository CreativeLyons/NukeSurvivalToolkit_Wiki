# Agent notes (Nuke Survival Toolkit Wiki)

When working in this repository on documentation, MkDocs, or PDF export:

| Document | Purpose |
|----------|---------|
| [`documentation/DEVELOPMENT.md`](documentation/DEVELOPMENT.md) | **Current** architecture: repo layout, build modes, deployment, PDF entrypoints (`./export_pdf`, `buildPDF/make_wiki_pdf`), merge order, dependencies, validation. |
| [`documentation/archive/pdf-pipeline-history.md`](documentation/archive/pdf-pipeline-history.md) | **Historical** context: WeasyPrint vs browser renderer decisions, debugging conclusions, dated benchmarks, optional `.ai/` handoff pointers. |
| [`documentation/USER_GUIDE.md`](documentation/USER_GUIDE.md) | Step-by-step usage for contributors (preview, offline HTML, `./export_pdf` flags). |

Do not treat the archive as the live spec; verify behavior in `buildPDF/` when in doubt.
