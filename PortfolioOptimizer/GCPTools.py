"""
Tools to help with Google Cloud Platform.

Classes:
    GCPTools: Creates connections and interactions with GCP.
"""

from google.cloud import bigquery
from google.oauth2 import service_account


class GCPTools(object):
    """
    Creates connections and interactions with GCP.

    Methods:

    """

    def __init__(self, service_type, scope, credentials, client=None):
        """
        Args:
            service_type(string): The plain english name of the GCP
                service we will be connecting to. This can be implied
                from scope, but is more reader friendly this way.
                Currently supports 'bigquery'.
            scope(string): The scope of the connection, such as bigquery
                or read/write storage, as
                'https://www.googleapis.com/auth/bigquery'
                See scopes here:
                https://developers.google.com/identity/protocols/oauth2/scopes
            credentials(string): Path to service account credentials.
            client: The connection to GCP once set up.
        """

        self.service_type = service_type
        self.scope = scope
        self.credentials = credentials
        self.client = client

        # we connect to a GCP service here so that we don't need to
        # reconnect every time something runs because in some cases
        # we will be rerunning multiple times, such as storing new data
        # set scopes and credentials
        scope = [self.scope]
        our_credentials = self.credentials
        # get credentials
        creds = service_account.Credentials.from_service_account_file(
            our_credentials, scopes=scope)
        # set up client
        if self.service_type == 'bigquery':
            self.client = bigquery.Client(credentials=creds)
        else:
            log_str = ("*******************Error*******************\n"
                       "GCPTools currently only supports connections to "
                       "bigquery (service_type='bigquery').")
            raise ValueError(log_str)

    def store_df_bigquery(self, df, project, dataset, table_name):
        """
        Stores a DataFrame to BigQuery.

        Args:
            df(pandas.DataFrame): The dataframe to store.
            project(string): The GCP project.
            dataset(string): The GCP dataset.
            table_name(string): The GCP table name.

        Returns:
            N/A
        """

        # set up table_id and load
        table_id = project + "." + dataset + "." + table_name
        job = self.client.load_table_from_dataframe(df, table_id)
        job.result()

        try:
            table = self.client.get_table(table_id)  # Make an API request
        except Exception as e:
            log_str = ("*******************Error*******************\n"
                       "Error getting table from BigQuery.\n"
                       "Error: " + str(e))
            raise ValueError(log_str)

    def pull_df_bigquery(self, project, dataset, table_name, index=None):
        """
        Pull DataFrame data from BigQuery.

        Args:
            project(string): The GCP project.
            dataset(string): The GCP dataset.
            table_name(string): The GCP table name.
            index(string): If we want to set an index for the DataFrame,
                the default from BigQuery is to only set the column names.

        Returns:
            df(DataFrame): The DataFrame with the data.
        """

        # create and run the query
        table_id = project + "." + dataset + "." + table_name
        sql_statement = f"SELECT * FROM {table_id}"
        query_job = self.client.query(sql_statement)
        query_job.result()

        table = self.client.get_table(table_id)  # Make an API request.
        print("Pulled {} rows and {} columns from {}".format(
            table.num_rows, len(table.schema), table_id))

        # create the df and set the index if we want to
        df = query_job.to_dataframe()
        if index:
            df.set_index(index, inplace=True)
            df.sort_index(inplace=True)

        return df
