from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict

from v1.utils.api_metadata import CREATE_PRODUCT

class PostSchemaProductIn(BaseModel):
    name:        str                        # Name of the product	
    description: str                        # Detailed description of the product	
    category_id: Optional[str] = None       # id for the category of the product
    brand_id:    Optional[str] = None       # id for the brand of the product
    price:       float                      # Price of the product
    weight:      Optional[float] = None     # Weight of the product

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",           # Forbid additional generic key-value pairs in support
        json_schema_extra={
            "examples": [CREATE_PRODUCT.input.example]
        }
    )

class PostSchemaProductOut(BaseModel):
    product_id:  str                        # Unique identifier for the product
    created_at:  datetime                   # Date and time the product was created

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",           # Forbid additional generic key-value pairs in support
        json_schema_extra={
            "examples": [CREATE_PRODUCT.output.example]
        }
    )

class PutSchemaProductIn(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    brand_id: Optional[str] = None
    price: Optional[float] = None
    weight: Optional[float] = None
    cover_url: Optional[str] = None

    class Config:
        from_attributes=True
        extra = "forbid"

class PutSchemaProductOut(BaseModel):
    ID: str
    updated_at: datetime
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    brand_id: Optional[str] = None
    price: Optional[float] = None
    weight: Optional[float] = None
    cover_url: Optional[str] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        json_schema_extra = {
            "examples": [{
                "ID": "1caff255-ef44-4066-a7a3-884c81c34ecf",
                "updated_at": "2024-06-18T17:40:00Z",
                "name": "Product Name",
                "description": "Product Description",
                "category_id": "cat12345",
                "brand_id": "brand67890",
                "price": 99.99,
                "weight": 1.5,
                "cover_url": "http://example.com/image.jpg"
            }]
        }
    )

class DeleteSchemaProductOut(BaseModel):
    ID: str
    message: Optional[str] = None
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [{
                "ID": "1caff255-ef44-4066-a7a3-884c81c34ecf",
                "message": "Product with ID '1caff255-ef44-4066-a7a3-884c81c34ecf' has been deleted"
            }]
        }
    )