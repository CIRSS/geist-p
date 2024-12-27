**load** method of the *Connection* class imports data into an existing dataset on disk or in memory. It is very similar to the `load()` function. The only difference is that `datastore`, `dataset`, and `inmemory` parameters do not need to be passed as they have already been specified while initialzing the *Connection* class.

Parameters description for *load* method of the *Connection* class:

|Name           |Type    |Description                                | Default   |
|-------------- |------- |------------------------------------------ |---------- |
|inputfile      |string  |A file to be loaded                        |[required] |
|inputformat    |string  |Format of the file to be loaded            |[required] |
|isinputpath    |bool    |True if the inputfile is the file path, otherwise the inputfile is the content |[required] |
|config         |dict    |A dictionary with configurations for certain backend store | see below |

Description for the *config* parameter:

=== "datastore: duckdb"

    |Key            |Type    |Description                                | Default   |
    |-------------- |------- |------------------------------------------ |---------- |
    |table          |string  |Name of the table to be loaded             |[required] |

=== "datastore: rdflib"
    
    |Key            |Type    |Description                                | Default   |
    |-------------- |------- |------------------------------------------ |---------- |
    |colnames       |string  |Column names of triples with the format of [[subject1, predicate1, object1], [subject2, predicate2, object2], ...] | [required] when `inputformat`='csv' |

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
