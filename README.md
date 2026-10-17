# CI/CD Pipeline Integration for Networked Software Testing

## Project Overview

This project demonstrates how to build and test networked software services using a Continuous Integration and Continuous Delivery (CI/CD) pipeline.

It contains two Python-based HTTP services that communicate over a network. Docker Compose manages the services, pytest performs integration testing, and GitHub Actions automatically builds the services and runs the tests when changes are pushed to GitHub or submitted through a pull request.

## Objectives

- Develop two independent networked services.
- Enable communication between services through HTTP.
- Containerize services using Docker.
- Orchestrate containers using Docker Compose.
- Automate integration tests using pytest.
- Generate HTML and JUnit XML test reports.
- Run automated testing through GitHub Actions.
- Capture service logs and clean up containers during CI execution.

## System Architecture

**Client / Integration Tests → Gateway Service → User Service**

- **User Service:** Provides user data and a health endpoint.
- **Gateway Service:** Receives API requests and forwards user requests to the User Service.
- **Docker Compose:** Builds and runs both services with service discovery and health checks.
- **pytest:** Validates API responses, service health, and error handling.
- **GitHub Actions:** Automates the build, startup, test execution, report upload, and cleanup process.

## Technologies Used

- Python 3.12
- pytest
- pytest-html
- Docker
- Docker Compose
- GitHub Actions
- HTTP and JSON
- Git and GitHub

## Project Structure

```text
ci-cd-network-testing/
├── .github/
│   └── workflows/
│       └── ci.yml
├── test_services/
│   ├── gateway_service/
│   │   ├── app.py
│   │   └── Dockerfile
│   └── user_service/
│       ├── app.py
│       └── Dockerfile
├── tests/
│   └── test_gateway_integration.py
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

## Services and Endpoints

### User Service

Runs on port `8000` on the host machine.

| Endpoint | Purpose |
|---|---|
| `GET /health` | Checks service health |
| `GET /users/1` | Retrieves user 1 |
| `GET /users/2` | Retrieves user 2 |

### Gateway Service

Runs on port `8001` on the host machine.

| Endpoint | Purpose |
|---|---|
| `GET /health` | Checks service health |
| `GET /api/status` | Checks gateway status |
| `GET /api/user/1` | Retrieves user data through the gateway |
| `GET /api/user/abc` | Tests invalid user ID handling |
| `GET /api/user/999` | Tests missing user handling |

## Run the Project Locally

### Prerequisites

Install Python 3.12 and Docker Desktop with Docker Compose support.

### 1. Clone the repository

```bash
git clone https://github.com/hariharan81k/ci-cd-network-testing.git
cd ci-cd-network-testing
```

### 2. Install test dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Validate Docker Compose configuration

```bash
docker compose config -q
```

### 4. Build and start services

```bash
docker compose up -d --build
```

### 5. Run integration tests

```bash
python -m pytest -v tests/test_gateway_integration.py
```

### 6. Generate test reports

```bash
python -m pytest -v tests/test_gateway_integration.py --junitxml=reports/junit-results.xml --html=reports/test-report.html --self-contained-html
```

### 7. Stop services

```bash
docker compose down
```

## Automated CI/CD Pipeline

The GitHub Actions workflow is defined in `.github/workflows/ci.yml`.

It performs these steps:

1. Checks out the repository.
2. Sets up Python.
3. Installs test dependencies.
4. Validates the Docker Compose configuration.
5. Builds and starts the services.
6. Waits for the service health endpoints.
7. Runs integration tests.
8. Uploads test reports as a workflow artifact.
9. Displays service logs if a step fails.
10. Stops services and cleans up containers.

The workflow runs on pushes to `main`, pull requests targeting `main`, and manual workflow dispatches.

## Integration Test Results

The integration test suite currently contains six tests, all passing in the latest local run.

- **Tests passed:** 6
- **Execution time:** 2.80 seconds
- **JUnit XML report:** Generated
- **HTML report:** Generated

### Test Coverage

| Test Scenario | Expected Result |
|---|---|
| Retrieve an existing user through the gateway | HTTP 200 |
| Invalid user ID | HTTP 400 |
| Missing user | HTTP 404 |
| User Service health check | HTTP 200 |
| Gateway Service health check | HTTP 200 |
| User Service unavailable | HTTP 502 |

The network failure test starts a temporary Gateway Service configured to contact an unavailable local port. It verifies that the gateway returns HTTP 502 with the expected `User service unavailable` error message.

The GitHub Actions workflow generates JUnit XML and HTML reports and uploads them as the `integration-test-reports` artifact.

## Test Reports

The CI workflow uploads reports as an artifact named `integration-test-reports`.

Open the [GitHub Actions runs](https://github.com/hariharan81k/ci-cd-network-testing/actions) page, select a successful run, and download the artifact.

## Key Learning Outcomes

- Network communication between independent services.
- HTTP status codes and API error handling.
- Docker image creation and multi-container orchestration.
- Integration testing with pytest.
- Health checks and service readiness.
- CI/CD automation using GitHub Actions.
- Automated test reporting and failure diagnostics.

## Future Improvements

- Add unit tests and additional integration scenarios.
- Add configurable timeouts and retry policies.
- Test service failures and recovery behavior.
- Add code quality checks and test coverage reporting.
- Add versioned releases and deployment automation.

## Author

**Hariharan K**

GitHub: [hariharan81k](https://github.com/hariharan81k)