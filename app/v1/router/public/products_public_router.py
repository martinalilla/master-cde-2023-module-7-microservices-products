from fastapi import APIRouter, Body, Depends
from starlette import status
from typing import List

from v1.controller.products_service.products_service import ProductsService
from v1.model.schemas.schema import PostSchemaProductIn, PostSchemaProductOut, GetSchemaProductOut
from v1.utils.api_metadata import CREATE_PRODUCT, GET_PRODUCT, GET_ALL, GET_PRODUCT_BY_NAME

router = APIRouter()

@router.post("/products", status_code=status.HTTP_201_CREATED,  responses=CREATE_PRODUCT.responses,
            summary=CREATE_PRODUCT.summary, description=CREATE_PRODUCT.description,
            operation_id=CREATE_PRODUCT.operationId, tags=['Post'])
def post(
        data: PostSchemaProductIn = Body(...,
        title=CREATE_PRODUCT.input.title, description=CREATE_PRODUCT.input.description),
        products_service: ProductsService = Depends()
) -> PostSchemaProductOut:
    return products_service.create_product(data)



@router.get("/products", responses=GET_ALL.responses, summary=GET_ALL.summary,
      description=GET_ALL.description, operation_id='get all the product', tags=['Get'])
def get_products(
    products_service: ProductsService = Depends()
) -> List[GetSchemaProductOut]:
        return products_service.get_products()


@router.get("/products/id/{product_id}", responses=GET_PRODUCT.responses, summary=GET_PRODUCT.summary, 
            description=GET_PRODUCT.description, operation_id='get one product', tags=['Get'])
def get_product(
    product_id:str,
    products_service: ProductsService = Depends()) -> GetSchemaProductOut:
    return products_service.get_product(product_id)


@router.get("/products/name/{name}", responses=GET_PRODUCT_BY_NAME.responses, summary=GET_PRODUCT_BY_NAME.summary, 
            description=GET_PRODUCT_BY_NAME.description, operation_id='get one product by name', tags=['Get'])

def get_product_by_name(
    name:str,
    products_service: ProductsService = Depends()) -> GetSchemaProductOut:
    return products_service.get_product_byname(name)

