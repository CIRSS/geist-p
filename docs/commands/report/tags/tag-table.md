The `table` tag embed query results to HTML as a table. Here are parameters of the `table` tag:

| Name      | Description                                                    |
|-----------|----------------------------------------------------------------|
|`mappings` |File of the mappings to shorten text (str): path of a JSON file, where the key is the original text and the value is the shorter text. |
|`on`       |A column or a list of selected columns. All columns will be selected by default (None) |


??? example "Example: embed query results as a table"

    ```
    {% table %}
        {%- query isfilepath=False as query_results %}
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o
            }
            ORDER BY ?s ?p ?o
        {% endquery %}
        {{ query_results }}
    {% endtable %}
    ```
