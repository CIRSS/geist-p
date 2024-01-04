*graph* command can visualize an RDF dataset.

=== "CLI"

    Here are options of the *graph* command:
    ```
    Usage: geist graph [OPTIONS]

    Visualize a dataset

    Options:
    -d, --dataset TEXT              Name of RDF dataset to be visualized
                                    (default "kb")
    -r, --rankdir [TB|BT|LR|RL]     Direction of the graph (default TB): TB or
                                    BT or LR or RL
    -m, --mappings TEXT             File of the mappings to shorten text (str):
                                    path of a JSON file, where the key is the
                                    original text and the value is the shorter
                                    text.
    -oroot, --outputroot TEXT       Path of the directory to store the graph
                                    (default: current directory). If the given
                                    path (i.e., --outputfile) is a relative
                                    path, it will be ignored.
    -ofile, --outputfile TEXT       Path of the file without extension to store
                                    the graph (default: res)
    -oformat, --outputformat [none|svg|png|gv]
                                    Format of the graph (default: none): none or
                                    svg or png or gv
    --help                          Show this message and exit.
    ```

    ??? example "Example: visualize the `test` dataset"

        ```
        geist graph --dataset test --outputformat svg 
        ```

=== "Geist Template"

    Check the [graph](report/tags/tag-graph.md) tag.
