# Project Overview

This repository is a comprehensive guide to learning FastAPI, from basic concepts to cloud deployment. It includes several example projects that demonstrate how to serve a static website with FastAPI using different project structures and dependency management techniques.

The main components are:

*   **`kaira-1.0.0`**: A static website for a fashion store, which serves as the frontend for the FastAPI applications.
*   **`kaira-server`**: A simple FastAPI application that serves the static website. It uses a single `main.py` file and a `requirements.txt` for dependencies.
*   **`kaira-fastapi-poetry`**: A more structured FastAPI application that uses Poetry for dependency management and a modular project structure.
*   **`docs`**: A collection of markdown files that provide a step-by-step guide to learning FastAPI, covering topics such as CLI usage, Poetry, testing, logging, database integration, Docker, and cloud deployment.

## Building and Running

### `kaira-server`

To run the `kaira-server` application:

1.  Install the dependencies:
    ```bash
    pip install -r kaira-server/requirements.txt
    ```
2.  Run the application:
    ```bash
    uvicorn app.main:app --reload --app-dir kaira-server
    ```

### `kaira-fastapi-poetry`

To run the `kaira-fastapi-poetry` application:

1.  Install the dependencies using Poetry:
    ```bash
    poetry install --directory kaira-fastapi-poetry
    ```
2.  Run the application:
    ```bash
    poetry run uvicorn kaira_fastapi_poetry.main:app --reload --app-dir kaira-fastapi-poetry/src
    ```

## Development Conventions

The repository follows a structured, tutorial-based approach to learning FastAPI. The code examples demonstrate best practices for building and organizing FastAPI applications, including:

*   **Dependency Management**: Using `requirements.txt` for simple projects and Poetry for more complex applications.
*   **Project Structure**: Progressing from a single-file application to a modular structure with separate files for API endpoints, configuration, and other concerns.
*   **Testing**: The `docs` provide guidance on testing FastAPI applications using `pytest` and `TestClient`.
*   **Logging**: The `kaira-server` application includes an example of how to set up and use logging in a FastAPI application.
*   **Configuration**: The `kaira-fastapi-poetry` application demonstrates how to use a settings object for application configuration.
