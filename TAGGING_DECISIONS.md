<!-- Working spec and precedent log from the automated semantic-tagging run (July 2026). The "Precedents" section records editorial judgment calls made batch by batch; see TAGGING.md for the editor-facing guide. -->

# Agent conventions for semantic tagging of artificial_flowers.xml

You are tagging a batch of folios in `/Users/thc4/Github/ArtificialFlowers/artificial_flowers.xml`,
an EditionCrafter TEI file for an 18th-century Flemish-French manuscript of artificial-flower-making
recipes. The file has TWO text layers covering the same folios:

- `<text xml:id="tc">` — the French transcription (starts ~line 240)
- `<text xml:id="tl">` — the English translation (starts ~line 2770)

Each folio page is marked `<pb facs="#fNNN" />`; each recipe/entry on the page is an `<ab>` block.
For any folio `fNNN`, `grep -n 'pb facs="#fNNN"'` returns (up to) two hits: the FIRST is the tc
layer, the SECOND is the tl layer. Some folios exist in tc only — then tag tc alone.

## What to do for every `<ab>` in your folio range, in BOTH layers

1. Read the entry and identify every meaningful mention of:
   - **materials** — substances, fabrics, dyestuffs, liquids, gums, waxes, wires, papers…
   - **tools** — implements, vessels, forms, brushes, presses, irons…
   - **measurements** — units of quantity, money, volume, weight (patar, pint, ounce, ell…)
   - **techniques** — named processes (boiling, dyeing, starching, cutting, drying, pressing…)
   - **flowers** — flower/plant kinds being made (rose, carnation, tulip…) and distinct plant
     parts made as products (leaf, bud, stem…)
2. Wrap each such term occurrence in `<seg ana="#tag_id">exact original text</seg>`. Tag EVERY
   occurrence of the term inside the entry, not just the first. A `<seg>` may contain `<lb />`
   (continue across a line break) but must NEVER contain a `<pb ... />`.
3. Wrap the whole `<ab>…</ab>` in `<div ana="#tag1 #tag2 …">` … `</div>`, where the ana list is
   the UNION of every tag used in a `<seg>` inside that ab. The `<pb />` stays OUTSIDE the div.
4. The same recipe appears once in tc (French) and once in tl (English). Decide the tag set once
   and keep the two layers' entry-level `ana` lists IDENTICAL (union of both layers if one layer
   mentions something the other omits). Term-level segs go on the corresponding French and English
   words respectively.
