**create** method of the *Connection* class creates a new dataset on disk or in memory. It is very similar to the `create()` function. The only difference is that the `datastore` and the `dataset` parameters do not need to be passed as they have already been specified while initialzing the *Connection* class.

Parameters description for *create* method of the *Connection* class:

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
    |table          |string  |Name of the table to be created            |df         |

=== "datastore: rdflib"
    
    |Key            |Type    |Description                                | Default   |
    |-------------- |------- |------------------------------------------ |---------- |
    |colnames       |string  |Column names of triples with the format of [[subject1, predicate1, object1], [subject2, predicate2, object2], ...] | [required] when `inputformat`='csv' |
    |infer          |string  |Inference to perform on update, i.e., none, [rdfs](https://owl-rl.readthedocs.io/en/latest/RDFSClosure.html#owlrl.RDFSClosure.RDFS_Semantics), [owl](https://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules), or [rdfs_owl](https://owl-rl.readthedocs.io/en/latest/CombinedClosure.html#owlrl.CombinedClosure.RDFS_OWLRL_Semantics) | none |

??? example "Example 1: create a `test` SQL dataset from a string"

    The `.geistdata/duckdb/test.duckdb` file is created and a `Connection` instance is returned.

    ```
    import geist

    csv_str = """
    v1,v2,v3
    1,2,3
    4,5,6
    7,8,9
    """

    # Create a Connection instance
    connection = geist.Connection(datastore='duckdb', dataset='test')
    connection.create(inputfile=csv_str, inputformat="csv", isinputpath=False, config={"table": "df"})
    ```

??? example "Example 2: create a `test` SQL dataset from a file"

    The `.geistdata/duckdb/test.duckdb` file is created and a `Connection` instance is returned.

    Here is the `test.csv` file:

    ```file
    v1,v2,v3
    1,2,3
    4,5,6
    7,8,9
    ```

    Code:
    ```
    import geist

    # Create a Connection instance
    connection = geist.Connection(datastore='duckdb', dataset='test')
    connection.create(inputfile="test.csv", inputformat="csv", isinputpath=True, config={"table": "df"})
    ```

??? example "Example 3: create a SQL dataset in memory from a string"

    A `Connection` instance is returned.

    ```
    import geist

    csv_str = """
    v1,v2,v3
    1,2,3
    4,5,6
    7,8,9
    """

    # Create a Connection instance
    connection = geist.Connection(datastore='duckdb', dataset=':memory:')
    connection.create(inputfile=csv_str, inputformat="csv", isinputpath=False, config={"table": "df"})
    ```

??? example "Example 4: create a SQL dataset in memory from a file"

    A `Connection` instance is returned.

    Here is the `test.csv` file:

    ```file
    v1,v2,v3
    1,2,3
    4,5,6
    7,8,9
    ```

    Code:
    ```
    import geist

    # Create a Connection instance
    connection = geist.Connection(datastore='duckdb', dataset=':memory:')
    connection.create(inputfile="test.csv", inputformat="csv", isinputpath=True, config={"table": "df"})
    ```