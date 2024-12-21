The `load` tag imports data into a dataset. Here are parameters of the `load` tag:

| Name          | Description                                                    |
|---------------|----------------------------------------------------------------|
|`dataset`      | Name of RDF dataset to be removed (default `kb`)               |
|`datastore`    | Data backend. `duckdb` and `rdflib` are available for now. (by default, `rdflib`) |
|`inputformat`  | Format of the file to be loaded as triples (default `json-ld`)   |
|`isfilepath`   | A bool value to denote if the given data is a file path or not (default `True`, which denotes the given data is a file path) |
|`table`        | Table name to be loaded. Available for `duckdb` data backend only. |
|`colnames`     | Column names of triples with the format of `[[subject1, predicate1, object1], [subject2, predicate2, object2], ...]` when the input format is csv. Available for `rdflib` data backend only. |

??? example "Example: load a file into the `test` dataset"

    ```
    {% load "test", datastore="rdflib" %} test_add.jsonld {% endload %}
    ```
