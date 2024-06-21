# Products microservice
This repository goal is to provide the ready to use code for the products microservice, with the necessary instructions to test it.
The code implements the four basic REST APIs (GET, POST, PUT, DELETE), with their related endpoints, that are designed and configured to communicate with DynamoDB.

The code is written in Python, it implements the [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification) interface description for HTTP APIs through the [FastAPI](https://fastapi.tiangolo.com/) framework to easily and automatically build them. It's possible to test the APIs through [Swagger](https://swagger.io/) very easily by going to `localhost:8080/docs`; Moreover, the code includes a dedicated logging system through the dedicated python library `logging` appropriately configured.

All the code is designed to run in a simple Docker container (see the _Dockerfile_), to maintain all the advantages of the microservices architecture, run in a lightweight isolated environment (so other microservices can be added following this architecture) in order to decouple the microservice, and to easily allow its scalability thanks to the cloud architecture.
Since the code is designed to work correctly with the Docker container, it's better to test it _as is_ with the provided image in ECR [inserire link]() with the provided AWS infrastructure, but, if you want, you can test it in your local machine by following the _local execution_ steps below (please, remember that you can encounter errors due to your different environment).

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

## Prerequisites
In order to run this code, you must satisfy these prerequisites:
- Have an AWS account with both access and secret keys.
- Have access to AWS DynamoDB and ECR
- Have Docker installed (needed to push the image to ECR)
- Have installed the [AWS-CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) (only if you want to test in local)


### Software Management Approach

The chosen software management approach consists in two kind of branches: __Feature branches__ and __Production branch__ with code versioning.

The _Feature Branching_ approach is used to implement the new features (i.e. the POST, GET, PUT, DELETE APIs + docs) in order to allow the developers to work in isolation each others (after assigned the activities to each of them); once the feature is complete, it is merged back into one of the _development_ branch, in order to test it with the provided development infrastructure. 

When the tests have been completed successfully, the __development__ branch is merged to the __production__ branch, where the code is live in the production cloud infrastructure. 
If something goes wrong with the dedicated tests, a new branch is opened to fix the problem asap.

Of course, all the changes are reviewed by Pull Requests before the merging operation to the _production_ and _development_ branches.
This approach ensures simple and efficient CI/CD operations, with independent and rapid development of each feature.

Finally, to maintain the code versioning, the __Release branching__ approach has been implemented, i.e. there is a branch for each version to prepare for a new production release (of course the _production_ branch is always the one with the code implemented in the production cloud environment). So, each version has its _features_ and _development_ branches, and when the new release _development_ branch is ready to go in production, it is merged with the _production_ branch as explained before [aggiungere versioning sulla repo]()

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



### Generate OpenAPI spec
To generate the OpenAPI spec, please, run in your active virtual environment the following commands:
```
$env:ENVIRONMENT=local
$env:PYTHONPATH=./app
python extract_openapi.py
```