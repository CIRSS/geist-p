The `map` replaces the original string (JSON string) on selected columns (if provides) with the shorter ones based on the given mappings. By default, the given string is a file path. However, it can be updated by setting the `isfilepath` field to False. A Pandas DataFrame will be returned. Here are parameters of the `map` tag:

|Name           | Description |
|---------------|-------------|
|`isfilepath`   |A bool value to denote if the given data is a file path or not (by default: `True`, which denotes the given data is a file path) |
|`mappings`     |File of the mappings to shorten text (str): path of a JSON file, where the key is the original text and the value is the shorter text. |
|`on`           |A column or a list of selected columns. All columns will be selected by default (`None`) |

??? info "data.json"
    ```
    {
        "v1": {"0":"test_a1","1":"test_b1","2":"test_c1"}, 
        "v2": {"0":"test_a2","1":"test_b2","2":"test_c2"},
        "v3": {"0":"test_a3","1":"test_b3","3":"test_c3"}
    }
    ```

??? info "mapping.json"
    ```
    {"test_": ""}
    ```

??? example "Example 1: replace all columns"

    ```
    {%- map mappings="mappings.json" as res %} data.json {% endmap %}
    {{ res }}
    ```

    Expected output:
    ```
    v1,v2,v3
    a1,a2,a3
    b1,b2,b3
    c1,c2,c3
    ```

??? example "Example 2: replace selected columns"

    ```
    {% map mappings="mappings.json", on=["v1","v2"] as res %} data.json {% endmap %}
    {{ res }}
    ```

    Expected output:
    ```
    v1,v2,v3
    a1,a2,test_a3
    b1,b2,test_b3
    c1,c2,test_c3
    ```

    If only "v1" column need to be replaced, you can replace `on=["v1","v2"]` with `on="v1"`.
    