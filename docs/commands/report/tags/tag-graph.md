The `graph` tag visualizes a dataset. Here are parameters of the `graph` tag:

| Name          | Description                                                    |
|---------------|----------------------------------------------------------------|
|`dataset`      | Name of RDF dataset to be visualized (default "kb")            |
|`rankdir`      | Direction of the graph (default TB): TB or BT or LR or RL      |
|`mappings`     | File of the mappings to shorten text (str): path of a JSON file, where the key is the original text and the value is the shorter text. |
|`on`           | Column(s) to be mapped (default None, which means all columns will be mapped) |

??? example "Example: visualize the `test` dataset"

    ```
    {% graph dataset="test" %}
    ```
