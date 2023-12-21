*export* command can export an RDF dataset.

=== "CLI"

    Here are options of the *export* command:
    ```
    Usage: geist export [OPTIONS]

        Export an RDF graph

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
        geist export --dataset test
        ```
