**load** function can import data into an existing dataset.

Parameters description for *query()*:

|Name           |Type    |Description                    | Default    |
|-------------- |------- |------------------------------ |----------- |
|datastore      |string | A backend datastore, i.e., `'rdflib'` or `'duckdb'` |REQUIRED |
|dataset        |string OR `DuckPyConnection` object OR `GeistGraph` object |Dataset to load an object: (1) A string indicates the name of the dataset stored on disk OR (2) a `DuckPyConnection` object OR a `GeistGraph` object for dataset in memory |REQUIRED |
|inputfile      |string | File to be loaded |REQUIRED |
|inputformat    |string | Format of the file to be loaded |REQUIRED |
|isinputpath    |bool   |`True` if the inputfile is the file path, otherwise the inputfile is the content |REQUIRED |
|config         |dict   | A dictionary with configurations for certain backend store |see below |

Description for the *config* parameter:

??? info "datastore: duckdb"

    |Name           |Type    |Description                    | Default    |
    |-------------- |------- |------------------------------ |----------- |
    |table          |string  |Name of the table to be loaded |REQUIRED|

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

        # Load csv_str to the df table of the test dataset
        geist.load(datastore='duckdb', dataset='test', inputfile=csv_str, inputformat='csv', isinputpath=False, config={'table': 'df'})
        ```

??? info "datastore: rdflib"
    
    |Name           |Type    |Description                    | Default    |
    |-------------- |------- |------------------------------ |----------- |
    |inmemory       |bool    |`True` if the new dataset (after loading data) is stored in memory only, otherwise it is stored on disk |`False` |
    |colnames       |string  |Column names of triples with the format of `[[subject1, predicate1, object1], [subject2, predicate2, object2], ...]` |REQUIRED when `inputformat='csv'` |

    ??? example "Example: load a triple into the `test` dataset"

        There exist a file with the path of `.geistdata/rdflib/test.pkl`. The `csv_str` will be imported into the `test` RDF dataset.

        ```
        import geist

        csv_str = """
        subject,predicate,object
        <http://example.com/drewp>,<http://example.com/feels>,"Happy"
        """

        # Load csv_str to the df table of the test dataset
        geist.load(datastore='rdflib', dataset='test', inputfile=csv_str, inputformat='csv', isinputpath=False, config={"colnames": "[['subject', 'predicate', 'object']]"})
        ```
