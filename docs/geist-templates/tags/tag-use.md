The `use` tag can be used to define custom tags. Here is a parameter of the `use` tag:

| Name          | Description                                |
|---------------|--------------------------------------------|
|`filepath`     | Path of a file to define custom tags       |

Here is the structure of tags to be defined within the file at the path `filepath`:
```
{% template TAG_NAME PARAM1 PARAM2 %}
    CONTENT
{% endtemplate %}
```
You need to update `TAG_NAME`, `PARAM1`, `PARAM2`, and `CONTENT` based on your use case. `TAG_NAME` must be unique, which means you cannot define multiple tags with the same name. You can have any number of parameters, which means `{% template TAG_NAME %}` and `{% template TAG_NAME PARAM1 PARAM2 PARAM3 %}` are also valid. Nested tags are also supported, which means you can put another tag within the `CONTENT` part.

??? example "Example: define `predicate_term` and `format_output` tags"

    1. Write `{% use "templates.geist" %}` at the beginning of a Geist template, where you want to use the custom tags, i.e., `predicate_term` and `format_output` tags.

    2. Define custom tags in file with the path of "templates.geist":

        ```
        {% template predicate_term %}says{% endtemplate %}

        {% template format_output person sent %}
            {{ person }} {% predicate_term %} {{sent}}
        {% endtemplate %}
        ```

    3. Use custom tags in the Geist template as other predefined tags (e.g., `create`)

        ```
        {% use "templates.geist" %}

        {%- create inputformat="nt", isfilepath=False %}
            <http://example.com/test1> <http://example.com/p1> "Hello World".
            <http://example.com/test2> <http://example.com/p2> "What a Nice Day".
        {% endcreate %}

        {%- query "kb1", isfilepath=False as res %}
            SELECT ?s ?o
            WHERE {
                ?s ?p ?o
            }
            ORDER BY ?s ?o
        {% endquery %}
        {% set all_triples = res | json2df %}

        {% for _, row in all_triples.iterrows() %}
            {% format_output row["s"], row["o"] %}.
        {%- endfor %}

        {%- destroy %}
        ```

    4. Expected output:

        ```
        <http://example.com/test1> says Hello World.
        <http://example.com/test2> says What a Nice Day.
        ```
