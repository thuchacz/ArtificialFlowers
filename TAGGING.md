# Tagging Guide: Semantic Filtering for the Artificial Flowers Edition

This guide explains the tag-filtering feature added to the edition in July 2026, and walks through how to extend the tagging from the first sample entries to the full manuscript. It is written for editors who are comfortable editing TEI XML but who are not developers.

## What the feature does

Readers can now filter the manuscript's pages by the things mentioned in them — materials, tools, measurements, and techniques — directly inside the viewer, the way the [Ornament : Design : Translation](https://performant-software.github.io/editioncrafter-odt/#/ec/) edition works.

In the viewer, the reader:

1. Clicks the **grid icon** in the top-left corner to open the **Contents** drawer, which lists every page as a thumbnail.
2. Clicks **Filter** and checks one or more tags (for example *Materials → gum tragacanth*). The page list immediately narrows to only the pages whose entries mention those things.
3. Hovers over a thumbnail and clicks its **"insert left"** or **"insert right"** button to open that page in the viewer. (Clicking the thumbnail picture itself does nothing — you must use the two small buttons that appear on hover.)
4. While a tag is selected, every tagged term is highlighted in the transcription and translation panes.

The reader's selections are saved in the page address, so a filtered view can be bookmarked or shared as a link.

Everything the filter knows comes from the TEI file `artificial_flowers.xml`. There is no separate list to maintain: tag the TEI, run one command, and the viewer picks it up.

## What has been done so far

- The viewer software was upgraded to a version that includes the "Tag Explorer" (the filter interface), and the site was configured to use it.
- A starter set of categories was added to the TEI header: **Materials** (silk, gum tragacanth, rainwater, cambric, gamboge, saffron, lye, crimson fabric, paper), **Tools** (spoon, knife, glass pane, cloth, towel, flower form, polishing stone, stove, earthenware pot, paintbrush), **Measurements** (patar, pint), and **Techniques** (starching, boiling, drying, cutting, dyeing, undyeing).
- The first three recipes (pages 0003–0004, i.e. folios `f002`–`f003`) were tagged as a working example, in **both** the French transcription and the English translation.

Everything else — roughly 110 more entries — still needs tagging. The rest of this guide explains how.

## How the tagging works

There are three pieces, all inside `artificial_flowers.xml`.

### 1. The tag list (in the header)

Near the top of the file, inside `<encodingDesc><classDecl>`, each group of tags is a `<taxonomy>` and each tag is a `<category>`:

```xml
<taxonomy xml:id="materials">
    <bibl>Materials</bibl>
    <category xml:id="silk"><catDesc>silk</catDesc></category>
    <category xml:id="gum_tragacanth"><catDesc>gum tragacanth</catDesc></category>
    ...
</taxonomy>
```

- The `<bibl>` line is the group heading shown in the filter panel.
- Each `<category>` needs a unique `xml:id` (lowercase, words joined with underscores, no spaces) and a `<catDesc>` — the label readers will see.
- To add a new tag, copy one of the existing `<category>` lines, change both the `xml:id` and the label, and keep it inside the right taxonomy. You can also add whole new taxonomies (for example "Plants" or "Colors") by copying an entire `<taxonomy>` block.

Use the reader-facing label to normalize spelling: the manuscript's *gomme dragant*, *gomme de sois*, and the translation's *tragacanth gum* are all one tag, `gum_tragacanth`.

### 2. Tagging a whole entry

Each recipe in the manuscript is an `<ab>` block. To make an entry findable, wrap its `<ab>` in a `<div>` that lists every tag that applies to it, each preceded by `#`:

```xml
<div ana="#cambric #gamboge #saffron #lye #undyeing">
<ab>
<lb />Maniere poūr detindre le cambraij, tain
...
</ab>
</div>
```

This `div` is what makes pages show up when a reader filters. Its `ana` list should contain the union of everything tagged inside the entry.

### 3. Tagging individual terms

Inside a tagged entry, wrap each meaningful term in a `<seg>`:

```xml
<lb />aūec de la <seg ana="#gamboge">gomme-gūt</seg>, il faūt ensieper la
```

These `seg` tags are what light up in the reading panes when a reader selects a tag. **Important:** a `<seg>` only counts if it sits inside an entry `<div>` that has an `ana` attribute — a stray `seg` outside a tagged `div` will be ignored.

Tag the **transcription (`tc`) and the translation (`tl`) in parallel** — the same entry appears once in each half of the file, and both should carry the same entry-level tags so filtering behaves the same whichever pane the reader has open.

The three tagged entries at the start of each layer (search the file for `div ana=` to find them) are the model to copy.

## The workflow, step by step

1. **Edit `artificial_flowers.xml`** — add any new categories to the header, then tag entries and terms as above. Work in manageable batches (a few folios at a time).

2. **Check the file is well-formed.** Any XML-aware editor (Oxygen, VS Code with an XML extension) will flag a missing quote or an unclosed tag. This is the most common source of trouble.

3. **Regenerate the viewer data.** In a terminal at the project folder (a GitHub Codespace works fine), run:

   ```
   npm run edition
   ```

   This one command rebuilds everything the viewer reads: the page manifest, the transcription/translation pages, and the tag database. It takes a minute or two. If you misspell a tag reference, it will print a warning like `Tag #gum_tragacant not found in taxonomy element.` — fix the typo and run it again.

4. **Commit and push to GitHub.** The site rebuilds and republishes itself automatically a few minutes after every push to the `main` branch. Then check your new tags at https://thuchacz.github.io/ArtificialFlowers/.

> **Note on previewing before pushing:** the generated files point at the published site's address, so a plain local preview will show the *previously published* text, not your fresh edits. For a true local preview a developer can rebuild with a localhost address — the exact commands are in the "Semantic Tag Filtering" section of `README.md`. For most tagging work, pushing to GitHub and checking the live site is the simplest reliable check.

## Rules and gotchas checklist

- Every `#reference` in an `ana` must exactly match a `<category xml:id>` in the header — same spelling, case-sensitive.
- `xml:id`s: lowercase letters and underscores only; must be unique across the whole file.
- Multiple tags in one `ana` are separated by single spaces: `ana="#silk #knife #cutting"`.
- A `<seg>` may span a line break (`<lb />` inside it is fine), but keep each `seg` within one page — don't cross a `<pb />`.
- Only `<seg>` elements inside a tagged entry `<div>` are indexed.
- Tag both the `tc` and `tl` layers.
- Don't rename or remove the `xml:id` on `<facsimile>` or empty the `<title>` in the header — the build tools require both.
- The software versions in `package.json` are deliberately pinned, and two small bug-fix patches are applied automatically when the project is installed. Don't upgrade the EditionCrafter packages without reading the "Semantic Tag Filtering" section of `README.md` first.

## Questions this guide doesn't answer

The technical details (which packages, what the patches fix, how the database is built) are documented in `README.md` under "Semantic Tag Filtering". For decisions about *what* to tag — which terms deserve tags, how fine-grained the taxonomy should be — the Making & Knowing Project's [Principles of Encoding](https://edition640.makingandknowing.org/#/content/resources) for the 1580 edition is the closest model.
