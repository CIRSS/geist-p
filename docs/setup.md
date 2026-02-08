# Setup

Install Geist with the backend(s) you need:
```bash
pip install geist-p[duckdb]    # DuckDB module
pip install geist-p[rdflib]    # RDFLib module
pip install geist-p[clingo]    # Clingo module
pip install geist-p[all]       # All backends
```

You can also combine multiple backends:
```bash
pip install geist-p[duckdb,rdflib]
```

To install the development version:
```bash
pip install "geist-p[duckdb] @ git+https://github.com/CIRSS/geist-p.git@develop"
pip install "geist-p[rdflib] @ git+https://github.com/CIRSS/geist-p.git@develop"
pip install "geist-p[clingo] @ git+https://github.com/CIRSS/geist-p.git@develop"
pip install "geist-p[all] @ git+https://github.com/CIRSS/geist-p.git@develop"
```

To check Geist is working, run `geist` in the command line. You should get the following output:
```
Usage: geist [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create   Create a new dataset
  destroy  Delete a dataset
  export   Export a dataset
  graph    Visualize a dataset
  load     Import data into a dataset
  query    Perform a query on a dataset
  report   Expand a report using dataset(s)
```