5. An `<ab>` that merely continues the previous page's recipe still gets its own `<div>`, carrying
   the tags for what is mentioned in THAT ab (plus the recipe's principal tags when obvious).
6. If an `<ab>` genuinely mentions nothing taggable (blank page notes, pure cross-references),
   leave it unwrapped — do not invent tags.

## Taxonomy rules (header `<classDecl>`, ~lines 16–60)

- ALWAYS re-read the current `<classDecl>` block FIRST (it grows as other batches are tagged) and
  reuse existing category ids wherever the concept matches. Spelling variants and synonyms map to
  ONE id: *gomme dragant* / *gomme de sois* / *tragacanth gum* are all `#gum_tragacanth`.
- Add a new `<category xml:id="new_id"><catDesc>reader-facing label</catDesc></category>` inside
  the right `<taxonomy>` only when no existing category fits. Ids: lowercase letters and
  underscores only, unique across the whole file. Labels: concise English, lowercase; put a
  memorable original-language term in parentheses when helpful, e.g. `crimson fabric (incarlacque)`.
- Keep to the five existing taxonomies (materials, tools, measurements, techniques, flowers). If
  something fits none of them, skip it and mention it in your final report.
- Prefer a moderately coarse grain: "brass wire" and "iron wire" deserve separate tags only if the
  manuscript really distinguishes them; colors of silk are still `#silk`. Distinct dyestuffs DO
  get their own tags. Generic plain water is NOT tagged; `#rainwater` and other specific waters are.

## Hard constraints

- NEVER alter, add, or delete any character of the transcription/translation text itself —
  including its idiosyncratic spelling, `ū` characters, `[illeg]`, `+`, `✠`, `~` marks. You only
  ADD `<div ana>`, `<seg ana>`, and taxonomy `<category>` elements.
- Do not touch folios outside your assigned range, and do not re-tag entries that already have a
  `<div ana=`.
- Model to copy: the already-tagged entries at f002/f003 in both layers (grep `div ana=`).
- Every `#ref` you write must exactly match a `category xml:id` (case-sensitive).
- After finishing, run `xmllint --noout /Users/thc4/Github/ArtificialFlowers/artificial_flowers.xml`
  and fix any well-formedness error you introduced.

## Precedents from earlier batches (follow these; append-only)

From f004–f016:
- Generic plain/hot/cold/clear water: never tagged. Specific waters (`#rainwater`) are.
- A mention that merely refers BACK to an already-used object ("cette colle", "le linge" meaning
  the previously starched cloth) is not re-tagged; tag substantive uses only. `#cloth` (tool) is
  reserved for straining/binding cloths per the f002/f003 model.
- Colors/shades of silk are still `#silk`; named dyestuffs and pigments each get their own
  material tag (e.g. `#carmine`, `#vermilion`, `#red_lead`, `#bruges_blue`, `#lacmus`).
- Places (attic, cellar) are not taggable — skip, flag in report if notable.
- When one layer splits an entry into two <ab>s and the other merges it into one, keep the
  folio-level union of ana sets identical across layers (see f007/f016 handling).
- When a sentence fragment at the top of a folio completes a recipe from an earlier page, tag it
  with the tags its own words support (e.g. f010 "d'empoise" → `#starch_blue`).
- If the two layers disagree on what a word means (f012 "ponsaū" = poppy-red color vs tl "pansy"),
  leave the doubtful term untagged in both layers and flag it in your report.

From f017–f029:
- Color NAMES are not flower tags: "coūloeūrs jonqūille" / "coūleūr de rosse" describe shades,
  not flowers being made — do not tag `#jonquil` etc. for them.
- Time expressions (quarter of an hour, month of May) and state adjectives (quite dry) fit no
  taxonomy: skip silently.
- When tc's reading is confident and tl is evidently a mistranslation of the same word (f028
  alimon → "elements"), tag BOTH layers with the tc meaning to keep parity, and flag it. (The
  f012 leave-untagged precedent applies only when the meaning is doubtful in both layers.)
- Bare "gomme"/"gum" in dye/tracing contexts follows f003: `#gum_tragacanth`.
- An <ab> with nothing taggable (illegible marginal fragments) stays unwrapped (rule 6).
- Long multi-page recipes: each continuation ab carries the recipe's principal technique tag
  (e.g. `#dyeing`) plus its own page's mentions.

From f030–f042:
- A PREPARED colorant and its RAW ingredient are distinct materials (`#bottle_green` = the made
  green liquid vs `#verdigris` = the raw ingredient). Reuse the prepared-product tag when the
  text refers to the made substance.
- Verbs for coloring a substrate (verdir, roūgir, jonnir paper/vellum) map to `#dyeing` per the
  coarse-grain rule; do not mint per-color techniques.
- Different words for the same implement share one tag (canif and coūtaū are both `#knife`).
- Plant parts made as products (leaf, stem) belong in the flowers taxonomy.
- Skip as fitting no taxonomy: stirring/mixing/beating/cooling/sun-exposure actions, month
  names, color-shade adjectives, and similes ("like laundry", "thick like pap").
- Uncertainly identified substances get a generic label with the original term in parentheses
  ("white pigment (petit blan)") rather than a speculative identification.

## Final report (your return message)

Return a terse report: folios tagged; number of entries wrapped per layer; new categories added
(id → label, taxonomy); any terms you couldn't classify or editorial ambiguities worth flagging.
Do NOT paste file content.
