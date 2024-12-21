The `html` tag formats and saves the string as a HTML file. Here is a parameter of the `html` tag:

| Name      | Description                                                    |
|-----------|----------------------------------------------------------------|
|`path`     | Path of the HTML file to be saved. By default, `report.html`   |

??? example "Save the `Hello World!` string as a file"

    ```
    {% html %}Hello World!{% endhtml %}
    ```

    Expected content of the `report.html` file:

    ```
    <!DOCTYPE html>
    <html>
    Hello World!
    </html>
    ```