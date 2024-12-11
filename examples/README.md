# Example Project Setup
This example demonstrates the usage of gitHub specific operators.

## Steps to Set Up the Project
1. **Add Your GitHub Personal Access Token (PAT):**
   - Navigate to the `examples` directory.
   - Open the `secrets.json.example` file.
   - Replace the placeholder with your GitHub PAT.
   - Save the file as `secrets.json`.

     ```json
        {
          "github_conn_id": {
            "password": "YOUR-GETHUB-PAT-HERE"
          }
        }
     ```

2. **Start the Application:**
   - Run the following command to bring up the Docker environment:

     ```bash
     docker-compose up
     ```

3. **Trigger the DAG:**
   - Access the Airflow web interface.
   - Trigger github_dag DAG to execute.
