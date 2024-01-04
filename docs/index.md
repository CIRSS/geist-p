# Welcome to Geist documentation

Geist is a templating language to manipulate, query, and report data. At the moment, Geist supports RDF dataset. More types of datasets will be supported in the near future.

The [geist-p](https://github.com/CIRSS/geist-p) GitHub repository is the Python implementation of it. It can load various formats of files as RDF graph objects, and store them as PKL files together with the corresponding inference information. Each PKL file is a dataset stored under the `.geistdata` folder, where the filename is consistent with the `--dataset` field. Thanks to [RDFLib](https://rdflib.readthedocs.org/), Geist can create, load, destroy, export, visualize, and query a dataset. Furthermore, [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/intro/) makes it possible to do nested queries and expand a report (i.e., a Geist template) using a dataset, which makes it easier to generate customized reusable interactive report, such as a HTML file.

## Commands

* [`report`](commands/report/introduction.md) command: expand a report using a dataset
* [`create`](commands/create.md) command: create a new RDF dataset
* [`destroy`](commands/destroy.md) command: delete an RDF dataset
* [`export`](commands/export.md) command: export an RDF graph
* [`graph`](commands/graph.md) command: visualize a dataset
* [`load`](commands/load.md) command: import data into an RDF dataset
* [`query`](commands/query.md) command: perform a SPARQL query on a dataset
