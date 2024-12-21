**export** function can export a dataset.

Parameters description for *export()*:

|Name           |Type    |Description                                | Default   |
|-------------- |------- |------------------------------------------ |---------- |
|datastore      |string  |A backend datastore, i.e., `rdflib` or `duckdb`|`[required]` |
|dataset        |string OR `DuckPyConnection` object OR `GeistGraph` object |Dataset to load an object: (1) A string indicates the name of the dataset stored on disk OR (2) a `DuckPyConnection` object OR a `GeistGraph` object for dataset in memory |[required] |
|hasoutput      |bool    |`True` to export as a file or print it out   |`[required]` |
|config         |dict    |A dictionary with configurations for certain backend store | see below |

Description for the *config* parameter:

=== "datastore: duckdb"

    |Key            |Type    |Description                                | Default   |
    |-------------- |------- |------------------------------------------ |---------- |
    |outputroot     |string  |Path of the directory to store the exported table | `./` |
    |outputfile     |string  |Path of the file to store the exported table | `None`      |
    |outputformat   |string  |Format of the exported table, i.e., `csv` or `json` |`csv` |
    |table          |string  |Name of the table to be exported           |`df`         |

=== "datastore: rdflib"
    
    |Key            |Type    |Description                                      | Default   |
    |-------------- |------- |------------------------------------------------ |---------- |
    |outputroot     |string  |Path of the directory to store these exported triples | `./` |
    |outputfile     |string  |Path of the file to store these exported triples | `None`      |
    |outputformat   |string  |Format of the exported triples, i.e., `json-ld`, `n3`, `nquads`, `nt`, `hext`, `pretty-xml`, `trig`, `trix`, `turtle`, `longturtle`, or `xml`. |`nt` |

??? example "Example 1: export all rows of the `df` table in `test` dataset on disk"

    There exist a file with the path of `.geistdata/duckdb/test.duckdb`. The following code returns a Pandas data frame named `data` and the DuckPyConnection` object `conn`.

    ```
    import geist

    # Export the df table of the test dataset
    (data, conn) = geist.export(datastore='duckdb', dataset='test', hasoutput=False, config={'table': 'df'})
    ```

??? example "Example 2: export all rows of the `df` table in `test` dataset in memory"

    Suppose `conn` is a `DuckPyConnection` object points to a DuckDB dataset in memory. The following code returns a Pandas data frame named `data` and the same DuckPyConnection` object `conn`.

    ```
    import geist

    # Export the df table of the test dataset
    (data, conn) = geist.export(datastore='duckdb', dataset=conn, hasoutput=False, config={'table': 'df'})
    ```
