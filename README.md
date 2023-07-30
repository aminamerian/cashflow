# Cashflow

This is a Dockerized Django project with SQLite as the database backend.

## Getting Started

- Clone the repository:

   ```bash
   git clone git@github.com:aminamerian/cashflow.git
    ```

- Run the docker containers:

   ```bash
   docker-compose up
   ```
  This will run `makemigrations`, `migrate` and `collectstatic` commands and then run the server on port **8000**.


- Run the tests:

   ```bash
    docker exec -it <container-name> pytest
   ```