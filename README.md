# EditionCrafter Project React Template
[![DOI](https://zenodo.org/badge/883392542.svg)](https://doi.org/10.5281/zenodo.16755979)

This repository provides a starting point for creating an [Astro](https://astro.build/) website using EditionCrafter. It comes with a number of pre-configured examples and step-by-step instructions for configuring your own edition. If you are familiar with web software development, follow the installation instructions to set up your development environment. If you want to get started without setting up a local development environment, this repo is configured to work with GitHub CodeSpaces. The code space comes with the latest EditionCrafter Command Line Interface (CLI) and other dependencies pre-installed. Simply fork this repo and then click on the CodeSpaces button.


## Installation

This is a Javascript based project and you will need Node.js v18 or higher to run it locally. First, clone this repository and then run:

```npm install```

Then, install the EditionCrafter CLI:

```npm install -g @cu-mkp/editioncrafter-cli```

Next, follow the initial setup instructions below.

## Initial Setup

To setup setup your project:

1) Edit the `astro.config` file, replacing BASE_DIR with your project base directory. For local installation, this is "."

2) Edit the `data/config.json` file. Fill in the DOCUMENT_NAME, BASE_DIR, and DOCUMENT_ID. You may also need to adjust the `transcriptionTypes` depending on your document. For more information, please see the ["Getting Started"](https://editioncrafter.org/getting-started/) section of the EditionCrafter website.


## Exploring the Example Documents

This project comes with a number of pre-built example documents for you to try out. Simply replace `data/config.json` with one of these alternative config files:

* fr640-config.json : Demonstrates the use of the EditionCrafter component using the folio 3r from [Secrets of Craft and Nature](https://edition640.makingandknowing.org/#/folios/3r)
* fr640-entries.json : Demonstrates the use of the EntryList component in tandem with the EditionCrafter component.
* cary-config.json : This demonstrates the use of zones in the surface images.

## Semantic Tag Filtering (Tag Explorer)

This edition uses EditionCrafter's Tag Explorer to let readers filter pages by semantically tagged terms (materials, tools, measurements, techniques), in the manner of [editioncrafter-odt](https://performant-software.github.io/editioncrafter-odt/#/ec/). It is enabled by `"tagExplorer": "true"` and `"dbUrl"` in `data/config.json`, which cause `src/pages/index.astro` to render the `TagExplore` component instead of the plain `EditionCrafter` viewer.

The tagging conventions in `artificial_flowers.xml` are:

* Taxonomies are declared in `teiHeader/encodingDesc/classDecl`: each `<taxonomy xml:id="...">` needs a `<bibl>` display name, and each leaf `<category xml:id="...">` with a `<catDesc>` becomes a filterable tag.
* Entries (recipe blocks) are wrapped in `<div ana="#tag1 #tag2 ...">` around the `<ab>`; individual terms inside are wrapped in `<seg ana="#tag">term</seg>`. Only `<seg>` elements inside a tagged `<div>` are indexed, and both the `tc` and `tl` layers should be tagged in parallel.
* The `<facsimile>` element must have an `xml:id`, and the header must have a non-empty `<title>` (the CLI requires both).

After editing the TEI, regenerate the viewer data (IIIF manifest, HTML partials, and the tag database) with:

```npm run edition```

Note the versions of `@cu-mkp/editioncrafter` (1.3.1-beta.11) and `@cu-mkp/editioncrafter-cli` (1.3.0-beta.8) are pinned exactly in `package.json`: the Tag Explorer only exists in the 1.3.1-beta line of the viewer, and semver considers the stable 1.3.1 release (which predates it) "newer" than the betas. Two `patch-package` patches under `patches/` are applied automatically by the `postinstall` script:

* `@cu-mkp/editioncrafter-cli`: fixes an out-of-memory bug in the CLI's `database` command (it cloned the whole text layer with JSDOM on every page-scan iteration).
* `@cu-mkp/editioncrafter`: fixes single-document navigation in the Tag Explorer sidebar. Upstream, clicking a page's "insert left/right" button navigates to a `<document>_<surface>` folio ID, but with only one document the viewer indexes folios by bare surface ID, so the viewer pane stayed blank. (The ODT reference edition has many documents and never hits this.) Both bugs are worth reporting upstream before upgrading these packages.

## Getting Started with EditionCrafter CLI

To learn how to use the EditionCrafter CLI to create your own project, please see the ["Getting Started"](https://editioncrafter.org/getting-started/) section of the EditionCrafter website. Note that the props passed into the components are configurable via the `data/config.json` file.

## Running this Project Locally

To run locally, set the BASE_DIR in the steps above to "." 

Then use the following command:

```npm run start```

## Upgrading EditionCrafter

This repository contains the latest version of EditionCrafter. To upgrade to a newer version in the future, run the following command:

```npm install @cu-mkp/editioncrafter@latest```

Then, upgrade the EditionCrafter CLI using this command:

```npm install @cu-mkp/editioncrafter-cli@latest```

## Credits

Developed by the [Making and Knowing Project](https://www.makingandknowing.org/) at the Center for Science and Society at Columbia University and [Performant Software Solutions LLC](https://www.performantsoftware.com). Funded by Grant SES-2218218 from the National Science Foundation.
