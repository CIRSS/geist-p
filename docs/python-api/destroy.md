**destroy** function can delete a dataset.

Parameters description for *destroy()*:

|Name           |Type    |Description                    | Default    |
|-------------- |------- |------------------------------ |----------- |
|datastore      |string  |A backend datastore, i.e., `'clingo'`, `'duckdb'`, or `'rdflib'` |REQUIRED |
|dataset        |string  |Name of the dataset to be removed |REQUIRED |
|quiet          |bool    |`True` to suppress error messages if the provided dataset does not exist |`False` |

??? example "Example: delete the `test` dataset"

    ```
    import geist
    geist.destroy(datastore='rdflib', dataset='test')
    ```

    The `.geistdata/rdflib/test.pkl` file will be removed after this operation. By default, you will get an error message if the provided dataset (in this case, it is the `test` dataset) does not exist. To suppress this error message, you can set `quiet=True`:

    ```
    import geist
    geist.destroy(datastore='rdflib', dataset='test', quiet=True)
    ```
