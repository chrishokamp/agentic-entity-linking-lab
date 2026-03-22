# Wikidata Entity Linking Lab

This repository is a bootstrap lab for simple entity linking backed by Wikidata. The README is also the intro presentation: you can present directly from it, then point students into the notebook in [`notebooks/01_wikidata_bootstrap_entity_linking.ipynb`](/Users/christopherhokamp/projects/agentic-entity-linking-lab/notebooks/01_wikidata_bootstrap_entity_linking.ipynb).

## Lab Topic

Wikidata, open knowledge graphs, SPARQL, and agentic entity linking.

## Session Format

1. 10-15 minute intro on Wikidata, SPARQL, and the lab pipeline.
2. Students start from a bare-bones local KB bootstrapped from a single SPARQL query.
3. Students extend the spotter, linker, vector retrieval, or agentic layer with support from lab monitors.

## Core Idea

The pipeline is intentionally simple and explicit:

1. `Documents`
2. `Spot`
3. `Disambiguate`
4. `Use`
5. `Evaluate`

The starting point is just:

1. Run one SPARQL query against Wikidata.
2. Turn the results into a tiny local KB.
3. Build a surface-form dictionary from that KB.
4. Annotate text with exact string matching.

That baseline works with standard Python and the notebook alone. No embedding model, vector DB, or LLM backend is required for the default exercise.

## Default Domain

The default KB bootstrap targets:

`living people currently holding a political office in Ireland`

Operationally, the default SPARQL query asks for:

1. Humans (`wdt:P31 wd:Q5`)
2. With Irish citizenship (`wdt:P27 wd:Q27`)
3. With occupation politician (`wdt:P106 wd:Q82955`)
4. With a current `position held` statement (`p:P39`)
5. With no death date
6. With no end date on the office-holding statement
7. Where the office is tied to Ireland via `country` or `applies to jurisdiction`

## What Students See

Nothing important is hidden.

Students can inspect and change:

1. The SPARQL string itself in [`src/wikidata_lab/wikidata.py`](/Users/christopherhokamp/projects/agentic-entity-linking-lab/src/wikidata_lab/wikidata.py) and in the notebook.
2. The raw rows returned by Wikidata.
3. The code that groups those rows into a local KB.
4. The code that builds the surface-form index.
5. The exact string-matching annotator.

That is deliberate. The KB bootstrap should be understandable, editable, and easy to repurpose.

## How To Change Or Expand The KB

To explore a different domain, students only need to change the query and rerun the notebook.

Examples:

1. Replace Irish politicians with Irish musicians by changing `wd:Q82955`.
2. Replace Ireland with another country by changing `wd:Q27`.
3. Remove the office filter to get a broader list of people.
4. Add more properties to inspect, such as party membership, gender, place of birth, or aliases.
5. Start from a different seed query entirely and keep the same local linking pipeline.

The key teaching point is:

`the local KB is just the result of a SPARQL query plus a little Python glue`

## Repo Layout

- [`notebooks/01_wikidata_bootstrap_entity_linking.ipynb`](/Users/christopherhokamp/projects/agentic-entity-linking-lab/notebooks/01_wikidata_bootstrap_entity_linking.ipynb): baseline hands-on notebook
- [`src/wikidata_lab/wikidata.py`](/Users/christopherhokamp/projects/agentic-entity-linking-lab/src/wikidata_lab/wikidata.py): explicit SPARQL fetch, KB construction, and string-match linker
- [`src/wikidata_lab/extensions.py`](/Users/christopherhokamp/projects/agentic-entity-linking-lab/src/wikidata_lab/extensions.py): vector retrieval and agentic linking templates
- [`tests/test_wikidata.py`](/Users/christopherhokamp/projects/agentic-entity-linking-lab/tests/test_wikidata.py): offline unit tests
- [`tests/test_live_wikidata.py`](/Users/christopherhokamp/projects/agentic-entity-linking-lab/tests/test_live_wikidata.py): live API integration test

## Intro Presentation

### 1. What is Wikidata?

Wikidata is an open knowledge graph. Entities have stable identifiers such as `Q27` for Ireland, labels, aliases, and graph relations.

For entity linking, that gives us:

1. A knowledge base we can query live.
2. Stable URIs for linked entities.
3. Labels and aliases that can become surface forms.
4. Extra graph structure for disambiguation and fact checking.

### 2. What is SPARQL?

SPARQL is the graph query language used to retrieve a domain-specific slice of the KB.

In this lab, SPARQL is not just a background detail. It is the mechanism that builds the local KB students will work with.

### 3. Why start with a local KB?

Because it makes the entity linking task concrete.

