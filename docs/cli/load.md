*load* command can import data into an existing dataset.

There are two subcommands for *load*:
```
Usage: geist load [OPTIONS] COMMAND [ARGS]...

Import data into a dataset

Options:
  --help  Show this message and exit.

Commands:
  duckdb  Import data into a SQL dataset
  rdflib  Import data into a RDF dataset
```

??? info "geist load duckdb [OPTIONS]"

    ```
    Usage: geist load duckdb [OPTIONS]

    Import data into a SQL dataset

    Options:
    -d, --dataset TEXT              Name of SQL dataset to load a file (default
                                    "kb")
    -ifile, --inputfile FILENAME    Path of the file to be loaded as a table
                                    [required]
    -iformat, --inputformat [csv|json]
                                    Format of the file to be loaded as a table
                                    (default csv)
    -t, --table TEXT                Name of the table to be created  [required]
    --help                          Show this message and exit.
    ```

    ??? example "Example: load a file into the `test` dataset"

        ```
        geist load duckdb --dataset test --inputfile test_add.csv --inputformat csv --table df
        ```

??? info "geist load rdflib [OPTIONS]"

    Here are options of the *load* command:
    ```
    Usage: geist load rdflib [OPTIONS]

    Import data into a RDF dataset

    Options:
    -d, --dataset TEXT              Name of RDF dataset to load a file (default
                                    "kb")
    -ifile, --inputfile FILENAME    Path of the file to be loaded as triples
                                    [required]
    -iformat, --inputformat [xml|n3|turtle|nt|pretty-xml|trix|trig|nquads|json-ld|hext|csv]
                                    Format of the file to be loaded as triples
                                    (default json-ld)
    --colnames TEXT                 Column names of triples with the format of
                                    [[subject1, predicate1, object1], [subject2,
                                    predicate2, object2], ...] when the input
                                    format is csv
    --help                          Show this message and exit.
    ```

    ??? example "Example: load a file into the `test` dataset"

        ```
        geist load rdflib --dataset test --inputfile test_add.jsonld
        ```
