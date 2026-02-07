**export** function can export a dataset.

Parameters description for *export()*:

|Name           |Type    |Description                    | Default    |
|-------------- |------- |------------------------------ |----------- |
|datastore      |string  |A backend datastore, i.e., `'clingo'`, `'duckdb'`, or `'rdflib'` |REQUIRED |
|dataset        |string OR `Control` object OR `DuckPyConnection` object OR `GeistGraph` object |Dataset to load an object: (1) A string indicates the name of the dataset stored on disk OR (2) a `Control` object, a `DuckPyConnection` object, or a `GeistGraph` object for dataset in memory |REQUIRED |
|hasoutput      |bool    |`True` to export as a file or print it out |REQUIRED |
|config         |dict    |A dictionary with configurations for certain backend store |see below |

Description for the *config* parameter:

??? info "datastore: clingo"

    |Name           |Type    |Description                    | Default    |
    |-------------- |------- |------------------------------ |----------- |
    |returnformat   |string  |Format of the returned data, i.e., `'lp'`, `'df'`, or `'dict'` |`'lp'` |
    |predicate      |string  |Name of the predicate to be exported |`None` |

    ??? example "Example 1: export all facts of the `test` ASP dataset on disk"

        There exist a file with the path of `.geistdata/clingo/test.pkl`. The following code returns data and a `Control` object named `conn`.

        ```
        import geist

        # Export all facts of the test ASP dataset
        (data, conn) = geist.export(datastore='clingo', dataset='test', hasoutput=False)
        ```

    ??? example "Example 2: export all facts of the `test` ASP dataset in memory"

        Suppose `conn` is a `Control` object pointing to an ASP dataset in memory. The following code returns data and the same `Control` object named `conn`.

        ```
        import geist

        # Export all facts of the test ASP dataset
        (data, conn) = geist.export(datastore='clingo', dataset=conn, hasoutput=False)
        ```

??? info "datastore: duckdb"

    |Name           |Type    |Description                    | Default    |
    |-------------- |------- |------------------------------ |----------- |
    |outputroot     |string  |Path of the directory to store the exported table |`'./'` |
    |outputfile     |string  |Path of the file to store the exported table |`None`      |
    |outputformat   |string  |Format of the exported table, i.e., `csv` or `json` |`'csv'` |
    |table          |string  |Name of the table to be exported |`'df'`    |

    ??? example "Example 1: export all rows of the `df` table in `test` dataset on disk"

        There exist a file with the path of `.geistdata/duckdb/test.duckdb`. The following code returns a Pandas data frame named `data` and a `DuckPyConnection` object named `conn`.

        ```
        import geist

        # Export the df table of the test dataset
        (data, conn) = geist.export(datastore='duckdb', dataset='test', hasoutput=False, config={'table': 'df'})
        ```

    ??? example "Example 2: export all rows of the `df` table in `test` dataset in memory"

        Suppose `conn` is a `DuckPyConnection` object points to a DuckDB dataset in memory. The following code returns a Pandas data frame named `data` and the same `DuckPyConnection` object named `conn`.

        ```
        import geist

        # Export the df table of the test dataset
        (data, conn) = geist.export(datastore='duckdb', dataset=conn, hasoutput=False, config={'table': 'df'})
        ```

??? info "datastore: rdflib"
    
    |Name           |Type    |Description                    | Default    |
    |-------------- |------- |------------------------------ |----------- |
    |outputroot     |string  |Path of the directory to store these exported triples |`'./'` |
    |outputfile     |string  |Path of the file to store these exported triples |`None`      |
    |outputformat   |string  |Format of the exported triples, i.e., `'json-ld'`, `'n3'`, `'nquads'`, `'nt'`, `'hext'`, `'pretty-xml'`, `'trig'`, `'trix'`, `'turtle'`, `'longturtle'`, or `'xml'` |`'nt'` |

    ??? example "Example 1: export all triples of the `test` dataset on disk"

        There exist a file with the path of `.geistdata/rdflib/test.pkl`. The following code returns a string named `data` and a `GeistGraph` object named `conn`.

        ```
        import geist

        # Export all triples of the test dataset
        (data, conn) = geist.export(datastore='rdflib', dataset='test', hasoutput=False)
        ```

    ??? example "Example 2: export all triples of the `test` dataset in memory"

        Suppose `conn` is a `GeistGraph` object points to a RDF dataset in memory. The following code returns a string named `data` and the same `GeistGraph` object named `conn`.

        ```
        import geist

        # Export all triples of the test dataset
        (data, conn) = geist.export(datastore='rdflib', dataset=conn, hasoutput=False)
        ```
