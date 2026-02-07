**create** method of the *Connection* class creates a new dataset on disk or in memory. It is very similar to the `create()` function. The only difference is that the `datastore` and the `dataset` parameters do not need to be passed as they have already been specified while initialzing the *Connection* class.

Parameters description for *create* method of the *Connection* class:

|Name           |Type    |Description                                | Default     |
|-------------- |------- |------------------------------------------ |----------   |
|inputfile      |string  |A file to be loaded                        |REQUIRED |
|inputformat    |string  |Format of the file to be loaded            |REQUIRED |
|isinputpath    |bool    |`True` if the inputfile is the file path, otherwise the inputfile is the content |REQUIRED |
|config         |dict    |A dictionary with configurations for certain backend store | see below |

Description for the *config* parameter:

??? info "datastore: duckdb"

    |Key            |Type    |Description                                | Default   |
    |-------------- |------- |------------------------------------------ |---------- |
    |table          |string  |Name of the table to be created            |`'df'`     |

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

??? info "datastore: rdflib"
    
    |Key            |Type    |Description                                | Default   |
    |-------------- |------- |------------------------------------------ |---------- |
    |colnames       |string  |Column names of triples with the format of `[[subject1, predicate1, object1], [subject2, predicate2, object2], ...]`. |REQUIRED when `inputformat='csv'`) |
    |infer          |string  |Inference to perform on update, i.e., `'none'`, [`'rdfs'`](https://owl-rl.readthedocs.io/en/latest/RDFSClosure.html#owlrl.RDFSClosure.RDFS_Semantics), [`'owl'`](https://www.w3.org/TR/owl2-profiles/#Reasoning_in_OWL_2_RL_and_RDF_Graphs_using_Rules), or [`'rdfs_owl'`](https://owl-rl.readthedocs.io/en/latest/CombinedClosure.html#owlrl.CombinedClosure.RDFS_OWLRL_Semantics) |`'none'` |

    ??? example "Example 1: create a `test` RDF dataset from a string"

        The `.geistdata/rdflib/test.pkl` file is created and a `Connection` instance is returned.

        ```
        import geist

        csv_str = """
        subject,predicate,object
        <http://example.com/drewp>,<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>,<http://xmlns.com/foaf/0.1/Person>
        <http://example.com/drewp>,<http://example.com/says>,"Hello World"
        """

        # Create a Connection instance
        connection = geist.Connection(datastore='rdflib', dataset='test')
        connection.create(inputfile=csv_str, inputformat="csv", isinputpath=False, config={"colnames": "[['subject', 'predicate', 'object']]"})
        ```

    ??? example "Example 2: create a `test` RDF dataset from a file"

        The `.geistdata/rdflib/test.pkl` file is created and a `Connection` instance is returned.

        Here is the `test.csv` file:

        ```file
        subject,predicate,object
        <http://example.com/drewp>,<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>,<http://xmlns.com/foaf/0.1/Person>
        <http://example.com/drewp>,<http://example.com/says>,"Hello World"
        ```

        Code:
        ```
        import geist

        # Create a Connection instance
        connection = geist.Connection(datastore='rdflib', dataset='test')
        connection.create(inputfile="test.csv", inputformat="csv", isinputpath=True, config={"colnames": "[['subject', 'predicate', 'object']]"})
        ```

    ??? example "Example 3: create a RDF dataset in memory from a string"

        A `Connection` instance is returned.

        ```
        import geist

        csv_str = """
        subject,predicate,object
        <http://example.com/drewp>,<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>,<http://xmlns.com/foaf/0.1/Person>
        <http://example.com/drewp>,<http://example.com/says>,"Hello World"
        """

        # Create a Connection instance
        connection = geist.Connection(datastore='rdflib', dataset=':memory:')
        connection.create(inputfile=csv_str, inputformat="csv", isinputpath=False, config={"colnames": "[['subject', 'predicate', 'object']]"})
        ```

    ??? example "Example 4: create a RDF dataset in memory from a file"

        A `Connection` instance is returned.

        Here is the `test.csv` file:

        ```file
        subject,predicate,object
        <http://example.com/drewp>,<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>,<http://xmlns.com/foaf/0.1/Person>
        <http://example.com/drewp>,<http://example.com/says>,"Hello World"
        ```

        Code:
        ```
        import geist

        # Create a Connection instance
        connection = geist.Connection(datastore='rdflib', dataset=':memory:')
        connection.create(inputfile="test.csv", inputformat="csv", isinputpath=True, config={"colnames": "[['subject', 'predicate', 'object']]"})
        ```

??? info "datastore: clingo"

    |Key            |Type    |Description                                | Default   |
    |-------------- |------- |------------------------------------------ |---------- |
    |predicate      |string  |`'isfirstcol'` for using the first column as the predicate name; strings other than `'isfirstcol'` are used as the predicate name directly |`'isfirstcol'` |
    |programname    |string  |Name of the program                        |`'base'`   |

    ??? example "Example 1: create a `test` ASP dataset from a string"

        The `.geistdata/clingo/test.pkl` file is created and a `Connection` instance is returned.

        ```
        import geist

        lp_str = """
        friends(a, b).
        friends(a, c).
        """

        # Create a Connection instance
        connection = geist.Connection(datastore='clingo', dataset='test')
        connection.create(inputfile=lp_str, inputformat="lp", isinputpath=False)
        ```

    ??? example "Example 2: create a `test` ASP dataset from a file"

        The `.geistdata/clingo/test.pkl` file is created and a `Connection` instance is returned.

        Here is the `friends.lp` file:

        ```file
        friends(a, b).
        friends(a, c).
        ```

        Code:
        ```
        import geist

        # Create a Connection instance
        connection = geist.Connection(datastore='clingo', dataset='test')
        connection.create(inputfile="friends.lp", inputformat="lp", isinputpath=True)
        ```

    ??? example "Example 3: create an ASP dataset in memory from a string"

        A `Connection` instance is returned.

        ```
        import geist

        lp_str = """
        friends(a, b).
        friends(a, c).
        """

        # Create a Connection instance
        connection = geist.Connection(datastore='clingo', dataset=':memory:')
        connection.create(inputfile=lp_str, inputformat="lp", isinputpath=False)
        ```
