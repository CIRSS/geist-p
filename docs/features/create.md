**create** feature can create a new dataset on disk or in memory. For the disk option, a `.duckdb` or a `.pkl` file will be created under the `.geistdata/duckdb` or the `.geistdata/rdflib` folder with the same name of this dataset. For the memory option, a `DuckDBPyConnection` object or a `GeistGraph` object (a dictionary with `rdf_graph` and `infer` keys) will be returned.

You can write a [Geist template](geist-templates/introduction.md) with the [create](geist-templates/tags/tag-create.md) tag. You can also use **CLI** or **Python API** step by step as follows:

=== "CLI: create command"

    --8<-- "cli/create.md"

=== "Python API: create function"

    --8<-- "python-api/create.md"

=== "Python API: create method of the Connection Class"

    --8<-- "python-api/connect/create.md"
    

