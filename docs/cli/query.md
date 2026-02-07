*query* command can perform a query on a dataset.

There are three subcommands for *query*:
```
Usage: geist query [OPTIONS] COMMAND [ARGS]...

  Perform a query on a dataset

Options:
  --help  Show this message and exit.

Commands:
  clingo  Perform an ASP query on a dataset
  duckdb  Perform a SQL query on a dataset
  rdflib  Perform a SPARQL query on a dataset
```

??? info "geist query clingo [OPTIONS]"

    ```
    Usage: geist query clingo [OPTIONS]

    Perform an ASP query on a dataset

    Options:
    -d, --dataset TEXT              Name of ASP dataset to be queried (default
                                    "kb")
    -ifile, --inputfile FILENAME    Specify either the path of the file
                                    containing the ASP query to execute or
                                    provide the ASP query itself via stdin
                                    [required]
    -oroot, --outputroot TEXT       Path of the directory to store the query
                                    results (default: current directory). If the
                                    given path (i.e., --outputfile) is None or a
                                    relative path, it will be ignored.
    -ofile, --outputfile TEXT       Path of the file to store the query results
                                    (default: None). This file can be reused to
                                    create a dataset by setting
                                    inputformat=json.
    -rformat, --returnformat [lp|df|dict]
                                    Format of the returned data in memory
                                    (default lp)
    -pred, --predicate TEXT         Name of the predicate to be queried
    -prog, --programname TEXT       Name of the program
    --help                          Show this message and exit.
    ```

    ??? example "Example 1: query the `test` ASP dataset from stdin"

        ```
        geist query clingo --dataset test << __END_QUERY__

        friends(X, Z) :- friends(X, Y), friends(Y, Z), X < Z.
        friends(Y, Z) :- friends(X, Y), friends(X, Z), Y < Z.

        __END_QUERY__
        ```

    ??? example "Example 2: query the `test` ASP dataset from a query file"

        ```
        geist query clingo --dataset test --inputfile query
        ```

        Here is the query file's content:
        ```
        friends(X, Z) :- friends(X, Y), friends(Y, Z), X < Z.
        friends(Y, Z) :- friends(X, Y), friends(X, Z), Y < Z.
        ```

??? info "geist query duckdb [OPTIONS]"

    ```
    Usage: geist query duckdb [OPTIONS]

    Perform a SQL query on a dataset

    Options:
    -d, --dataset TEXT            Name of RDF dataset to be queried (default
                                    "kb")
    -ifile, --inputfile FILENAME  Specify either the path of the file containing
                                    the SQL query to execute or provide the SQL
                                    query itself via stdin  [required]
    -oroot, --outputroot TEXT     Path of the directory to store the query
                                    results (default: current directory). If the
                                    given path (i.e., --outputfile) is None or a
                                    relative path, it will be ignored.
    -ofile, --outputfile TEXT     Path of the file to store the query results
                                    (default: None)
    --help                        Show this message and exit.
    ```

    ??? example "Example 1: all rows of the `df` table in `test` dataset from stdin"

        ```
        geist query duckdb --dataset test << __END_QUERY__

        SELECT * FROM df

        __END_QUERY__
        ```
    
    ??? example "Example 2: all rows of the `test` dataset from a query file"

        ```
        geist query duckdb --dataset test --inputfile query_file
        ```

        Here is the query_file's content:
        ```
        SELECT * FROM df
        ```


??? info "geist query rdflib [OPTIONS]"

    ```
    Usage: geist query rdflib [OPTIONS]

    Perform a SPARQL query on a dataset

    Options:
    -d, --dataset TEXT            Name of RDF dataset to be queried (default
                                    "kb")
    -ifile, --inputfile FILENAME  Specify either the path of the file containing
                                    the SPARQL query to execute or provide the
                                    SPARQL query itself via stdin  [required]
    -oroot, --outputroot TEXT     Path of the directory to store the query
                                    results (default: current directory). If the
                                    given path (i.e., --outputfile) is None or a
                                    relative path, it will be ignored.
    -ofile, --outputfile TEXT     Path of the file to store the query results
                                    (default: None)
    --help                        Show this message and exit.
    ```

    ??? example "Example 1: all triples of the `test` dataset from stdin"

        ```
        geist query rdflib --dataset test << __END_QUERY__

        SELECT ?s ?p ?o
        WHERE {
            ?s ?p ?o
        }
        ORDER BY ?s ?p ?o

        __END_QUERY__
        ```
    
    ??? example "Example 2: all triples of the `test` dataset from a query file"

        ```
        geist query rdflib --dataset test --inputfile query_file
        ```

        Here is the query_file's content:
        ```
        SELECT ?s ?p ?o
        WHERE {
            ?s ?p ?o
        }
        ORDER BY ?s ?p ?o
        ```
    