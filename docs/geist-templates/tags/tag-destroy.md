The `destroy` tag deletes a dataset. Here are parameters of the `destroy` tag:

| Name          | Description                                                    |
|---------------|----------------------------------------------------------------|
|`dataset`      | Name of RDF dataset to be removed (default `kb`)               |
|`datastore`    | Data backend. `clingo`, `duckdb`, and `rdflib` are available. (by default, `rdflib`) |
|`quiet`        | Suppress error messages if the provided dataset does not exist |

??? example "Example: delete the `test` dataset"

    ```
    {% destroy dataset="test" %}
    ```
    OR
    ```
    {% destroy "test" %}
    ```

    The dataset file (e.g., `.geistdata/rdflib/test.pkl`) will be removed after this operation. By default, you will get an error message if the provided dataset (in this case, it is the `test` dataset) does not exist. To suppress this error message, you can add the `quiet` parameter:

    ```
    {% destroy "test", quiet=True %}
    ```
