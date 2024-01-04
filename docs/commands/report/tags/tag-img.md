The `img` tag renders Graphviz code as an image and embeds it into HTML. Here are parameters of the `img` tag:

| Name      | Description                                                    |
|-----------|----------------------------------------------------------------|
|`src`      | Path of the rendered image to be saved. Various extensions are supported. Check [PyGraphviz Docs](https://pygraphviz.github.io/documentation/stable/reference/agraph.html#pygraphviz.AGraph.draw) for the whole list. Note: `dot` or `gv` will show code directly.|
|...        | Attributes of the [HTML <img>](ttps://www.w3schools.com/tags/tag_img.asp) or the [HTML <code>](https://www.w3schools.com/tags/tag_code.asp) tag |


??? example "Example 1: render as svg"

    ```
    {% img src="test.svg" %}digraph test_graph { node1 -> node2 }{% endimg %}
    ```

    A file named `test.svg` will be created and the Geist template will be updated as:
    ```
    <img src="test.svg" width="100%" >
    ```

??? example "Example 2: render as gv"

    ```
    {% img src="test.gv" %}digraph test_graph { node1 -> node2 }{% endimg %}
    ```

    A file named `test.gv` will be created and the Geist template will be updated as:
    ```
    <pre><code>digraph test_graph { node1 -> node2 }</code></pre>
    ```
