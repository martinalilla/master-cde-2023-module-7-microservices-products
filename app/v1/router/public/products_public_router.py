from fastapi import APIRouter, Body, Depends, Query
from starlette import status
from typing import Annotated, List, Optional, Union

from v1.config.config import Settings, get_config
from v1.controller.products_service.products_service import ProductsService
from v1.model.schemas.schema import PostSchemaProductIn, PostSchemaProductOut, GetSchemaProductOut
from v1.utils.api_metadata import CREATE_PRODUCT, GET_PRODUCT

router = APIRouter()

@router.post("/products", status_code=status.HTTP_201_CREATED,  responses=CREATE_PRODUCT.responses,
            summary=CREATE_PRODUCT.summary, description=CREATE_PRODUCT.description,
            operation_id=CREATE_PRODUCT.operationId, tags=['Product'])
def post(
        data: PostSchemaProductIn = Body(...,
        title=CREATE_PRODUCT.input.title, description=CREATE_PRODUCT.input.description),
        products_service: ProductsService = Depends()
) -> PostSchemaProductOut:
    return products_service.create_product(data)



@router.get("/products", responses=GET_PRODUCT.responses, summary=GET_PRODUCT.summary,
      description=GET_PRODUCT.description, operation_id=GET_PRODUCT.operationId, tags=['products'])
def get_products(
    products_service: ProductsService = Depends()
) -> List[GetSchemaProductOut]:
        return products_service.get_products()


