*report* command can expand a report (Geist template) using dataset(s).

Here are options of the *report* command:
```
Usage: geist report [OPTIONS]

Expand a report using dataset(s)

Options:
-ifile, --inputfile FILENAME   Path of the file containing the report
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

??? example "Example 2: expand a report from a file"

    ```
    geist report --inputfile report.geist
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
