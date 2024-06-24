# Products microservice
This repository goal is to provide the ready to use code for the products microservice, with the necessary instructions to test it.
The code implements the four basic REST APIs (GET, POST, PUT, DELETE), with their related endpoints, that are designed and configured to communicate with DynamoDB.

The code is written in Python, it implements the [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification) interface description for HTTP APIs through the [FastAPI](https://fastapi.tiangolo.com/) framework to easily and automatically build them. It's possible to test the APIs through [Swagger](https://swagger.io/) very easily by going to `localhost:8080/docs`; Moreover, the code includes a dedicated logging system through the dedicated python library `logging` appropriately configured.

All the code is designed to run in a simple Docker container (see the _Dockerfile_), to maintain all the advantages of the microservices architecture, run in a lightweight isolated environment (so other microservices can be added following this architecture) in order to decouple the microservice, and to easily allow its scalability thanks to the cloud architecture.
Since the code is designed to work correctly with the Docker container, it's better to test it _as is_ with the provided image in ECR [inserire link]() with the provided AWS infrastructure, but, if you want, you can test it in your local machine by following the _local execution_ steps below (please, remember that you can encounter errors due to your different environment).

## Test the code

### Prerequisites
In order to run this code, you must satisfy these prerequisites:
- Have an AWS account with both access and secret keys.
- Have access to AWS DynamoDB and ECR
- Have Docker installed (needed to push the image to ECR)
- Have installed the [AWS-CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) (only if you want to test in local)

### Steps
1. Go to the products microservice endpoints: 
- endpoint


[rivedere a seconda di cosa dice il platform team]
Local Run

1. Take the final code version from the master branch
2. Build the Docker image with 
`docker build --build-arg PROJECT_ID=products -t productsimage .`
3. Start the Docker container with 
`docker run --env-file=.env.development -d --name productscontainer -p 8080:8080 productsimage`
4. Test the products microservice in `localhost:8080/docs`

## Software Management Approach
### TEAM Responsibilities 
Here the goals of each team member's work:
- Lilla Martina: Microservice backbone & template, team coordination, PR review
- Patanè Gabriele: Readme, test microservice in local and cloud
- Puzzo Michele: Post & Get APIs
- Ursino Zarmina: Put & Delete APIs

The team has been organized per tasks, with the major goal to equally divide the total amount of work. The team had three meeting per week, in order to constantly review the activities and solve the encountered problmems. For each week a final goal has been assigned (i.e. 1st week: complete the microservice code template, 2nd week: implement the first API, etc) based on the final delivery date.

Finally, the team also actively coperated with the platform team with multiple meetings when the project started, and then, one meeting per week, in order to clarify and meet the technological constraints, and to develop a functional and easy to use code to implement the products microservice. This was fundamental in order to generate the final Docker image to later use in the cloud environment.

### Branching Strategy

The chosen software management approach consists in a mix of __Release Branching__ (one branch for development, one branch for test, one branch for production) and __Feature Branching__ (e.g. _Post&Get/products_). This mix has been chosen to follow the best practices in a real work environment.

The __Feature Branching__ approach is used to implement the new features (i.e. the POST, GET, PUT, DELETE APIs + docs) in order to allow the developers to work in isolation each others (after assigned the activities to each of them); once the feature is complete, it is merged back into the _development_ branch, in order to test it with the provided development infrastructure. 

The __Release Branching__ approach has been implemented to have different versions of the working code. In particular, we can distinguish three branches: _Development_, _Test_ and _Production_, like in real case scenario. Each branch reflects a dedicated environment (each with the purpose of the branch name),
so, for example, when the _development_ branch is updated, it is because this new code version will be used in the related development cloud environment, in order to test it, fix the related bugs / problems (with dedicated __bugfix__ branches, as the _feature branching_ suggests), and, finally, if the tests are successful, the code can be pushed to the other _release_ branches: first in the _test_ branch, and, finally, after each test has been completed in the dedicated test environment - otherwise, even in this case, dedicated _bugfix_ branches will be created - it will be pushed in to the __production__ branch, that is the final branch where the cleaned and well-working code resides with its dedicated production environment, so its represent the final stage of the code development. 

When the code is pushed in the _production branch_, of course, some problems and bugs can later occur (you can be very good, but not perfect!) due to different reasons (like changes in the infrastructure, or something that needs to be added, etc). In this case, this branching strategy helps us; in fact, the problems can be solved with a new version of the code! Everything starts again from the features of the development branch, and it continues as described above, up to the production branch, that will always reflect the current and active production environment. But in this case all the other branches, will be named and contain the new version of the code which is put also in the branches names.

### Merging Strategy
Defining a merging strategy is necessary to allow each developer to work in an ordered and efficient way, to align the team's workflow, meet the project requirements in a structured way and to also have a better quality code. The merging happens between _feature branches_ towards _release branches_ each time that a new feature / bugfix is completed.

In this specific case, even if there are three _release branches (dev, test, prod)_ to follow the best practices, the _test_ branch is ininfluent for our scope because of the lack of its dedicated cloud environment, and also for the simplicity of this microservice. So, only _development_ and _production_  branches will be taken into account for this project.
The workflow is the following:
1. Definition of new features - problems
2. Activities assignment to each team member
3. Creation of dedicated _feature branches_ (based on the previous assignment), starting from the _development_ branch
4. Once a feature is completed, its _feature branch_ needs to be merged to the _development branch_ in order to be tested. A __Pull Request__ is opened.
5. If the reviewer of the _pull request_ approve it, it is merged to the _development branch_ in order to be tested, otherwise it will be rejected with the reason, in such way that the developer can fix the problem and apply the P_R_ another time.
6. The code in _development branch_ is tested in its dedicated infrastructure, in order to verify if there are some problems with the application, and if so, restart from the point 1.
7. At this point, the code passed all the tests and it's ready to go in production! So, a new _pull request_ is made, from the _development_ to the _production branch_, to update the latter with the latest code version.

---
### Environment preparation
The code has been tested with [Visual Studio Code](https://code.visualstudio.com/Download) in Windows computer, so teh following steps apply are guaranteed to work smoothly with this configuration. If you use other tools or operating systems, apply the required changes.

1. Create a launch.json file with the following content:
```
    {
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/run.py",
            "env": {
                // adjust pythonpath for local module 
                "PYTHONPATH": "${workspaceFolder}/app"
            },
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
    ENVIRONMENT=local
    VERSION=1.0                                                  
    MICROSERVICE_NAME=products
    MICROSERVICE_DESCRIPTION="The Products microservice is a self-contained service responsible for managing product data within a larger application. It provides functionalities to create, retrieve, update, and delete product information."                                                
    
    LOGGING_LEVEL=DEBUG
    DYNAMODB_TABLE=MCDE2023-d-products
    DYNAMODB_REGION=<your region> #eg eu-west-1

    AWS_ACCESS_KEY_ID=<your_aws_access_key>
    AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key>
    ```
4. Now you're ready to test the microservice. To do so, you can build and start the Docker container specified in the `Dockerfile` or, if you want to run it in your local machine environment, you can launch the `run_from_local.py`.

  - **Docker container**

    - Build the Docker Image
      ```
      docker build --build-arg PROJECT_ID=products -t productsimage .
      ```

    - Start the Docker Container
      ```
      docker run --env-file=.env.development -d --name productscontainer -p 8080:8080 productsimage
      ```

  
  - **If you want to test it locally**
    - In your active .venv run `aws configure` and insert your AWS keys
    - Set the environment variables with
      ```
      $env:ENVIRONMENT=local
      $env:PYTHONPATH=./app
      ```
    - Start "run_from_local.py" (it uses the already created .env file in order to use custom environment variables) with `python run_from_local.py`

5. With your browser, go to `localhost:8080/docs`


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



### API Documentation
#TODO 
The code implements the [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification) interface description for HTTP APIs through the [FastAPI](https://fastapi.tiangolo.com/) framework to easily and automatically build them. It's possible to test the APIs through [Swagger](https://swagger.io/) very easily by going to `localhost:8080/docs`

#CONTINUE

#### Generate OpenAPI spec
The OpenAPI spec is generated as `openapi.yaml` through the dedicated python script `extract_openapi.py`. To generate the OpenAPI spec, please, run in your active virtual environment the following commands:
```
$env:ENVIRONMENT=local
$env:PYTHONPATH=./app
python extract_openapi.py
```