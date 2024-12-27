# Changelog

## v0.3.0

- Code refactoring: datastores -> api -> commands (e.g., code under the api folder is based on code under the datastore folder)
- Add Python API: (1) Connection class with create, close, destroy, export, graph, load, and query methods; and (2) create, destroy, export, graph, load, query, and report functions
- Update CLI of report and query commands: replace --file with --inputfile
- Update the documentation

## v0.2.1

- Add the Geist Poster for [SciPy 2024](https://www.scipy2024.scipy.org)
- Update the documentation: add descriptions for the demo of SciPy 2024

## v0.2.0

- SQL queries are supported by GEIST based on [duckdb](https://duckdb.org)
- Update ContainerTag: return objects of any type, not just strings

## v0.1.0

- Add [documentation](https://cirss.github.io/geist-p)
- Add the component tag to extract connected components of a given graph
- Add the process_str_for_html filter
- Make the map tag more flexible: make it possible to map selected columns
- Fix the quotes bug: keep the cell's original format

## v0.0.1

- The first version of GEIST with create, load, query, destroy, graph, graph2, map, use, html, img, and table tags
- SPARQL queries are supported by GEIST based on [RDFLib](https://github.com/RDFLib/rdflib)
