The `map` replaces the original text in a Pandas data frame on selected columns (if provides) with the shorter ones based on the given mappings. By default, the given string is a file path. However, it can be updated by setting the `isfilepath` field to False. Here are parameters of the `map` tag:

|Name           | Description |
|---------------|-------------|
|`isfilepath`   |A bool value to denote if the given data is a file path or not (by default: True, which denotes the given data is a file path) |
|`mappings`     |File of the mappings to shorten text (str): path of a JSON file, where the key is the original text and the value is the shorter text. |
|`on`           |A column or a list of selected columns. All columns will be selected by default (None) |

??? example "data.csv"
    ```
    v1,v2,v3
    test_a1,test_a2,test_a3
    test_b1,test_b2,test_b3
    ```

??? example "mapping.json"
    ```
    {"test_": ""}
    ```

??? example "Example 1: replace all columns"

    ```
    {% map mappings="mappings.json" %} data.csv {% endmap %}
    ```

    Expected output:
    ```
    v1,v2,v3
    a1,a2,a3
    b1,b2,b3
    ```

??? example "Example 2: replace selected columns"

    ```
    {% map mappings="mappings.json" on=["v1","v2"] %} data.csv {% endmap %}
    ```

    Expected output:
    ```
    v1,v2,v3
    test_a1,test_a2,a3
    test_b1,test_b2,b3
    ```

    If only "v1" column need to be replaced, you can replace `on=["v1","v2"]` with `on="v1"`.
    