# Products microservice
This repository goal is to provide the ready to use code for the products microservice, with the necessary instructions to test it.
The code implements the four basic REST APIs (GET, POST, PUT, DELETE), with their related endpoints, that are designed and configured to communicate with DynamoDB.

The code is written in python, it implements the [FastAPI](https://fastapi.tiangolo.com/) framework that comes with multiple advantages such as the automatic inputs validation, error management, and automated generation of [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification) for HTTP APIs.
It's possible to test the APIs thanks to [Swagger](https://swagger.io/) very easily by going to the dedicated endpoint (if tested in local it is `localhost:8080/docs`). Moreover, the code includes a dedicated logging system through the dedicated python library `logging` appropriately configured.

All the code is designed to run in a simple Docker container (see the _Dockerfile_), to maintain all the advantages of the microservices architecture, run in a lightweight isolated environment (so other microservices can be added following this architecture) in order to decouple the microservice, and to easily allow its scalability thanks to the cloud architecture.
Since the code is designed to work correctly with the Docker container, it's better to test it _as is_ with the provided cloud AWS infrastructure [go to inserire link]() or, if you want, you can test it in your local machine by following the __local execution__ steps below by running a Docker container.

## Test the code

### Prerequisites
In order to run this code, you must satisfy these prerequisites:
- Have an AWS account with both access and secret keys.
- Have access to AWS DynamoDB
- Have Docker installed locally (needed to test locally)

### Test the microservice
#### Test it in the AWS Cloud Infrastructure
1. Go to the products microservice endpoint: 
    - [endpoint]()
2. Test the APIs. You can:
    - List all the items in the products database
    - Search a product through its ID
    - Search a product through its name (the first with the selected name will be returned)
    - Modify the attributes of a product searching it from its ID
    - Delete a product from its ID
    
    __Note__: The APIs documentation is available in the Swagger interface for each API. More on the APIs documentation at the end of the readme, in the dedicated chapter.


#### Test it locally

1. Clone locally the final code version from the __production__ branch [here](https://github.com/martinalilla/master-cde-2023-module-7-microservices-products/tree/production).
2. Build the Docker image by running:
    ```
    docker build --build-arg PROJECT_ID=products -t productsimage .
    ```
3. Start the Docker container with:
    ```
    docker run --env-file=.env.development -d --name productscontainer -p 8080:8080 productsimage
    ```
4. Test the products microservice going to the address `localhost:8080/docs`

## Software Management Approach
### TEAM Responsibilities 
Here the goals of each team member's work:
- Lilla Martina: Microservice backbone & template, team coordination
- Patanè Gabriele: Readme, test microservice in local and cloud, platform team interactions
- Puzzo Michele: Post & Get APIs
- Ursino Zarmina: Put & Delete APIs

The team has been organized per tasks, with the major goal to equally divide the total amount of work. The team had three meetings per week, in order to constantly review the activities and solve the encountered problems. For each week a final goal has been assigned (i.e. 1st week: complete the microservice code template, 2nd week: implement the first API, etc) based on the final delivery date.

Finally, the team also actively cooperated with the platform team with multiple meetings when the project started, and then, one meeting per week, in order to clarify and meet the technological constraints, and to develop a functional and easy-to-use code to implement the products microservice. This was fundamental in order to generate the final code to later use in the cloud environment or locally through a Docker image and container.

### Branching Strategy

The chosen branching strategy consists in a mix of __Release Branching__ (one branch for development, one for test and one for production) and __Feature Branching__ (e.g. _Post&Get/products_). This mix has been chosen to follow the best practices in a real work environment.

The __Feature Branching__ approach is used to implement the new features (i.e. the POST, GET, PUT, DELETE APIs + docs) in order to allow the developers to work in isolation each others (after assigned the activities to each of them); once the feature is complete, it is merged back into the _development_ branch, in order to test it with the provided development infrastructure. 

The __Release Branching__ approach has been implemented to have different versions of the working code. In particular, we can distinguish three branches: _Development_, _Test_ and _Production_, like in real case scenarios. Each branch reflects a dedicated environment (each with the purpose of the branch name),
so, for example, when the __development__ branch is updated, it is because this new code version will be used in the related development cloud environment, in order perform basic tests, fix the related bugs / problems (by making dedicated __bugfix__ branches to later merge them in the _development branch_ once the fix has been completed), and, finally, if the tests are successful, the code can be pushed to the other _release_ branches: first in the __test__ branch, to perform other and more complex tests, and, finally, after each test has been completed in the dedicated test environment - otherwise, even in this case, dedicated _bugfix_ branches will be created - it will be pushed in to the __production__ branch, that is the final branch where the cleaned and well-working code resides with its dedicated production environment, so its represents the final stage of the code development. 

In this specific case, even if there are three _release branches (dev, test, prod)_ to follow the best practices, the _test_ branch is ininfluent for our scope because of the lack of its dedicated cloud environment, and also for the simplicity of this microservice. So, only _development_ and _production_  branches will be taken into account for this project.

When the code is pushed in the _production branch_, of course, some problems and bugs can later occur (you can be very good, but not perfect!) due to different reasons (like changes in the infrastructure, or something that needs to be added, etc). In this case, this branching strategy helps us; in fact, the problems can be solved with a new version of the code! Everything starts again from the features of the development branch, and it continues as described above, up to the production branch, that will always reflects the current and active production environment. But in this case all the other branches, will be named and contain the new version of the code which is put also in the branches names.

### Merging Strategy
Defining a merging strategy is necessary to allow each developer to work in an ordered and efficient way, to align the team's workflow, meet the project requirements in a structured way and to also have a better quality code. The merging happens between _feature branches_ towards _release branches_ each time that a new feature / bugfix is completed.


The workflow is the following:
1. Definition of new features - problems
2. Activities assignment to each team member
3. Creation of dedicated _feature branches_ (based on the previous assignment), starting from the _development_ branch
4. Once a feature is completed, its _feature branch_ needs to be merged to the _development branch_ in order to be tested.
5. Now a __Pull Request__ is expected. If the reviewer of the _pull request_ approve it, it is merged to the _development branch_ in order to be tested, otherwise it will be rejected with the reason, in such way that the developer can fix the problem and apply the _PR_ another time. In this case, since the team had multiple calls (3 per week) and reviewed everything all together during those meetings, instead of having multiple pull requests, the team decided to merge directly the branches when ready. 
6. The code in _development branch_ is tested in its dedicated infrastructure, in order to verify if there are some problems with the application, and, if so, restart from the point 1.
7. At this point, the code passed all the tests and it's ready to go in production! So, a new _pull request_ is made, from the _development_ to the _production branch_, to update the latter with the latest code version.


---
### Local tests Environment preparation
This section shows how the code development has been approached in the team's local machines.
The code has been developed and tested locally thanks to [Visual Studio Code](https://code.visualstudio.com/Download) in Windows computers, so the following steps are guaranteed to work smoothly with this configuration. If you use other tools or operating systems, apply the needed changes.

Below the required steps to run and test the code locally during the development: 
1. Create a launch.json file with the following content:
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
2. Set up a virtual environment:
  - With the following command create and name it `.venv` to isolate your project dependencies:
    ```
    python -m venv --copies .venv
    ```

  - Activate the virtual environment
    ```
    .venv\Scripts\activate.bat
    ```
  - Install the requirements contained into requirements.txt file
    ```
    pip install -r requirements.txt
    ```
3. Create and set your .env file with the following infos:
    ```
    ENVIRONMENT=local           # where you're going to test the code
    VERSION=1.0                 # the version                                           
    MICROSERVICE_NAME=products  # microservice name
    MICROSERVICE_DESCRIPTION="The Products microservice is a self-contained service responsible for managing product data within a larger application. It provides functionalities to create, retrieve, update, and delete product information."                                                
    
    LOGGING_LEVEL=DEBUG         # logging level used in the code for the logging python package
    DYNAMODB_TABLE=MCDE2023-d-products            
    DYNAMODB_REGION=<your region> #eg eu-west-1

    AWS_ACCESS_KEY_ID=<your_aws_access_key>
    AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key>
    ```
4. Now you can do the first test of the code and use the virtual environment you created in your local machine in step 2. To do so, launch the Visual Studio Code debugger.
5. Now you're ready for the final test: test the microservice in a Docker container. To do so, you can build and start the Docker container specified in the `Dockerfile` in this way:

    - Build the Docker Image
      ```
      docker build --build-arg PROJECT_ID=products -t productsimage .
      ```

    - Start the Docker Container
      ```
      docker run --env-file=.env.development -d --name productscontainer -p 8080:8080 productsimage
      ```


6. With your browser, go to `localhost:8080/docs` and test the APIs.


---
### Code Structure:
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
There is a custom class that mocks a DB library.
The DAOs are responsible for the DB management. 
DAOs are not DBs. DAOs **uses** the DBs. The idea is that if you change DB, you have to do some adjustment only into your DAOs. 
Controllers and routers should not be changed.



### API Documentation
The code implements the [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification) interface description for HTTP APIs through the [FastAPI](https://fastapi.tiangolo.com/) framework to easily and automatically build them. It's possible to test the APIs through [Swagger](https://swagger.io/) very easily by going to `localhost:8080/docs`. In particular, this configuration has been chosen because __FastAPI__ is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. It's easy to use and automatically produces interactive API documentation. The APIs are designed according to the __OpenAPI Specification__. The OpenAPI Specification (OAS) defines a standard, language-agnostic interface to HTTP APIs which allows both humans and computers to discover and understand the capabilities of the service without access to source code, documentation, or through network traffic inspection. When properly defined, a consumer can understand and interact with the remote service with a minimal amount of implementation logic. The API documentation is __automatically generated__ (see the __OpenAPI Spec__ below) and it can be accessed through a user-friendly interface provided by __Swagger UI__. Swagger allows you to describe the structure of your APIs so that machines can read them. The ability of APIs to describe their own structure is the root of all awesomeness in Swagger. It can automatically build beautiful and interactive API documentation. Moreover, through the Swagger UI interface (you can reach it by following the steps in _test the microservice_ chapter of this readme), you can also interactively test the APIs. simply click on an API endpoint to expand it, fill in any required parameters, and click "Try it out!".



#### Generate OpenAPI spec as yaml file
The OpenAPI spec can also be generated as `openapi.yaml` through the dedicated python script `extract_openapi.py` to be easily shared with other teams (other STREAM teams, and Platform team). 

To generate the OpenAPI spec, please, run in your active virtual environment the following commands:
```
$env:ENVIRONMENT="local"
$env:PYTHONPATH="./app"
python extract_openapi.py
```