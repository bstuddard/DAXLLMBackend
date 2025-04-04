import os, sys, clr
from typing import Any, Optional

# Add the ADOMD.NET assembly path
adomd_path = r"C:\Program Files\DAX Studio\bin"
sys.path.append(adomd_path)

# Add reference to the DLL
clr.AddReference(os.path.join(adomd_path, "Microsoft.AnalysisServices.AdomdClient"))

# Import the required .NET types
from Microsoft.AnalysisServices.AdomdClient import AdomdConnection # type: ignore
from Microsoft.AnalysisServices.AdomdClient import AdomdCommand # type: ignore


def run_dax_query(query: str, initial_catalog: str = "7fc3799c-9559-494a-9342-cc91963e9803") -> Optional[list[dict[str, Any]]]:
    """Execute a DAX query against a local Analysis Services instance.

    Args:
        query (str): The DAX query to execute.
        initial_catalog (str, optional): The database ID to connect to. 
            Defaults to "7fc3799c-9559-494a-9342-cc91963e9803", but should be changed to local key.

    Returns:
        Optional[list[dict[str, Any]]]: A list of dictionaries where each dictionary represents
            a row of the query result. Each dictionary maps column names to their values.
            Returns None if the query execution fails.

    Raises:
        Exception: Prints error message if query execution fails.

    Example:
        >>> query = "EVALUATE VALUES('Table'[Column])"
        >>> results = run_dax_query(query)
        >>> if results:
        ...     for row in results:
        ...         print(row)
    """
    conn = None  # Define connection outside try block so it's accessible in finally
    try:
        # Connection string with the initial_catalog parameter
        connection_string = (
            "Provider=MSOLAP.8;"
            "Data Source=localhost:57406;"
            f"Initial Catalog={initial_catalog}"
        )

        # Create and open connection
        conn = AdomdConnection(connection_string)
        conn.Open()

        # Create and execute command with the provided query
        cmd = AdomdCommand(query, conn)
        reader = cmd.ExecuteReader()

        # Store results in a list of dictionaries
        results = []
        while reader.Read():
            row = {}
            for i in range(reader.FieldCount):
                row[reader.GetName(i)] = reader.GetValue(i)
            results.append(row)

        return results

    except Exception as e:
        print(f"Error executing DAX query: {str(e)}")
        return None

    finally:
        # Close connection if it was opened
        if conn is not None:
            conn.Close()