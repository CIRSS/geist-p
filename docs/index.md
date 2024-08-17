# Welcome to Geist documentation

Geist is a new templating language for declarative data manipulation, query, and report generation. Building on the [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/intro/) template engine, Geist is designed to support diverse data backends and query engines via predefined tags and filters, and may be extended with custom tags. A single Geist template may include multiple queries expressed in different languages, e.g. SQL and SPARQL, to leverage the strengths of each for clarity and ease of maintenance. Because Geist both can generate reports in diverse formats and perform inserts and updates on new or existing databases during template expansion, Geist templates may orchestrate data extraction, transformation, and load operations spanning multiple tools and data storage systems. The Geist Python package can be installed easily and accessed via the command line. If your dataset is stored in DuckDB and SPARQL queries are more suitable for your problem, then Geist might be for you! Check out our [Poster](./SciPy2024Poster.pdf) for [SciPy 2024](https://www.scipy2024.scipy.org)!

At the moment, Geist supports [DuckDB](https://duckdb.org) and [RDFLib](https://rdflib.readthedocs.io). More types of data backends will be available in the near future.

## Commands

* [`report`](commands/report/introduction.md) command: expand a report using a dataset
* [`create`](commands/create.md) command: create a new dataset
* [`destroy`](commands/destroy.md) command: delete a dataset
* [`export`](commands/export.md) command: export a graph
* [`graph`](commands/graph.md) command: visualize a dataset
* [`load`](commands/load.md) command: import data into a dataset
* [`query`](commands/query.md) command: perform a query on a dataset

## Demo for SciPy 2024

**A Geist report that employs two different query languages**. We demonstrate how Geist can be used to extract triples from a relational database, store them as a RDF dataset, and perform SPARQL queries on it. Instead of purely in-memory operations, Geist can be used to migrate data. With the hamming numbers dataset stored in DuckDB as an input, we generate a [report](commands/report/scipy-2024-demo/report.html) to describe the original dataset and the subgraph extracted via SQL and SPARQL queries using a single [Geist script](https://github.com/CIRSS/geist-p/blob/main/demo/04-scipy-2024/run.sh).