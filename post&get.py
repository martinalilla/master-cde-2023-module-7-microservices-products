from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import boto3
from botocore.exceptions import ClientError

#aws configure
#console: https://891377298977.signin.aws.amazon.com/console
#username: MCDE2023_stream_products
#password: @!MCDE2023_stream_products

app = FastAPI()

# Initialize DynamoDB resource (no endpoint_url for AWS)
dynamodb = boto3.resource('dynamodb', region_name='YOUR_AWS_REGION')

# Define the Product model
class Product(BaseModel):
    name: str
    price: float
    description: str

# Initialize the DynamoDB table
table = dynamodb.Table('Products')

@app.post("/products", response_model=Product)
def add_product(product: Product):
    try:
        # Create a unique product ID
        product_id = str(len(products) + 1)
        # Add product to DynamoDB
        response = table.put_item(
            Item={
                'id': product_id,
                'name': product.name,
                'price': product.price,
                'description': product.description
            }
        )
        return product
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/products", response_model=List[Product])
def get_products():
    try:
        response = table.scan()
        return response.get('Items', [])
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))