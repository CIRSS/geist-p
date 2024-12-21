**graph** function can visualize a dataset. Only `rdflib` is supported for now.

Parameters description for *export()*:

|Name           |Type    |Description                                | Default   |
|-------------- |------- |------------------------------------------ |---------- |
|datastore      |string  |A backend datastore, i.e., `rdflib` or `duckdb`|`[required]` |
|dataset        |string OR `GeistGraph` object |Dataset to load an object: (1) A string indicates the name of the dataset stored on disk OR (2) a `GeistGraph` object for dataset in memory |`[required]` |
|hasoutput      |bool    |`True` to export as a file or print it out   |`[required]` |
|config         |dict    |A dictionary with configurations for certain backend store | see below |

Description for the *config* parameter:

=== "datastore: rdflib"
    
    |Key            |Type    |Description                                  | Default   |
    |-------------- |------- |-------------------------------------------- |---------- |
    |rankdir        |string  |Direction of the graph: `TB` or `BT` or `LR` or `RL` |`TB`       |
    |mappings       |string  |File of the mappings to shorten text (str): path of a JSON file, where the key is the original text and the value is the shorter text |`None` |
    |on             |string  |Column(s) to be mapped |`None` |
    |samecolor      |bool    |`True` to use the same color for same edges, otherwise False |`True` |
    |outputroot     |string  |Path of the directory to store the graph | `./` |
    |outputfile     |string  |Path of the file without extension to store the graph | `res` |
    |outputformats  |list    |Format of the graph: `none` or `svg` or `png` or `gv` |`[none]` |

??? example "Example: visualize the `test` dataset"

    ```
    import geist

    # Visualize the test dataset as a graph and save it as the res.svg file
    geist.graph(datastore='rdflib', dataset='test', hasoutput=True, config={'outputformats': ['svg']})
    ```