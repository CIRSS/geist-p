**query** method of the *Connection* class can query a dataset stored on disk or in memory. It is very similar to the `query()` function. The only difference is that the `datastore` and the `dataset` parameters do not need to be passed as they have already been specified while initialze the *Connection* class.

Parameters description for *query* method of the *Connection* class:

|Name           |Type    |Description                                | Default   |
|-------------- |------- |------------------------------------------ |---------- |
|inputfile      |string  |File containing the query                  |[required] |
|isinputpath    |bool    |True if the inputfile is the file path, otherwise the inputfile is the content |[required] |
|hasoutput      |bool    |True to store the query results as a CSV file or print them out |[required] |
|config         |dict    |A dictionary with configurations when `hasoutput=True` | see below |

Description for the *config* parameter:

|Key            |Type    |Description                                     | Default   |
|-------------- |------- |----------------------------------------------- |---------- |
|outputroot     |string  |Path of the directory to store the query results|'./'       |
|outputfile     |string  |Path of the file to store the query results     |None       |

??? example "Example 1: all rows of the `df` table in `test` dataset on disk (query from a string)"

    There exist a file with the path of `.geistdata/duckdb/test.duckdb`. The following code returns a Pandas data frame named `res` with query results.

    ```
    import geist

    # Create a Connection instance
    connection = geist.Connection.connect(datastore='duckdb', dataset='test')
    # Query the df table of the test dataset
    res = connection.query(inputfile="SELECT * FROM df;", isinputpath=False, hasoutput=False)
    ```

??? example "Example 2: all rows of the `df` table in `test` dataset on disk (query from a file)"

    There exist a file with the path of `.geistdata/duckdb/test.duckdb`. The following code returns a Pandas data frame named `res` with query results.

    Here is the `query.txt` file:

    ```file
    SELECT * FROM df;
    ```

    Code:
    ```
    import geist

    # Create a Connection instance
    connection = geist.Connection.connect(datastore='duckdb', dataset='test')
    # Query the df table of the test dataset
    res = connection.query(inputfile="query.txt", isinputpath=True, hasoutput=False)
    ```

??? example "Example 3: all rows of the `df` table in `test` dataset in memory (query from a string)"

    Suppose `conn` is a `DuckPyConnection` object points to a DuckDB dataset in memory. The following code returns a Pandas data frame named `res` with query results.

    ```
    import geist

    # Create a Connection instance
    connection = geist.Connection(datastore='duckdb', dataset=':memory:', conn=conn)
    # Query the df table of the test dataset
    res = connection.query(inputfile="SELECT * FROM df;", isinputpath=False, hasoutput=False)
    ```

??? example "Example 4: all rows of the `df` table in `test` dataset in memory (query from a file)"

    Suppose `conn` is a `DuckPyConnection` object points to a DuckDB dataset in memory. The following code returns a Pandas data frame named `res` with query results.

    Here is the `query.txt` file:

    ```file
    SELECT * FROM df;
    ```

    Code:
    ```
    import geist

    # Create a Connection instance
    connection = geist.Connection(datastore='duckdb', dataset=':memory:', conn=conn)
    # Query the df table of the test dataset
    res = connection.query(inputfile="query.txt", isinputpath=True, hasoutput=False)
    ```
