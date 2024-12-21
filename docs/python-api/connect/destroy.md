**destroy** method of the *Connection* class is to delete the dataset and close the dataset connection.

??? example "Example: delete the dataset and close the connection"

    Suppose `connection` is the instance of the *Connection* class for a DuckDB dataset named `test` stored on disk. The following code will delete the `.geistdata/duckdb/test.duckdb` file.

    ```
    # Delete the dataset and close the connection
    connection.destroy()
    ```
