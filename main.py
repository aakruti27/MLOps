from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError
from flask import Flask, request
import os

app = Flask(__name__)

PROJECT_ID = "king-dap-learning-sandbox"

# Initialize BigQuery client
big_query_client = bigquery.Client(project=PROJECT_ID)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/my-service-key.json"

@app.route('/',methods=['GET', 'POST']) # Ensure POST is allowed here
def main():
    try:
        table_id = f"{PROJECT_ID}.aa_test_schema.us_states"
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
        )
        uri = "gs://dap-learning-aakruti/us-states.csv"
        load_job = big_query_client.load_table_from_uri(
            uri, table_id, job_config=job_config
        )

        load_job.result()  # Wait for the job to complete

        destination_table = big_query_client.get_table(table_id)
        return {"data": destination_table.num_rows}
    except GoogleCloudError as e:
        return {"error": str(e)}, 500
    except Exception as e:
        return {"error": "Unexpected error occurred: " + str(e)}, 500


if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG", False), host="0.0.0.0", port=int(os.environ.get("PORT", 5052)))


