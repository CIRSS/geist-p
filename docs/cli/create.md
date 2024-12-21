The *create* command has two subcommands, both of which create a new dataset on disk. The dataset name `:memory:` is a reserved value for datasets that exist only in memory and is not allowed in the CLI.

```
Usage: geist create [OPTIONS] COMMAND [ARGS]...

Create a new dataset

Options:
--help  Show this message and exit.

Commands:
duckdb  Create a new SQL dataset using DuckDB
rdflib  Create a new RDF dataset using RDFLib
```

??? info "geist create duckdb [OPTIONS]"

    ```
    Usage: geist create duckdb [OPTIONS]

    Create a new SQL dataset using DuckDB

    Options:
    -d, --dataset TEXT              Name of SQL dataset to create (default "kb")
    -ifile, --inputfile FILENAME    Path of the file to be loaded as a Pandas
                                    DataFrame  [required]
    -iformat, --inputformat [csv|json]
                                    Format of the file to be loaded as a Pandas
                                    DataFrame (default csv)
    -t, --table TEXT                Name of the table to be created (default
                                    "df")
    --help                          Show this message and exit.
    ```

    ??? example "Example 1: create a `test` SQL dataset from stdin"

        ```
        geist create duckdb --dataset test --inputformat csv --table df << __END_INPUT__
        v1,v2,v3
        1,2,3
        4,5,6
        7,8,9
        __END_INPUT__
        ```
    
    ??? example "Example 2: create a `test` dataset from a file"
        
        Here is the `test.csv` file:

        ```file
        v1,v2,v3
        1,2,3
        4,5,6
        7,8,9
        ```

        Code:
        ```
        geist create duckdb --dataset test --inputfile test.csv --inputformat csv --table df
        ```

??? info "geist create rdflib [OPTIONS]"

    ```
    Usage: geist create rdflib [OPTIONS]

    Create a new RDF dataset

    Options:
    -d, --dataset TEXT              Name of RDF dataset to create (default "kb")
    -ifile, --inputfile FILENAME    Path of the file to be loaded as triples
                                    [required]
    -iformat, --inputformat [xml|n3|turtle|nt|pretty-xml|trix|trig|nquads|json-ld|hext|csv]
                                    Format of the file to be loaded as triples
                                    (default json-ld)
    --colnames TEXT                 Column names of triples with the format of
                                    [[subject1, predicate1, object1], [subject2,
                                    predicate2, object2], ...] when the input
                                    format is csv
    --infer [none|rdfs|owl|rdfs_owl]
                                    Inference to perform on update [none, rdfs,
                                    owl, rdfs_owl] (default "none")
    --help                          Show this message and exit.
    ```

    ??? example "Example 1: create a `test` RDF dataset from stdin"

        ```
        geist create rdflib --dataset test --inputformat nt --infer none << __END_INPUT__

        <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
        <http://example.com/drewp> <http://example.com/says> "Hello World" .

        __END_INPUT__
        ```
    
    ??? example "Example 2: create a `test` dataset from a file"

        Here is the `test.nt` file:

        ```file
        <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
        <http://example.com/drewp> <http://example.com/says> "Hello World" .

        ```
        Code:
        ```
        geist create rdflib --dataset test --inputfile test.nt --inputformat nt --infer none
        ```
