# Setup

Before installing Geist, please make sure [Graphviz](https://graphviz.org/download/) is installed. 
??? example "Example: GitHub Codespaces"

    ```bash
    sudo apt-get update && sudo apt-get install -y graphviz graphviz-dev
    ```

??? example "Example: Google Colab (Jupyter Notebook)"

    ```
    apt install libgraphviz-dev
    ```

Install Geist:
```python
pip install geist-p
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