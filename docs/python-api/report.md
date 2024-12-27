**report** function can expand a report (Geist template) using dataset(s).

Parameters description for *report()*:

|Name           |Type    |Description                | Default   |
|-------------- |------- |-------------------------- |---------- |
|inputfile      |string  |A report to be expanded    |`[required]` |
|isinputpath    |bool    |True if the inputfile is the file path, otherwise the inputfile is the content | `False` |
|outputroot     |string  |Path of the directory to store the expanded report | current directory, i.e., `./` |
|suppressoutput |bool    |True to suppress output    | `True`    |
|args           |dict    |External arguments, e.g., `{"arg1": "value1", "arg2": "value2"}` denotes that `{{ arg1 }}` and `{{ arg2 }}` in the report template will be replaced by `value1` and `value2` respectively | `{}` |

??? example "Example 1: expand a report from a string"

    ```py
    import geist

    report = """

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

    """

    # Return the expanded report as a string variable named expanded_report
    expanded_report = geist.report(inputfile=report)

    ```

??? example "Example 2: expand a report from a file"

    ```py
    import geist
    
    # Return the expanded report as a string variable named expanded_report
    expanded_report = geist.report(inputfile='report.geist', isinputpath=True)
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

??? example "Example 3: expand a report from a file with external arguments"

    ```py
    import geist

    # Return the expanded report as a string variable named expanded_report
    expanded_report = geist.report(
        inputfile='report.geist', 
        isinputpath=True, 
        args={
            "sentence": "Hello World", 
            "feeling": "Happy"
        }
    )
    ```

    Here is the report.geist file:
    ```
    {% create "test", datastore="rdflib", inputformat="nt", isfilepath=False %}
        <http://example.com/drewp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
        <http://example.com/drewp> <http://example.com/says> "{{ sentence }}" .
        <http://example.com/drewp> <http://example.com/feels> "{{ feeling }}" .
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
