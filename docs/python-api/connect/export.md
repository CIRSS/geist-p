**export** method of the *Connection* class exports a dataset. It is very similar to the `export()` function. The only difference is that the `datastore` and the `dataset` parameters do not need to be passed as they have already been specified while initialzing the *Connection* class.

Parameters description for *export* method of the *Connection* class:

|Name           |Type    |Description                                | Default   |
|-------------- |------- |------------------------------------------ |---------- |
|hasoutput      |bool    |`True` to export as a file or print it out |REQUIRED |
|config         |dict    |A dictionary with configurations for certain backend store | see below |

Description for the *config* parameter:

??? info "datastore: duckdb"

    |Key            |Type    |Description                                | Default   |
    |-------------- |------- |------------------------------------------ |---------- |
    |outputroot     |string  |Path of the directory to store the exported table | `'./'` |
    |outputfile     |string  |Path of the file to store the exported table | `None`      |
    |outputformat   |string  |Format of the exported table, i.e., `'csv'` or `'json'` |`'csv'`|
    |table          |string  |Name of the table to be exported           |`'df'`      |

    ??? example "Example 1: export all rows of the `df` table in `test` dataset on disk"

        There exist a file with the path of `.geistdata/duckdb/test.duckdb`. The following code returns a Pandas data frame named `data`.

        ```
        import geist

        # Create a Connection instance
        connection = geist.Connection.connect(datastore='duckdb', dataset='test')
        # Export the df table of the test dataset
        data = connection.export(hasoutput=False, config={'table': 'df'})
        ```

    ??? example "Example 2: export all rows of the `df` table in `test` dataset in memory"

        Suppose `conn` is a `DuckPyConnection` object points to a DuckDB dataset in memory. The following code returns a Pandas data frame named `data`.

        ```
        import geist

        # Create a Connection instance
        connection = geist.Connection(datastore='duckdb', dataset=':memory:', conn=conn)
        # Export the df table of the test dataset
        data = connection.export(hasoutput=False, config={'table': 'df'})
        ```

??? info "datastore: rdflib"

    |Key            |Type    |Description                                      | Default   |
    |-------------- |------- |------------------------------------------------ |---------- |
    |outputroot     |string  |Path of the directory to store these exported triples | `'./'` |
    |outputfile     |string  |Path of the file to store these exported triples | `None`      |
    |outputformat   |string  |Format of the exported triples, i.e., `'json-ld'`, `'n3'`, `'nquads'`, `'nt'`, `'hext'`, `'pretty-xml'`, `'trig'`, `'trix'`, `'turtle'`, `'longturtle'`, or `'xml'` |`'nt'` |

    ??? example "Example 1: export all triples of the `test` dataset on disk"

        There exist a file with the path of `.geistdata/rdflib/test.pkl`. The following code returns a string named `data`.

        ```
        import geist

        # Create a Connection instance
        connection = geist.Connection.connect(datastore='rdflib', dataset='test')
        # Export all triples of the test dataset as a string with the 'nt' format
        data = connection.export(hasoutput=False)
        ```

    ??? example "Example 2: export all triples of the `test` dataset in memory"

        Suppose `conn` is a `GeistGraph` object points to a RDF dataset in memory. The following code returns a string named `data`.

        ```
        import geist

        # Create a Connection instance
        connection = geist.Connection(datastore='rdflib', dataset=':memory:', conn=conn)
        # Export the df table of the test dataset
        data = connection.export(hasoutput=False)
        ```
