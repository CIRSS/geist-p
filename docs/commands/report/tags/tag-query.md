The `query` tag imports data into a dataset. Here are parameters of the `query` tag:

| Name          | Description                                                    |
|---------------|----------------------------------------------------------------|
|`dataset`      | Name of RDF dataset to be removed (default "kb")               |
|`isfilepath`   | A bool value to denote if the given data is a file path or not (default True, which denotes the given data is a file path) |

??? example "Example 1: the given string is not a file path"

    ```
    {% query dataset="test", isfilepath=False %}
        SELECT ?s ?p ?o
        WHERE {
            ?s ?p ?o
        }
        ORDER BY ?s ?p ?o
    {% endquery %}
    ```

??? example "Example 2: the given string is a file path"

    ```
    {% query dataset="test", isfilepath=True %} query_file {% endquery %}
    ```
    Here is the query_file's content:
    ```
    SELECT ?s ?p ?o
    WHERE {
        ?s ?p ?o
    }
    ORDER BY ?s ?p ?o
    ```
