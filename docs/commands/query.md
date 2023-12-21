*query* command can perform a SPARQL query on a dataset.

=== "CLI"

    Here are options of the *query* command:
    ```
    Usage: geist query [OPTIONS]

    Perform a SPARQL query on a dataset

    Options:
    -d, --dataset TEXT         Name of RDF dataset to be queried (default "kb")
    --file FILENAME            Path of the file containing the SPARQL query to
                                execute  [required]
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
        geist query << __END_QUERY__

        SELECT ?s ?p ?o
        WHERE {
            ?s ?p ?o
        }
        ORDER BY ?s ?p ?o

        __END_QUERY__
        ```
    
    ??? example "Example 2: all triples of the `test` dataset from a query file"

        ```
        geist query --file query_file
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
    