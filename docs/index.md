# Welcome to Geist documentation

Geist is a new templating language for declarative data manipulation, query, and report generation. Building on the [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/intro/) template engine, Geist is designed to support diverse data backends and query engines via predefined tags and filters, and may be extended with custom tags. A single Geist template may include multiple queries expressed in different languages, e.g. SQL and SPARQL, to leverage the strengths of each for clarity and ease of maintenance. Because Geist both can generate reports in diverse formats and perform inserts and updates on new or existing databases during template expansion, Geist templates may orchestrate data extraction, transformation, and load operations spanning multiple tools and data storage systems. The Geist Python package can be installed easily and accessed via the command line. If your dataset is stored in DuckDB and SPARQL queries are more suitable for your problem, then Geist might be for you! Check out our [Poster](https://zenodo.org/records/13942280) for [SciPy 2024](https://www.scipy2024.scipy.org)!

At the moment, Geist supports [DuckDB](https://duckdb.org), [RDFLib](https://rdflib.readthedocs.io), and [Clingo](https://potassco.org/clingo/).

## Features

Both CLI and Python API provide the following features:

* [report](features/report.md) feature: expand a report using dataset(s)
* [create](features/create.md) feature: create a new dataset
* [destroy](features/destroy.md) feature: delete a dataset
* [export](features/export.md) feature: export a graph
* [graph](features/graph.md) feature: visualize a dataset
* [load](features/load.md) feature: import data into a dataset
* [query](features/query.md) feature: perform a query on a dataset

## Demo for SciPy 2024

**A Geist report that employs two different query languages**. We demonstrate how Geist can be used to extract triples from a relational database, store them as a RDF dataset, and perform SPARQL queries on it. Instead of purely in-memory operations, Geist can be used to migrate data. With the hamming numbers dataset stored in DuckDB as an input, we generate a [report](scipy-2024-demo/report.html) to describe the original dataset and the subgraph extracted via SQL and SPARQL queries using a single [Geist script](https://github.com/CIRSS/geist-p/blob/main/demo/04-scipy-2024/run.sh).
