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

- **f139 · "wasch" / "[egg] wash"** — the Dutch means *wax* (for polishing dyed wood); tagged
  `#wax` in both layers. **Q:** correct the translation.
- **f139 · "linten" / "[?bits of the brazilwood?]"** — the Dutch means *ribbons* (as dyed
  goods); tagged `#ribbon`. **Q:** correct the translation.
- **f140 · "nemt 't lack" / "take the cloth and throw it on the floor"** — the Dutch describes
  classic lake-pigment making (pouring off the sediment to dry); the translation misses it
  entirely. Tagged `#lake_pigment`. **Q:** retranslate this passage.

- **f148–f170 · systematic small mistranslations in the Dutch section** (each tagged with the
  Dutch meaning per the f028 precedent; the English seg sits on the translator's word):
  f148 *groot* (coin) → "large"; f156 *gambe* (gamboge) → "gum"; f160 *wecken* (soak) →
  "Preserve" and *geschūmt* (skimmed) → "foamy"; f164/f166 *honse/onsse* (ounce) → "our";
  f168 *sien* (seethe) → "seen", *pot asschen* (potash) → "pot of…ashes", *pont* (pound) →
  "pints" (twice); f170 *hert* (hearth) → "heart" and *aerden pot* (earthenware) → "metal
  pot"; f155 *lescivve* (lye) → "Laundry soap/wax(??)"; f164 *wasschen* (wax) → "washed".
  **Q:** systematic retranslation review of the Dutch folios.

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
- **"boūck groen"** (f130s) — green pigment, unidentified; labeled generically as `bouck_green`.
  **Q:** firm identification?
- **"susijn" / "sisein"** (f142, f144) — an unrecorded measure of alum; minted as an
  "unidentified measure" category. **Q:** what unit is this?
- **Doubtful in both layers, left untagged:** f134 "ortiens" (tl "[nettles?]"); f136 "van Co"
  (truncated — cochineal?); f140 "contoor met vier" (possibly *comfoor*, a chafing dish).
  **Q:** readings?
- **f163 "leeder"** (ladder vs leather — tl chose "leather", but a drying rack is more
  plausible); **f168 "troocken"** (possibly *trekken*, steep); **f170 "om roosen te verwen"**
  (dyeing roses, or rose-color?); **f155 "een caen hoūt"** (fragmentary — *kanne*?). All left
  untagged. **Q:** readings?
- **`sap_green` vs `bouck_green`** — two green-pigment categories minted from different
  original terms (*sap groen*, *boūck groen*); identity unproven. **Q:** same substance?
  Merging is a one-line taxonomy change.
- **f148 "people who make flowers"** — generic *fleūrs*, no specific flower; there is no
  generic-flower category, so it's untagged. **Q:** is a generic `flower` category wanted for
  such mentions?

- **f045+ · "bois ferneboūcqūe" / "bois de bresil"** — the translator renders *ferneboucque* as
  "brazil wood" and *bois de bresil* as "logwood", the reverse of what the French names suggest.
  The run followed the translator (`#brazilwood` / `#logwood` respectively). **Update from
  f069:** the translation there *swaps* the correspondence (ferneboūcqūe → "logwood", bersil →
  "Brazilwood"); the run kept tagging by the French term, so the tags are consistent with the
  source even where the translation is not. **Q:** are the identifications right, or should the
  two tags be swapped/merged? The f069 translation likely needs correcting either way.
- **f057 · extra passage in tl only** — the translation contains a whole passage (yellow-dyed
  cloth finished with verjuice, stiffened with fish or hide glue) with no counterpart in the
  French transcription. Union rule applied, so the tc entry carries `#fish_glue`/`#drying`
  without French segs. **Q:** is the passage translated from a page missing in tc, or an
  interpolation? Affects whether the union tags should stay on the tc side.

- **f063 · "l'ensiepper" / "tie it up"** — the French plausibly means "to soap" (cf. *siepez* =
  soap elsewhere), the translation says "tie it up"; doubtful in both layers, left untagged.
  **Q:** which reading is right?
- **f063 · "lecmoūs" / "moss/lichen?"** — tc matches the established *lacmus* term, so both
  layers tagged `#lacmus`; the translator's "moss/lichen?" guess flagged. **Q:** confirm lacmus.
- **f069 · "menie"/"roomenie" / "sweet wine / minium [?]"** — tagged `#red_lead` (menie =
  minium); the tl offers "sweet wine" as an alternative. **Q:** confirm minium.

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

## Non-recipe content (informational)

- **f112 · "MAR"** — both layers contain only the letters MAR, evidently pattern lettering for
  "MARIA"; left untagged. **f122/f123 (tc only)** — abbreviated Latin liturgical text: Psalm 1
  (*Beatus vir*) and Psalm 2 (*Quare fremuerunt gentes*), likely calligraphy models. Untaggable
  under the five taxonomies, so these pages simply don't appear in the Tag Explorer filters.
  **Q:** is that the desired treatment for non-recipe pages, or should a content-type
  taxonomy (recipe / pattern / calligraphy model / glossary) be added so they're findable?
- **f130 · obituary, and the language switch** — f130 is a French obituary of Mother Adriene
  Terese de Maldeghem (Tournai, 1680) — a provenance clue worth noting in the edition's
  front matter. From f128 onward the "transcription" layer is Flemish/Dutch rather than
  French; f128 ("s: Augustinus") is another non-recipe fragment. Both left untagged.
  **Q:** should the language shift be recorded formally (e.g. xml:lang on the affected pages)?

## Standing policy questions

- **Union rule for divergent layers:** when tc and tl genuinely disagree, both currently get the
  tc-derived tag to keep filtering symmetrical, with the divergence flagged here. Alternative:
  tag each layer only for what it says. **Q:** which policy do the editors prefer?
- **Techniques granularity:** stirring, beating, cooling, sun-exposure and similar incidental
  actions are deliberately untagged; named processes (boiling, dyeing, starching, pressing…)
  are tagged. **Q:** is the current line drawn in the right place?
