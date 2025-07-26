# Setup

Install Geist:
```python
pip install geist-p
```

You can also install the development version of Geist:
```python
pip install git+https://github.com/CIRSS/geist-p.git@develop
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