*query* command can perform a query on a dataset.

There are two subcommands for *query*:
```
Usage: geist query [OPTIONS] COMMAND [ARGS]...

  Perform a query on a dataset

Options:
  --help  Show this message and exit.

Commands:
  duckdb  Perform a SQL query on a dataset
  rdflib  Perform a SPARQL query on a dataset
```

=== "CLI: duckdb"

    ```
    Usage: geist query duckdb [OPTIONS]

    Perform a SQL query on a dataset

    Options:
    -d, --dataset TEXT         Name of RDF dataset to be queried (default "kb")
    --file FILENAME            Specify either the path of the file containing
                                the SQL query to execute or provide the SQL query
                                itself via stdin  [required]
    -oroot, --outputroot TEXT  Path of the directory to store the query results
                                (default: current directory). If the given path
                                (i.e., --outputfile) is None or a relative path,
                                it will be ignored.
    -ofile, --outputfile TEXT  Path of the file to store the query results
                                (default: None)
    --help                     Show this message and exit.
    ```

    ??? example "Example 1: all rows of the `df` table in `test` dataset from stdin"

        ```
        geist query duckdb --dataset test << __END_QUERY__

        SELECT * FROM df

        __END_QUERY__
        ```
    
    ??? example "Example 2: all rows of the `test` dataset from a query file"

        ```
        geist query duckdb --dataset test --file query_file
        ```

        Here is the query_file's content:
        ```
        SELECT * FROM df
        ```


=== "CLI: rdflib"

    ```
    Usage: geist query rdflib [OPTIONS]

    Perform a SPARQL query on a dataset

    Options:
    -d, --dataset TEXT         Name of RDF dataset to be queried (default "kb")
    --file FILENAME            Specify either the path of the file containing
                                the SPARQL query to execute or provide the SPARQL
                                query itself via stdin  [required]
    -oroot, --outputroot TEXT  Path of the directory to store the query results
                                (default: current directory). If the given path
                                (i.e., --outputfile) is None or a relative path,
                                it will be ignored.
    -ofile, --outputfile TEXT  Path of the file to store the query results
                                (default: None)
    --help                     Show this message and exit.
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
        geist query rdflib --dataset test --file query_file
        ```

        Here is the query_file's content:
        ```
        SELECT ?s ?p ?o
        WHERE {
            ?s ?p ?o
        }
        ORDER BY ?s ?p ?o
        ```

=== "Geist Template"

    Check the [query](report/tags/tag-query.md) tag.
    