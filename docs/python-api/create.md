**create** function can create a new dataset on disk or in memory.

Parameters description for *create()*:

|Name           |Type    |Description                    | Default    |
|-------------- |------- |------------------------------ |----------- |
|datastore      |string  |A backend datastore, i.e., `'rdflib'` or `'duckdb'` |REQUIRED |
|dataset        |string  |Name of the dataset to be created. Note that `':memory:'` is a reserved value for datasets that exist only in memory |REQUIRED |
|inputfile      |string  |A file to be loaded |REQUIRED |
|inputformat    |string  |Format of the file to be loaded |REQUIRED |
|isinputpath    |bool    |`True` if the inputfile is the file path, otherwise the inputfile is the content |REQUIRED |
|config         |dict    |A dictionary with configurations for certain backend store |see below |

Description for the *config* parameter:

??? info "datastore: duckdb"

    |Name           |Type    |Description                    | Default    |
    |-------------- |------- |------------------------------ |----------- |
    |table          |string  |Name of the table to be created|`'df'`      |

    ??? example "Example 1: create a `test` SQL dataset on disk from a string"

        The `.geistdata/duckdb/test.duckdb` file is created and a `DuckDBPyConnection` object is returned.

        ```
        import geist

        csv_str = """
        v1,v2,v3
        1,2,3
        4,5,6
        7,8,9
        """

        # Create a DuckPyConnection object
        conn = geist.create(datastore='duckdb', dataset='test', inputfile=csv_str, inputformat="csv", isinputpath=False, config={"table": "df"})
        ```

    ??? example "Example 2: create a `test` SQL dataset on disk from a file"

        The `.geistdata/duckdb/test.duckdb` file is created and a `DuckDBPyConnection` object is returned.

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

        # Create a DuckPyConnection object
        conn = geist.create(datastore='duckdb', dataset='test', inputfile="test.csv", inputformat="csv", isinputpath=True, config={"table": "df"})
        ```

    ??? example "Example 3: create a SQL dataset in memory from a string"

        A `DuckDBPyConnection` object is returned.

        ```
        import geist

        csv_str = """
        v1,v2,v3
        1,2,3
        4,5,6
        7,8,9
        """

        # Create a DuckPyConnection object
        conn = geist.create(datastore='duckdb', dataset=':memory:', inputfile=csv_str, inputformat="csv", isinputpath=False, config={"table": "df"})
        ```

    ??? example "Example 4: create a SQL dataset in memory from a file"

        A `DuckDBPyConnection` object is returned.

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

        # Create a DuckPyConnection object
        conn = geist.create(datastore='duckdb', dataset=':memory:', inputfile="test.csv", inputformat="csv", isinputpath=True, config={"table": "df"})
        ```

??? info "datastore: rdflib"
    
    |Name           |Type    |Description                    | Default    |
    |-------------- |------- |------------------------------ |----------- |
    |colnames       |string  |Column names of triples with the format of `[[subject1, predicate1, object1], [subject2, predicate2, object2], ...]` |REQUIRED when `inputformat='csv'` |
    |infer          |string  |Inference to perform on update, i.e., `'none'`, [`'rdfs'`](https://owl-rl.readthedocs.io/en/latest/RDFSClosure.html#owlrl.RDFSClosure.RDFS_Semantics), [`'owl'`](https://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules), or [`'rdfs_owl'`](https://owl-rl.readthedocs.io/en/latest/CombinedClosure.html#owlrl.CombinedClosure.RDFS_OWLRL_Semantics) |`'none'` |

    ??? example "Example 1: create a `test` RDF dataset on disk from a string"

        The `.geistdata/rdflib/test.pkl` file is created and a `GeistGraph` object is returned.

        ```
        import geist

        csv_str = """
        subject,predicate,object
        <http://example.com/drewp>,<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>,<http://xmlns.com/foaf/0.1/Person>
        <http://example.com/drewp>,<http://example.com/says>,"Hello World"
        """

        # Create a GeistGraph object: a dictionary with 'rdf_graph' and 'infer' keys
        conn = geist.create(datastore='rdflib', dataset='test', inputfile=csv_str, inputformat="csv", isinputpath=False, config={"colnames": "[['subject', 'predicate', 'object']]"})
        ```

    ??? example "Example 2: create a `test` RDF dataset on disk from a file"

        The `.geistdata/rdflib/test.pkl` file is created and a `GeistGraph` object is returned.

        Here is the `test.csv` file:

        ```file
        subject,predicate,object
        <http://example.com/drewp>,<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>,<http://xmlns.com/foaf/0.1/Person>
        <http://example.com/drewp>,<http://example.com/says>,"Hello World"
        ```

        Code:
        ```
        import geist

        # Create a GeistGraph object: a dictionary with 'rdf_graph' and 'infer' keys
        conn = geist.create(datastore='rdflib', dataset='test', inputfile="test.csv", inputformat="csv", isinputpath=True, config={"colnames": "[['subject', 'predicate', 'object']]"})
        ```

    ??? example "Example 3: create a RDF dataset in memory from a string"

        A `GeistGraph` object is returned.

        ```
        import geist

        csv_str = """
        subject,predicate,object
        <http://example.com/drewp>,<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>,<http://xmlns.com/foaf/0.1/Person>
        <http://example.com/drewp>,<http://example.com/says>,"Hello World"
        """

        # Create a GeistGraph object: a dictionary with 'rdf_graph' and 'infer' keys
        conn = geist.create(datastore='rdflib', dataset=':memory:', inputfile=csv_str, inputformat='csv', isinputpath=False, config={"colnames": "[['subject', 'predicate', 'object']]"})
        ```

    ??? example "Example 4: create a RDF dataset in memory from a file"

        A `GeistGraph` object is returned.

        Here is the `test.csv` file:

        ```file
        subject,predicate,object
        <http://example.com/drewp>,<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>,<http://xmlns.com/foaf/0.1/Person>
        <http://example.com/drewp>,<http://example.com/says>,"Hello World"
        ```

        Code:
        ```
        import geist

        # Create a GeistGraph object: a dictionary with 'rdf_graph' and 'infer' keys
        conn = geist.create(datastore='rdflib', dataset=':memory:', inputfile='test.csv', inputformat='csv', isinputpath=True, config={"colnames": "[['subject', 'predicate', 'object']]"})
        ```
