*load* command can import data into an existing RDF dataset.

=== "CLI"

    Here are options of the *load* command:
    ```
    Usage: geist load [OPTIONS]

    Import data into an RDF dataset

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
    --help                          Show this message and exit.
    ```

    ??? example "Example: load a file into the `test` dataset"

        ```
        geist load --dataset test --inputfile test_add.jsonld
        ```

=== "Geist Template"
    The `load` tag imports data into a dataset. Please check the *report* command section for Geist template rendering.
    
    Here are parameters of the `load` tag:

    | Name          | Description                                                    |
    |---------------|----------------------------------------------------------------|
    |`dataset`      | Name of RDF dataset to be removed (default "kb")               |
    |`inputformat`  | Format of the file to be loaded as triples (default json-ld)   |
    |`colnames`     | Column names of triples with the format of [[subject1, predicate1, object1], [subject2, predicate2, object2], ...] when the input format is csv |
    |`isfilepath`   | A bool value to denote if the given data is a file path or not (default True, which denotes the given data is a file path) |

    ??? example "Example: load a file into the `test` dataset"

        ```
        {% load dataset="test" %} test_add.jsonld {% endload %}
        ```
