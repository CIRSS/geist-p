**query** function can perform a query on a dataset.

Parameters description for *query()*:

|Name           |Type    |Description                    | Default    |
|-------------- |------- |------------------------------ |----------- |
|datastore      |string  |A backend datastore, i.e., `'clingo'`, `'duckdb'`, or `'rdflib'` |REQUIRED |
|dataset        |string OR `Control` object OR `DuckPyConnection` object OR `GeistGraph` object |(1) A string indicates the name of the dataset stored on disk OR (2) a `Control` object, a `DuckPyConnection` object, or a `GeistGraph` object for dataset in memory |REQUIRED |
|inputfile      |string  |File containing the query |REQUIRED |
|isinputpath    |bool    |True if the inputfile is the file path, otherwise the inputfile is the content |REQUIRED |
|hasoutput      |bool    |True to store the query results as a CSV file or print them out |REQUIRED |
|config         |dict    |A dictionary with configurations when `hasoutput=True` |see below |

Description for the *config* parameter:

|Name           |Type    |Description                    | Default    |
|-------------- |------- |------------------------------ |----------- |
|outputroot     |string  |Path of the directory to store the query results |`'./'`  |
|outputfile     |string  |Path of the file to store the query results |`None`       |
|returnformat   |string  |Format of the returned data, i.e., `'lp'`, `'df'`, or `'dict'`. Available for `clingo` data backend only. |`'lp'` |
|predicate      |string  |Name of the predicate to be queried. Available for `clingo` data backend only. |`None` |
|programname    |string  |Name of the program. Available for `clingo` data backend only.           |`'base'`    |

??? example "Example 1: all rows of the `df` table in `test` dataset on disk (query from a string)"

    There exist a file with the path of `.geistdata/duckdb/test.duckdb`. The following code returns a Pandas data frame named `res` with query results, and a `DuckPyConnection` object.

    ```
    import geist

    # Query the df table of the test dataset
    (res, conn) = geist.query(datastore='duckdb', dataset='test', inputfile="SELECT * FROM df;", isinputpath=False, hasoutput=False)
    ```

??? example "Example 2: all rows of the `df` table in `test` dataset on disk (query from a file)"

    There exist a file with the path of `.geistdata/duckdb/test.duckdb`. The following code returns a Pandas data frame named `res` with query results, and a `DuckPyConnection` object.

    Here is the `query.txt` file:

    ```file
    SELECT * FROM df;
    ```

    Code:
    ```
    import geist

    # Query the df table of the test dataset
    (res, conn) = geist.query(datastore='duckdb', dataset='test', inputfile="query.txt", isinputpath=True, hasoutput=False)
    ```

??? example "Example 3: all rows of the `df` table in `test` dataset in memory (query from a string)"

    Suppose `conn` is a `DuckPyConnection` object points to a DuckDB dataset in memory. The following code returns a Pandas data frame named `res` with query results, and the same `DuckPyConnection` object.

    ```
    import geist

    # Query the df table of the test dataset
    (res, conn) = geist.query(datastore='duckdb', dataset=conn, inputfile="SELECT * FROM df;", isinputpath=False, hasoutput=False)
    ```

??? example "Example 4: all rows of the `df` table in `test` dataset in memory (query from a file)"

    Suppose `conn` is a `DuckPyConnection` object points to a DuckDB dataset in memory. The following code returns a Pandas data frame named `res` with query results, and the same `DuckPyConnection` object.

    Here is the `query.txt` file:

    ```file
    SELECT * FROM df;
    ```

    Code:
    ```
    import geist

    # Query the df table of the test dataset
    (res, conn) = geist.query(datastore='duckdb', dataset=conn, inputfile="query.txt", isinputpath=True, hasoutput=False)
```
