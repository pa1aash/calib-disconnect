# archives/

Frozen historical record (see `docs/LEGACY.md`). The zip files are not modified.

## What each archive contains

| Archive | SHA-256 | Contents |
|---------|---------|----------|
| `dl4cV1.zip` | `a9d59572bbf2e71280fc1458b1ec0623ac5d37e3efedf35cb203c09540c6e364` | The v1 manuscript bundle (`papers/v1`). |
| `dl4cV2.zip` | `5c054129c9a1d1659ce76a2509f69aa956ef40bdfdc853b33027086952e43858` | The **v3** manuscript bundle (`papers/v3`), despite its name. |
| `icml2026_styles.zip` | `8b29290f5828e176debb57ea9cc00252502973d55ea561a2f18a7f0a326bfc6c` | The stock ICML 2026 style kit (example paper and style files); no project manuscript. |

**No archive contains the v2 manuscript (`papers/v2`).**

## Evidence

Each zip was extracted to a scratch folder and every member was byte-compared (`filecmp.cmp`,
`shallow=False`) with the files of the same name in `papers/v1`, `papers/v2` and `papers/v3`
(2026-11-10, wave 2; the same result was first found with `cmp` in wave 1, `docs/s1/BUNDLE_MAP.md`).

- `dl4cV2.zip` (8 members): `main.tex`, `references.bib` and `main.bbl` are identical to
  `papers/v3` only. The five style files (`icml2026.sty`, `icml2026.bst`, `fancyhdr.sty`,
  `algorithm.sty`, `algorithmic.sty`) are identical in all three manuscript folders, so they do
  not distinguish versions.
- `dl4cV1.zip` (8 members): `main.tex`, `references.bib` and `main.bbl` are identical to
  `papers/v1` only; the five style files are shared as above.
- `icml2026_styles.zip` (9 members): `example_paper.tex/.bib/.pdf`, `icml_numpapers.pdf` and the
  five style files; it contains no `main.tex`.

SHA-256 values were computed with `shasum -a 256 archives/*.zip`.
