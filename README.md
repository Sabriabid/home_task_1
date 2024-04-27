# homte_task_1
 home_task_1

 ![app_diagram_azure](https://github.com/Sabriabid/home_task_1/assets/77688551/998afb9c-1be2-485b-8fe3-cd01472a59d7)


# Data Ingestion and API Service

This project implements a simple ETL (Extract, Transform, Load) pipeline and a REST API service designed to ingest data from CSV files into a database and expose the ingested data.

## Features

- **ETL Pipeline**: Extracts data from one or multiple CSV files, transforms it, and loads it into a database.
- **REST API**: Exposes the recently ingested data, making the first 10 rows available through a dedicated endpoint.
- **Logging**: Both ETL and API components produce comprehensive logs for traceability and debugging.
- **Testing**: Includes unit tests to ensure the integrity of the ETL process and the reliability of the API endpoint.
- **Dockerization**: The application is containerized using Docker, enabling easy deployment and scaling.

## Components

- `etl.py`: Python script for the ETL process to load CSV data into the database.
- `api.py`: Flask application providing the REST API to access ingested data.
- `test_load_data.py`: Test cases for validating the ETL process and API responses.
- `dockerfile` and `docker-compose.yml`: Configuration files for Docker deployment.
- `start.sh`: Shell script to sequentially run ETL and API services.
- `requirements.txt`: List of Python dependencies for the project.

## API Usage

- **Endpoint**: `GET /read/first-chunk`
- **Description**: Returns the first 10 lines from the database in JSON format.
- **Response**: A successful response with HTTP 200 OK status code along with a JSON array of 10 objects.

## Deployment

The application is designed to be deployed to cloud platforms such as Azure, AWS, or Kubernetes. A system diagram illustrating the cloud deployment architecture is included with the project.

## Running Locally

To run the application locally:

1. Ensure you have Docker installed and running on your machine.
2. Build the Docker image using:

``docker build -t data-ingestion-api``

3. Start the services using Docker Compose:

``docker-compose up``

## Tests

Run the included tests locally using:

``pytest``
