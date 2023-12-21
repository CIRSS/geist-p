# Setup

Geist will be available on PyPI. You should be able to install it via `pip install geist` in the near future.

For now, the best way to get it is through GitHub:
```python
pip install geist-p@git+https://github.com/CIRSS/geist-p
```

To check Geist is working, run `geist` in the command line. You should get the following output:
```
Usage: geist [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create   Create a new RDF dataset
  destroy  Delete an RDF dataset
  export   Export an RDF graph
  graph    Visualize an RDF dataset
  load     Import data into an RDF dataset
  query    Perform a SPARQL query on an RDF dataset
  report   Expand a report using an RDF dataset
```