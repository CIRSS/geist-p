*report* command can expand a report (Geist template) using a dataset.

# What is a Geist template?

A Geist template is a text file without a specific extension requirement although adding a `.geist` extension is recommended. It is an extension of a [Jinja template](https://jinja.palletsprojects.com/en/3.1.x/templates/), therefore it follows the default Jinja delimiters:

- `{% ... %}` for Statements
- `{{ ... }}` for Expressions to print to the template output
- `{# ... #}` for Comments not included in the template output

# Tags
Tags are used within the statements, i.e., `{% ... %}`. Besides the Jinja predefined tags (e.g., `for`), Geist supports more tags.

## tag: create

Check [create](create/#__tabbed_1_2)

## tag: load

## tag: query

## tag: destroy

## tag: graph

## tag: graph2

## tag: map

## tag: use

## tag: html

## tag: img

## tag: table

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

        {% create inputformat="nt", isfilepath=False %}
            <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
            <http://example.com/drewp> <http://example.com/says> "Hello World" .
        {% endcreate %}

        {% query isfilepath=False as res %}
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o
            }
            ORDER BY ?s ?p ?o
        {% endquery %}
        {% set all_triples = res | json2df %}

        {% for _, row in all_triples.iterrows() %}
            Subject: {{ row["s"] }}, Predicate: {{ row["p"] }}, Object: {{ row["o"] }}.
        {% endfor %}

        {% destroy %}

        END_TEMPLATE
        ```
    
    ??? example "Example 2: expand a report from file"

        ```
        geist report --file report.geist
        ```

        Here is the report.geist file:
        ```
        {% create inputformat="nt", isfilepath=False %}
            <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
            <http://example.com/drewp> <http://example.com/says> "Hello World" .
        {% endcreate %}

        {% query isfilepath=False as res %}
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o
            }
            ORDER BY ?s ?p ?o
        {% endquery %}
        {% set all_triples = res | json2df %}

        {% for _, row in all_triples.iterrows() %}
            Subject: {{ row["s"] }}, Predicate: {{ row["p"] }}, Object: {{ row["o"] }}.
        {% endfor %}

        {% destroy %}
        ```
