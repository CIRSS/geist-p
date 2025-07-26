The `img` tag renders the Mermaid string as an image and embeds it into HTML. Here are parameters of the `img` tag:

| Name      | Description                                                    |
|-----------|----------------------------------------------------------------|
|`src`      | Path of the rendered image to be saved. Various extensions are supported. Note: `mermaid`, `mmd`, `dot` or `gv` will show code directly. (Known issue: the image is rendered by mermaid.ink for now. Due to the limitation of URL length, you may get the `"414 Request-URI Too Large" errors` message. We recommend select `mermaid` or `mmd` instead.|
|...        | Attributes of the [HTML <img>](ttps://www.w3schools.com/tags/tag_img.asp) or the [HTML <code>](https://www.w3schools.com/tags/tag_code.asp) tag |


??? example "Example 1: render as svg"

    ```
    {% img src="test.svg", width="50%" %}
        graph TB
            node1 --> node2
    {% endimg %}
    ```

    A file named `test.svg` will be created and the Geist template will be updated as:
    ```
    <img src="test.svg" width="50%" >
    ```

??? example "Example 2: using the mermaid string directly"

    ```
    {% img src="test.mermaid" %}
        graph TB
            node1 --> node2
    {% endimg %}
    ```

    A file named `test.mermaid` will be created and the Geist template will be updated as:
    ```
    <pre class="mermaid">
        graph TB
            node1 --> node2
    </pre>
    <script type="module">
        import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    ```

??? example "Example 3: show gv directly"

    ```
    {% img src="test.gv" %}digraph test_graph { node1 -> node2 }{% endimg %}
    ```

    A file named `test.gv` will be created and the Geist template will be updated as:
    ```
    <pre><code>digraph test_graph { node1 -> node2 }</code></pre>
    ```
