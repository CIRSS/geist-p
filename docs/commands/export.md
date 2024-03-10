*export* command can export a dataset.

There are two subcommands for *export*:
```
Usage: geist export [OPTIONS] COMMAND [ARGS]...

  Export a dataset

Options:
  --help  Show this message and exit.

Commands:
  duckdb  Export a SQL dataset
  rdflib  Export an RDF dataset
```

=== "CLI: duckdb"

    ```
    Usage: geist export duckdb [OPTIONS]

    Export a SQL dataset

    Options:
    -d, --dataset TEXT              Name of SQL dataset to be exported (default
                                    "kb")
    -oroot, --outputroot TEXT       Path of the directory to store the exported
                                    table (default: current directory). If the
                                    given path (i.e., --outputfile) is None or a
                                    relative path, it will be ignored.
    -ofile, --outputfile TEXT       Path of the file to store the exported table
                                    (default: None)
    -oformat, --outputformat [csv|json]
                                    Format of the exported table (default csv)
    -t, --table TEXT                Name of the table to be exported (default
                                    "df")
    --help                          Show this message and exit.
    ```

    ??? example "Example: export the `df` table in `test` dataset"

        By default, the exported table will be printed in terminal:
        ```
        geist export duckdb --dataset test --table df
        ```


=== "CLI: rdflib"

    ```
    Usage: geist export rdflib [OPTIONS]

    Export an RDF dataset

    Options:
    -d, --dataset TEXT              Name of RDF dataset to be exported (default
                                    "kb")
    -oroot, --outputroot TEXT       Path of the directory to store these
                                    exported triples (default: current
                                    directory). If the given path (i.e.,
                                    --outputfile) is None or a relative path, it
                                    will be ignored.
    -ofile, --outputfile TEXT       Path of the file to store these exported
                                    triples (default: None)
    -oformat, --outputformat [json-ld|n3|nquads|nt|hext|pretty-xml|trig|trix|turtle|longturtle|xml]
                                    Format of the exported triples (default nt)
    --help                          Show this message and exit.
    ```

    ??? example "Example: export the `test` dataset"

        By default, the exported triples will be printed in terminal:
        ```
        geist export rdflib --dataset test
        ```
