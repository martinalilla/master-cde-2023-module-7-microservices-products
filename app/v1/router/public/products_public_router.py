from fastapi import APIRouter, Body, Depends
from starlette import status
from v1.model.schemas.schema import PostSchemaProductIn, PostSchemaProductOut, PutSchemaProductOut, PutSchemaProductIn, DeleteSchemaProductOut
from v1.controller.products_service.products_service import ProductsService
from v1.model.schemas.schema import PostSchemaProductIn, PostSchemaProductOut
from v1.utils.api_metadata import CREATE_PRODUCT, PUT_PRODUCT, DELETE_PRODUCT

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

@router.put("/products/id/{product_id}", responses=PUT_PRODUCT.responses, summary=PUT_PRODUCT.summary, 
            description=PUT_PRODUCT.description, operation_id='Update product by ID', tags=['Put'])
def update_product(
        product_id: str,
        data: PutSchemaProductIn = Body(..., title=PUT_PRODUCT.input.title, description=PUT_PRODUCT.input.description),
        products_service: ProductsService = Depends()
) -> PutSchemaProductOut:
    updated_product = products_service.update_product(product_id, data)
    return updated_product


@router.delete("/products/id/{product_id}", responses=DELETE_PRODUCT.responses, response_model_exclude_none=True, summary=DELETE_PRODUCT.summary, 
               description=DELETE_PRODUCT.description, operation_id='Delete product by ID', tags=['Delete'])
def delete(
        product_id: str,
        products_service: ProductsService = Depends()
) -> DeleteSchemaProductOut:
    response = products_service.delete_product(product_id)
    return response