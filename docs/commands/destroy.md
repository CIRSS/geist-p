*destroy* command can delete a dataset. The `.duckdb` or the `.pkl` file of the corresponding dataset will be discarded.

There are two subcommands for *destroy*:
```
Usage: geist destroy [OPTIONS] COMMAND [ARGS]...

  Delete a dataset

Options:
  --help  Show this message and exit.

Commands:
  duckdb  Delete a SQL dataset
  rdflib  Delete an RDF dataset
```

=== "CLI: duckdb"

    ```
    Usage: geist destroy duckdb [OPTIONS]

    Delete a SQL dataset

    Options:
    -d, --dataset TEXT  Name of SQL dataset to be removed (default "kb")
    -q, --quiet         Suppress error messages if the provided dataset does not
                        exist
    --help              Show this message and exit.
    ```

    ??? example "Example: delete the `test` dataset"

        ```
        geist destroy duckdb --dataset test
        ```

        The `.geistdata/duckdb/test.duckdb` file will be removed after this operation. By default, you will get an error message if the provided dataset (in this case, it is the `test` dataset) does not exist. To suppress this error message, you can add `--quiet`:

        ```
        geist destroy duckdb --dataset test --quiet
        ```

=== "CLI: rdflib"

    ```
    Usage: geist destroy rdflib [OPTIONS]

    Delete an RDF dataset

    Options:
    -d, --dataset TEXT  Name of RDF dataset to be removed (default "kb")
    -q, --quiet         Suppress error messages if the provided dataset does not
                        exist
    --help              Show this message and exit.
    ```

    ??? example "Example: delete the `test` dataset"

        ```
        geist destroy rdflib --dataset test
        ```

        The `.geistdata/rdflib/test.pkl` file will be removed after this operation. By default, you will get an error message if the provided dataset (in this case, it is the `test` dataset) does not exist. To suppress this error message, you can add `--quiet`:

        ```
        geist destroy rdflib --dataset test --quiet
        ```

=== "Geist Template"
    
    Check the [destroy](report/tags/tag-destroy.md) tag.
