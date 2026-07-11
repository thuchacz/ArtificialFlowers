# Editorial Questions from the Semantic Tagging Run

Open questions surfaced while tagging `artificial_flowers.xml` (July 2026), for review by the
edition's editors. Each entry records what the automated run did and what needs an editorial
decision. Answers can be noted inline; each ruling will also be added as a precedent in
`TAGGING_DECISIONS.md` so future tagging passes apply it automatically.

Format: **folio · term** — the issue, what was done, and the question.

## Probable translation errors (tc reading confident, tl divergent)

- **f024 · "un peūt dū vinaigre" / "a pint of white wine vinegar"** — tc says *a little* vinegar;
  tl renders it as *a pint*. Both entries currently carry `#pint` (union rule), which overstates
  the tc. **Q:** correct the translation? If so, `#pint` should be removed from this entry.
- **f028 · "alimon" / "elements"** — tc "gardez poūr les alimon" (kept for the anemones) is
  rendered "kept from the elements". Both words tagged `#anemone` with the tc meaning.
  **Q:** confirm and correct the translation.
- **f034 · "foeūilles dū jardin" / "flowers from the garden"** — tc has *leaves* from the garden
  (used to imprint vellum); tl says *flowers*. Both tagged `#garden_leaf` with the tc meaning.
  **Q:** confirm and correct the translation.

## Uncertain identifications

- **f012 · "ponsaū"** (tl "pansy") — the French syntax reads as *ponceau* (poppy-red color) being
  made for the anemones/ranunculus, not a pansy being made. Left untagged in both layers.
  **Q:** is this ponceau (color) or pansy (flower)? Tag accordingly.
- **f017–f018 · bare "gomme" / "clear gum"** in the violet recipe — tagged `#gum_tragacanth`
  following how f003 treats unqualified *gomme* in dye contexts, but gum arabic is plausible.
  **Q:** confirm which gum, here and as a default reading elsewhere.
- **"petit blan"** (f030s) — likely white lead/ceruse but not certain; labeled generically as
  "white pigment (petit blan)". **Q:** firm identification for the catDesc label?
- **"areniez"** — flower name that could not be identified; given its own category with the
  original spelling as label. **Q:** what flower is this?

- **f045+ · "bois ferneboūcqūe" / "bois de bresil"** — the translator renders *ferneboucque* as
  "brazil wood" and *bois de bresil* as "logwood", the reverse of what the French names suggest.
  The run followed the translator (`#brazilwood` / `#logwood` respectively). **Q:** are the
  identifications right, or should the two tags be swapped/merged?
- **f057 · extra passage in tl only** — the translation contains a whole passage (yellow-dyed
  cloth finished with verjuice, stiffened with fish or hide glue) with no counterpart in the
  French transcription. Union rule applied, so the tc entry carries `#fish_glue`/`#drying`
  without French segs. **Q:** is the passage translated from a page missing in tc, or an
  interpolation? Affects whether the union tags should stay on the tc side.

## Terms that fit no current taxonomy (left untagged)

- **"crin"** (horsehair cord, f007) — later tagged as material `#horsehair` from f021 onward;
  the f007 occurrence may deserve retro-tagging. **Q:** confirm.
- **"grez"** (sandstone, f012; again f046 as "caraūx de marbe, oū de grez") — alternative
  grinding/working surface, recurring. Worth a tool tag (or widening `marble_slab` to
  "stone slab")?
- **"tails"** (unclear cloth measure, f010) and **"caraū"** (square/cake of lacmus, f011) —
  possible measurement categories. **Q:** add them?
- **"la passe"** (the vellum pressing stack, f033–f034) — fits neither tool nor technique as
  currently defined. **Q:** how should this be modeled?
- **"gerniez" / attic** (f012, also drying "in the attic" elsewhere) — places are currently not
  tagged at all. **Q:** is a Places taxonomy wanted?

## Standing policy questions

- **Union rule for divergent layers:** when tc and tl genuinely disagree, both currently get the
  tc-derived tag to keep filtering symmetrical, with the divergence flagged here. Alternative:
  tag each layer only for what it says. **Q:** which policy do the editors prefer?
- **Techniques granularity:** stirring, beating, cooling, sun-exposure and similar incidental
  actions are deliberately untagged; named processes (boiling, dyeing, starching, pressing…)
  are tagged. **Q:** is the current line drawn in the right place?
