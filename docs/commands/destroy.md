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
    
    Check the [destroy](report/tags/tag-destroy.md) tag.
