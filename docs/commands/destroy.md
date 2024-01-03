*destroy* command can delete an RDF dataset. The PKL file of the corresponding dataset will be discarded.

=== "CLI"

    Here are options of the *destroy* command:
    ```
    Usage: geist destroy [OPTIONS]

        Delete an RDF dataset

    Options:
    -d, --dataset TEXT  Name of RDF dataset to be removed (default "kb")
    -q, --quiet         Suppress error messages if the provided dataset does not
                        exist
    --help              Show this message and exit.
    ```

    ??? example "Example: delete the `test` dataset"

        ```
        geist destroy --dataset test
        ```

        The `.geistdata/test.pkl` file will be removed after this operation. By default, you will get an error message if the provided dataset (in this case, it is the `test` dataset) does not exist. To suppress this error message, you can add `--quiet`:

        ```
        geist destroy --dataset test --quiet
        ```

=== "Geist Template"
    The `destroy` tag deletes a dataset. Please check the [*report*](report.md) command section for Geist template rendering.

    Here are parameters of the `destroy` tag:

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
