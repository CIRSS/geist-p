*create* command can create a new RDF dataset. A PKL file will be created under the `.geistdata` folder with the same name of this dataset.

=== "CLI"

    Here are options of the *create* command:
    ```
    Usage: geist create [OPTIONS]

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

    ??? example "Example 1: create a `test` dataset from stdin"

        ```
        geist create --dataset test --inputformat nt --infer none << __END_INPUT__

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
        geist create --dataset test --inputfile test.nt --inputformat nt --infer none
        ```

=== "Geist Template"
    
    Check the [create](report/tags/tag-create.md) tag.
