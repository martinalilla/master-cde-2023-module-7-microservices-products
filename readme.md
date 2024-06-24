# Products microservice
#TODO Add description

### Software Management Approach
Chosen approach: Release Branching (one branch for development, one branch for test, one branch for production) + Feature Branching (e.g. feat/create-product).
#TODO: Extend description

---
### To Start
- If you are working in VisualStudio Code, create a launch.json file with the following content:
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Microservice Development",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/run.py",
            "env": {
                // adjust pythonpath for local module 
                "PYTHONPATH": "${workspaceFolder}/app"
            },
            "envFile": "${workspaceFolder}/.env.development",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Microservice Test",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/run.py",
            "env": {
                // adjust pythonpath for local module
                "PYTHONPATH": "${workspaceFolder}/app"
            },
            "envFile": "${workspaceFolder}/.env.test",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Microservice Production",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/run.py",
            "env": {
                // adjust pythonpath for local module
                "PYTHONPATH": "${workspaceFolder}/app"
            },
            "envFile": "${workspaceFolder}/.env.production",
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```
- Create your Virtual Environment: 
    1. Setup a virtual environment
    Set up a virtual environment (optional but recommended), named venv to isolate your project dependencies.
    ```
    python -m venv --copies .venv
    ```

    2. Activate the virtual environment
    ```
    .venv\Scripts\activate.bat
    ```
- Install the requirements contained into requirements.txt file
    ```
    pip install -r requirements.txt
    ```
- Start "run.py" using the specific .env file in order to use custom environment variable.
  - With your browser, go to _localhost:8080/docs_


---
### Structure:
- **config**: used for your configurations like:
  - environment variable read
  - secrets data read
  - ecc

- **controller**: Controller pillar of MVC. Here there is all the business logics and it is divided into 2 sub folders:
  - **private**: contains the business logics that should be related to private/internal endpoint calls inside your own backend services
  - **public**: contains the business logics that should be related to your public endpoints

- **model**: Model pillar of MVC. Contains all models, DAO, DTO ecc. There are 2 sub folders:
  - **daos**: contains DBs logics and database data manipulation.
  - **schemas**: data representation useful for business logics, input/output models.
  - **db_schemas**: database data representation.

- **router**: View pillar or MVC. Contains all endpoint divided by functionalities. There are 2 sub folders:
  - **private**: used for private/internal endpoints
  - **public**: used for public endpoints

- **utils**: contains logics that could be re-used. This folder could be (or better, must be) replaced by a private library in order to share the code among micro-services.

The **v1** folder is used in order to version your code. In this way you can deploy a new version (v2) and at the same time maintain also the older one.
The v1 folder (v2, v3 ecc) is a sub-folder of **app**. This last folder, **app** should be the unique folder you have to deploy. It contains your application code.

### Database 
There is a custom class that mock a DB library.
The DAOs are responsible for the DB management. 
DAOs are not DBs. DAOs **uses** the DBs. The idea is that if you change DB, you have to do some adjustment only into your DAOs. 
Controllers and routers should not be changed.


### Docker
1. **Build the Docker Image**
    ```
    docker build --build-arg PROJECT_ID=products -t productsimage .
    ```

2. **Start the Docker Container**
    ```
    docker run --env-file=.env.development -d --name productscontainer -p 8080:8080 productsimage
    ```


### CI/CD
#TODO Add description


### Generate OpenAPI spec
    ```
    set ENVIRONMENT=local
    set PYTHONPATH=./app
    python extract_openapi.py
    ```