# Report Command Introduction

*report* command can expand a report (Geist template) using a dataset.

## What is a Geist template?

A Geist template is a text file without a specific extension requirement although adding a `.geist` extension is recommended. It is an extension of a [Jinja template](https://jinja.palletsprojects.com/en/3.1.x/templates/), therefore it follows the default Jinja delimiters:

- `{% ... %}` for Statements
- `{{ ... }}` for Expressions to print to the template output
- `{# ... #}` for Comments not included in the template output

## How to write a Geist template?

A Geist template relies on tags and filters.

### Tags

Tags are used within the statements, i.e., `{% ... %}`. There are two types of tags, `StandaloneTag` and `ContainerTag`. While the `StandaloneTag` does not require a closing tag, the `ContainerTag` does. Besides the Jinja predefined tags (e.g., `for`), Geist supports the following tags:

`StandaloneTag`:

- [destroy](tags/tag-destroy.md)
- [graph](tags/tag-graph.md)
- [graph2](tags/tag-graph2.md)
- [use](tags/tag-use.md)

`ContainerTag`:

- [create](tags/tag-create.md)
- [load](tags/tag-load.md)
- [query](tags/tag-query.md)
- [component](tags/tag-component.md)
- [map](tags/tag-map.md)
- [html](tags/tag-html.md)
- [img](tags/tag-img.md)
- [table](tags/tag-table.md)

Custom tags can be defined through files with the [use](tags/tag-use.md) tag.

### Filters

Filters are used to modify variables. Each filter can only take one variable as input. Multiple filters can be applied to a single variable in sequence. For example, `{{ var|filter1|filter2|filter3 }}` denotes the variable `var` will be processed through `filter1` first, then `filter2`, and `filter3` at the end.

Geist supports the following filters:

- **json2df**: convert a JSON string to a Pandas data frame
- **json2dict**: convert a JSON string to a dictionary
- **df2json**: convert a Pandas data frame to a JSON string
- **df2htmltable**: convert a Pandas data frame to an HTML table
- **escape_quotes**: escape both double and single quotation marks
- **process_str_for_html**: preprocess a string to be displayed within an HTML document, e.g., replace `<` with `&lt`

## How to execute (expand) a Geist template?

=== "CLI"

    Here are options of the *report* command:
    ```
    Usage: geist report [OPTIONS]

    Expand a report using a dataset

    Options:
    -f, --file FILENAME            Path of the file containing the report
                                    template to expand  [required]
    -oroot, --outputroot TEXT      Path of the directory to store the expanded
                                    report (default: current directory)
    -so, --suppressoutput BOOLEAN  Suppress output or not (default: False)
    --help                         Show this message and exit.
    ```

    ??? example "Example 1: expand a report from stdin"

        ```
        geist report << END_TEMPLATE

        {% create "test", datastore="rdflib", inputformat="nt", isfilepath=False %}
            <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
            <http://example.com/drewp> <http://example.com/says> "Hello World" .
        {% endcreate %}

        {% query "test", datastore="rdflib", isfilepath=False as all_triples %}
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o
            }
            ORDER BY ?s ?p ?o
        {% endquery %}

        {% for _, row in all_triples.iterrows() %}
            Subject: {{ row["s"] }}, Predicate: {{ row["p"] }}, Object: {{ row["o"] }}.
        {% endfor %}

        {% destroy "test", datastore="rdflib" %}

        END_TEMPLATE
        ```
    
    ??? example "Example 2: expand a report from file"

        ```
        geist report --file report.geist
        ```

        Here is the report.geist file:
        ```
        {% create "test", datastore="rdflib", inputformat="nt", isfilepath=False %}
            <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
            <http://example.com/drewp> <http://example.com/says> "Hello World" .
        {% endcreate %}

        {% query "test", datastore="rdflib", isfilepath=False as all_triples %}
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o
            }
            ORDER BY ?s ?p ?o
        {% endquery %}

        {% for _, row in all_triples.iterrows() %}
            Subject: {{ row["s"] }}, Predicate: {{ row["p"] }}, Object: {{ row["o"] }}.
        {% endfor %}

        {% destroy "test", datastore="rdflib" %}
        ```


