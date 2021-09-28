# Coding Challenge

## How to run

The easiest way to run the implementation is to use VSCode .devcontainer and docker.

### With VSCode and Docker

1. Open folder in VSCode
2. Install remote containers extension [ms-vscode-remote.remote-containers] (if not previously installed)
3. Open folder in container
4. Run mysql service with `service mysql start`
5. Execute tasks by running `python3 -m src api` or `python3 -m src sql`

### With Docker without VSCode

1. Build the image from the Dockerfile located at `.devcontainer/Dockerfile`
2. Open a container with the image and mount this folder
3. Run mysql service with `service mysql start`
4. Execute tasks by running `python3 -m src api` or `python3 -m src sql`

### Without Docker

1. Ensure python3 and mysql are installed
2. Install the following python requirements
   - mysql-connector-python==8.0.26
   - Flask==2.0.1
3. Setup the following mysql accounts

   ```bash
   domain: localhost
   user: sql_task
   password: sql_task
   database: sql_task

   domain: localhost
   user: api_task
   password: api_task
   database: api_task
   ```

4. Ensure mysql is running
5. Execute tasks by running `python3 -m src api` or `python3 -m src sql`

## Code structure and future improvements

1. The code is built and tested on Python 3.6.9 and MySQL 5.7.35.
2. `src` contains the two tasks implementation and provides a CLI interface to execute them.
3. `src/tasks/sql` contains the implementation of the SQL task.
   1. `src/tasks/sql/task.py` contains the answers to each of the questions as separate class functions. I have opted to write the SQL as formatted strings as at this scale it enabled easily managing all tasks.
4. `src/tasks/api` contains the implementation of the API task.
   1. The API has a pseudo MVC architecture with a rudimentary datamapper implementation.
   2. Ideally we would replace the datamapper with a proper ORM solution such as SQLAlchemy for scaling up. I have implemented data mapping using prepared statements as I wasn't sure about what we wanted to optimize and test here.
   3. At present route controllers directly instantiate models and datamapper. This might be better managed using Factory/Singleton pattern.
   4. Tests, logging, authentication/authorization has not been implemented.
5. Fixture data for dev and test should be migrated from the Python db files. At the moment they are in the same location because of interdependencies.
6. Dev environment should be split into MySQL and Python containers so that they much deployment configuration.
7. A lot of this setup may not be needed if we make each API a serverless function. Depending on the usecase, that might be a more suitable architecture.
