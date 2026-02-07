**load** method of the *Connection* class imports data into an existing dataset on disk or in memory. It is very similar to the `load()` function. The only difference is that `datastore`, `dataset`, and `inmemory` parameters do not need to be passed as they have already been specified while initialzing the *Connection* class.

Parameters description for *load* method of the *Connection* class:

|Name           |Type    |Description                                | Default   |
|-------------- |------- |------------------------------------------ |---------- |
|inputfile      |string  | A file to be loaded |REQUIRED |
|inputformat    |string  | Format of the file to be loaded |REQUIRED |
|isinputpath    |bool    |`True` if the inputfile is the file path, otherwise the inputfile is the content |REQUIRED |
|config         |dict    | A dictionary with configurations for certain backend store |see below |

Description for the *config* parameter:

??? info "datastore: duckdb"

    |Name           |Type    |Description                    | Default    |
    |-------------- |------- |------------------------------ |----------- |
    |table          |string  |Name of the table to be loaded |REQUIRED    |

    ??? example "Example: load a table into the `test` dataset"

        There exist a file with the path of `.geistdata/duckdb/test.duckdb`. The `csv_str` will be imported into the `df` table. Note that the order of table columns should be consistent with the imported data.

        ```
        import geist

        csv_str = """
        v1,v2,v3
        1,1,1
        2,2,2
        3,3,3
        """

        # Create a Connection instance
        connection = geist.Connection.connect(datastore='duckdb', dataset='test')
        # Load csv_str to the df table of the test dataset
        connection.load(inputfile=csv_str, inputformat='csv', isinputpath=False, config={'table': 'df'})
        ```

??? info "datastore: rdflib"
    
    |Name           |Type    |Description                    | Default    |
    |-------------- |------- |------------------------------ |----------- |
    |colnames       |string  | Column names of triples with the format of `[[subject1, predicate1, object1], [subject2, predicate2, object2], ...]` |REQUIRED when `inputformat='csv'` |

    ??? example "Example: load a triple into the `test` dataset"

        There exist a file with the path of `.geistdata/rdflib/test.pkl`. The `csv_str` will be imported into the `test` RDF dataset.

        ```
        import geist

        csv_str = """
        subject,predicate,object
        <http://example.com/drewp>,<http://example.com/feels>,"Happy"
        """

        # Create a Connection instance
        connection = geist.Connection.connect(datastore='rdflib', dataset='test')
        # Load csv_str to the test dataset
        connection.load(inputfile=csv_str, inputformat='csv', isinputpath=False, config={"colnames": "[['subject', 'predicate', 'object']]"})
        ```

??? info "datastore: clingo"

    |Name           |Type    |Description                    | Default    |
    |-------------- |------- |------------------------------ |----------- |
    |predicate      |string  |`'isfirstcol'` for using the first column as the predicate name; strings other than `'isfirstcol'` are used as the predicate name directly |`'isfirstcol'` |
    |programname    |string  |Name of the program            |`'base'`    |

    ??? example "Example: load facts into the `test` ASP dataset"

        There exist a file with the path of `.geistdata/clingo/test.pkl`. The `lp_str` will be imported into the `test` ASP dataset.

        ```
        import geist

        lp_str = """
        friends(b, d).
        """

        # Create a Connection instance
        connection = geist.Connection.connect(datastore='clingo', dataset='test')
        # Load lp_str into the test ASP dataset
        connection.load(inputfile=lp_str, inputformat='lp', isinputpath=False)
        ```
