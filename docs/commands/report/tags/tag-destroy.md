The `destroy` tag deletes a dataset. Here are parameters of the `destroy` tag:

| Name          | Description                                                    |
|---------------|----------------------------------------------------------------|
|`dataset`      | Name of RDF dataset to be removed (default "kb")               |
|`quiet`        | Suppress error messages if the provided dataset does not exist |

??? example "Example: delete the `test` dataset"

    ```
    {% destroy dataset="test" %}
    ```
    OR
    ```
    {% destroy "test" %}
    ```

    The `.geistdata/test.pkl` file will be removed after this operation. By default, you will get an error message if the provided dataset (in this case, it is the `test` dataset) does not exist. To suppress this error message, you can add the `quiet` parameter:

    ```
    {% destroy "test", quiet=True %}
    ```
