The `create` tag creates a dataset based on the given string. By default, the given string is a file path. However, it can be updated by setting the `isfilepath` field to False. Here are parameters of the `create` tag:

|Name           | Description |
|---------------|-------------|
|`dataset`      |Name of RDF dataset to create (by default, "kb") |
|`datastore`    |Data backend. `duckdb` and `rdflib` are available for now. (by default, "rdflib") |
|`inputformat`  |Format of the file to be loaded as triples (by default, "json-ld"). It has to be one of {"xml", "n3", "turtle", "nt", "pretty-xml", "trix", "trig", "nquads", "json-ld", "hext", "csv"} |
|`infer`        |Inference to perform on update choosing from {"none", "rdfs", "owl", "rdfs_owl"} (by default, "none"). Please check [OWL-RL](https://owl-rl.readthedocs.io/en/latest/owlrl.html) document for detailed information. |
|`isfilepath`   |A bool value to denote if the given data is a file path or not (by default: True, which denotes the given data is a file path) |
|`table`        |Table name. Available for `duckdb` data backend only. |
|`colnames`     |Column names of triples with the format of [[subject1, predicate1, object1], [subject2, predicate2, object2], ...] when the input format is csv (by default, None). Available for `rdflib` data backend only. |

??? example "Example 1: the given string is not a file path"

    ```
    {% create "test", datastore="rdflib", inputformat="nt", isfilepath=False %}
        <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
        <http://example.com/drewp> <http://example.com/says> "Hello World" .
    {% endcreate %}
    ```

??? example "Example 2: the given string is a file path"

    Here is the `test.nt` file:

    ```file
    <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
    <http://example.com/drewp> <http://example.com/says> "Hello World" .

    ```
    
    Code:
    ```
    {% create "test", datastore="rdflib", inputformat="nt", isfilepath=True %} test.nt {% endcreate %}
    ```
