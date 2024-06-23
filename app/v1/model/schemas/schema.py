from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict

from v1.utils.api_metadata import CREATE_PRODUCT, DELETE_PRODUCT, PUT_PRODUCT

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
    updated_at: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",           # Forbid additional generic key-value pairs in support
        json_schema_extra={
            "examples": [PUT_PRODUCT.input.example]
        }
    )

class PutSchemaProductOut(BaseModel):
    ID: str
    updated_at: str
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",           # Forbid additional generic key-value pairs in support
        json_schema_extra={
            "examples": [PUT_PRODUCT.output.example]
        }
    )
    )

class DeleteSchemaProductOut(BaseModel):
    ID: str
    message: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",           # Forbid additional generic key-value pairs in support
        json_schema_extra={
            "examples": [DELETE_PRODUCT.output.example]
        }
    )