Instead of trying to link every entity in the world, we bootstrap a compact domain KB and work against that first.

This has three advantages:

1. Students understand the search space.
2. The baseline can be built with no extra dependencies.
3. The extension path is clear: better spotting, better candidate retrieval, better disambiguation.

### 4. Baseline Pipeline

The baseline is:

1. `SPARQL query -> raw rows`
2. `raw rows -> local KB`
3. `local KB -> surface-form index`
4. `text -> matched surface forms -> Wikidata URIs`

This is a rule-based string matcher. It is intentionally unsophisticated.

That is useful pedagogically because students can immediately see:

1. what works,
2. what fails,
3. and where vector or agentic methods help.

### 5. Extension Routes

Students can extend in several directions:

1. Spotting: better mention detection, alias expansion, abbreviation handling, fuzzy matching.
2. Linking logic: tie-breaking, office-aware heuristics, context windows.
3. Vector retrieval: embed mentions and entities, retrieve candidates from a vector store, then disambiguate.
4. Agentic linking: give the model mention text, context, and candidates and ask it to decide.
5. Evaluation: exact-match metrics and optional LLM-as-a-judge workflows.

## Setup Requirements

Baseline:

1. `git`
2. Python 3.10+
3. Jupyter Notebook or JupyterLab

Optional agentic work:

1. Access to an OpenAI-compatible LLM API, or
2. A local model setup such as Ollama

We do not assume session time will be spent on API setup. Students who want agentic extensions should ideally arrive with that already working.

For agentic harnesses, the recommended reference is the Claude Agent SDK:

<https://github.com/anthropics/claude-agent-sdk-python>

## Quick Start

```bash
git clone <repo-url>
cd agentic-entity-linking-lab
jupyter notebook
```

Then open:

[`notebooks/01_wikidata_bootstrap_entity_linking.ipynb`](/Users/christopherhokamp/projects/agentic-entity-linking-lab/notebooks/01_wikidata_bootstrap_entity_linking.ipynb)

## The Default SPARQL Query

The repository keeps the query in code so students can edit it directly:

[`src/wikidata_lab/wikidata.py`](/Users/christopherhokamp/projects/agentic-entity-linking-lab/src/wikidata_lab/wikidata.py)

The default query returns raw rows with:

1. `person`
2. `personLabel`
3. `office`
4. `officeLabel`

The notebook then groups rows by person and turns `personLabel` into the initial surface form.

That choice is intentional:

1. it keeps the live query readable,
2. it keeps the KB bootstrap fast enough for a classroom setting,
3. and it makes alias expansion an explicit exercise instead of hidden magic.

## How Students Explore The KB

Suggested first steps in the notebook:

1. Print the raw SPARQL query.
2. Print a few raw result rows.
3. Inspect the grouped local KB.
4. Add a new property to the query.
5. Add a few aliases or alternate surface forms.
6. Run the string matcher on a short paragraph and inspect the spans.

Suggested domain changes:

1. Irish ministers only
2. Irish MEPs
3. Irish athletes
4. Irish universities
5. Irish locations

## Vector Retrieval Template

The vector template in [`src/wikidata_lab/extensions.py`](/Users/christopherhokamp/projects/agentic-entity-linking-lab/src/wikidata_lab/extensions.py) mirrors the same decomposition used in the SNOMED project:

1. Start with entities in a local KB.
2. Index entities into a vector store.
3. Retrieve top-k candidates for a mention.
4. Use the candidate list for disambiguation.

The template is dependency-free and backend-agnostic. Students only need to plug in an embedding provider.

## Agentic Linking Template

The agentic template also follows the reference project structure:

1. Keep the baseline candidate set explicit.
2. Extract a context window from the source text.
3. Build a prompt containing mention, context, and candidates.
4. Let an injected LLM backend choose the final URI.

This keeps the harness simple while preserving the important architecture:

`retrieval first, reasoning second`

## Evaluation

The baseline repository does not force a particular evaluation format, but there are two natural levels:

1. Deterministic evaluation against a small hand-labeled set.
2. Optional LLM-as-a-judge workflows for exploratory analysis.

## Tests

Run offline unit tests:

```bash
python3 -m unittest discover -s tests -v
```

Run live Wikidata integration tests:

```bash
LIVE_WIKIDATA_TESTS=1 python3 -m unittest tests.test_live_wikidata -v
```

The live test hits the real Wikidata Query Service and checks that the default query still returns valid rows.

## Teaching Notes

If the room splits into setup help and coding work, the coding track can proceed immediately with:

1. the baseline query,
2. the local KB,
3. the string matcher,
4. and one extension path.

That keeps the workshop productive even if some students are still sorting out local environments.
