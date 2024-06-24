from typing import Optional

from pydantic import BaseModel
from v1.router.endpoint_responses import get_all_responses, delete_all_responses, post_responses, update_responses, get_one_responses

class Schema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    example: Optional[dict | list] = None

    class Config:
        frozen = True

class APIMetadata(BaseModel):
    summary: str
    description: str
    operationId: str
    responses: dict
    input: Optional[Schema] = None
    output: Optional[Schema] = None

    class Config:
        frozen = True

CREATE_PRODUCT = APIMetadata(
    summary="Create a new product",
    description="Creates a new product in the system",
    operationId="CREATE_PRODUCT",
    responses=post_responses, 
    input=Schema(
        title="Product Input",
        description="The product content",
    example={
            "name": "Amazing T-Shirt",
            "description": "This is a high-quality, comfortable T-Shirt",
            "category_id": "7e96755c-88a3-4f3d-9f59-4d3ab3b277ee",
            "brand_id": "1c1a8ef9-7dab-4397-b73a-5f9a4143c135",
            "price": 19.99,
            "weight": 0.25,
    }
    ),
    output=Schema(
        title="Product Created",
        description="The newly created product information",
        example={
            "ID": "1caff255-ef44-4066-a7a3-884c81c34ecf",
            "created_at": "2024-06-08T17:40:00Z",
        },
    ),
)


PUT_PRODUCT = APIMetadata(
    summary="Update a product",
    description="Updates the details of an existing product by its ID",
    operationId="PUT_PRODUCT",
    responses= update_responses,
 
    input=Schema(
        title="Product Details",
        description="The details to update for the product",
        example={
            "name": "Updated T-Shirt",
            "price": 29.99
        }
    ),
    output=Schema(
        title="Product Updated",
        description="Details of the updated product",
        example={
            "ID":"1caff255-ef44-4066-a7a3-884c81c34ecf",
            "updated_at": "2024-06-23T15:00:26Z"
        }
    )
)

DELETE_PRODUCT = APIMetadata(
    summary="Delete a product",
    description="Deletes a specific product by its ID",
    operationId="DELETE_PRODUCT",
    responses=delete_all_responses,
    input=Schema(
        title="Product ID",
        description="The ID of the product to delete",
        example={
            "ID": "1caff255-ef44-4066-a7a3-884c81c34ecf"
        }
    ),
    output=Schema(
        title="Product Deleted",
        description="Details of the deleted product",
        example={
            "ID": "1caff255-ef44-4066-a7a3-884c81c34ecf",
            "message": "Product correctly deleted"
        }
    )
)
GET_PRODUCT = APIMetadata(
    summary="Get product details",
    description="Retrieves the details of a specific product by its ID",
    operationId="GET_PRODUCT",
    responses=get_one_responses,
    output= Schema(
            title="Product Details",
            description="Details of the requested product",
            example={
                "ID": "1caff255-ef44-4066-a7a3-884c81c34ecf",
                "name": "Amazing T-Shirt",
                "description": "This is a high-quality, comfortable T-Shirt",
                "category_id": "7e96755c-88a3-4f3d-9f59-4d3ab3b277ee",
                "brand_id": "1c1a8ef9-7dab-4397-b73a-5f9a4143c135",
                "price": 19.99,
                "weight": 0.25,
                "created_at": "2024-06-08T17:40:00Z",
            }
        ),
    input=Schema(
        title="Product ID",
        description="The ID of the product to retrieve",
        example={
            "ID": "1caff255-ef44-4066-a7a3-884c81c34ecf"
        }
    )
)

GET_ALL = APIMetadata(
    summary="Get product details",
    description="Retrieves the details of all the products",
    operationId="GET_ALL_PRODUCTS",
    responses=get_one_responses,
    output= Schema(
            title="Product Details",
            description="Details of the requested product",
            example={
                "ID": "1caff255-ef44-4066-a7a3-884c81c34ecf",
                "name": "Amazing T-Shirt",
                "description": "This is a high-quality, comfortable T-Shirt",
                "category_id": "7e96755c-88a3-4f3d-9f59-4d3ab3b277ee",
                "brand_id": "1c1a8ef9-7dab-4397-b73a-5f9a4143c135",
                "price": 19.99,
                "weight": 0.25,
                "created_at": "2024-06-08T17:40:00Z",
            }
        )
)

GET_PRODUCT_BY_NAME = APIMetadata(
    summary="Get product details",
    description="Retrieves the details of just one product which matches with the requested name, since it is expected that products with the same name have the same characteristics",
    operationId="GET_PRODUCT_BY_NAME",
    responses=get_one_responses,
    output= Schema(
            title="Product Details",
            description="Details of the requested product",
            example={ 
                    "ID": "e814c821-c7e7-46b2-988c-c3ffa0dd51c5",
                    "name": "hat",
                    "description": "This is a high-quality, comfortable hat",
                    "category_id": "7e96755c-88a3-4f3d-9f59-4d3ab3b277ee",
                    "brand_id": "1c1a8ef9-7dab-4397-b73a-5f9a4143c135",
                    "price": 19.99,
                    "weight": 0.25,
                    "created_at": "2024-06-19T09:25:23.239317",
                    "updated_at": 'null',
                    "cover_url": 'null'  
            }
        ),
    input=Schema(
        title="Product name",
        description="The name of the product to retrieve",
        example={
            "name": "hat"
        }
    )
)
