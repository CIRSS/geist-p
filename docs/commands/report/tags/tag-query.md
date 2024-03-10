The `query` tag performs a query on a dataset and returns a Pandas DataFrame. Here are parameters of the `query` tag:

| Name          | Description                                                    |
|---------------|----------------------------------------------------------------|
|`dataset`      | Name of a dataset to query (default "kb")               |
|`datastore`    | Data backend. `duckdb` and `rdflib` are available for now. (by default, "rdflib") |
|`isfilepath`   | A bool value to denote if the given data is a file path or not (default True, which denotes the given data is a file path) |

??? example "Example 1: the given string is not a file path"

    ```
    {% query "test", datastore="rdflib", isfilepath=False %}
        SELECT ?s ?p ?o
        WHERE {
            ?s ?p ?o
        }
        ORDER BY ?s ?p ?o
    {% endquery %}
    ```

??? example "Example 2: the given string is a file path"

    ```
    {% query "test", datastore="rdflib", isfilepath=True %} query_file {% endquery %}
    ```
    Here is the query_file's content:
    ```
    SELECT ?s ?p ?o
    WHERE {
        ?s ?p ?o
    }
    ORDER BY ?s ?p ?o
    ```
