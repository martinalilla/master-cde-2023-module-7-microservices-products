from fastapi import APIRouter, Depends, HTTPException
from v1.config.config import Settings, get_config
from v1.controller.products_service import ProductsService
from v1.model.schemas.schema import PostSchemaProductIn, PostSchemaProductOut, UpdateSchemaProductIn

router = APIRouter()
_config: Settings = get_config()

@router.post("/products", response_model=PostSchemaProductOut)
def create_product(product_in: PostSchemaProductIn, service: ProductsService = Depends()):
    return service.create_product(product_in)

@router.put("/products/{id}", response_model=PostSchemaProductOut)
def update_product(id: str, product_in: UpdateSchemaProductIn, service: ProductsService = Depends()):
    return service.update_product(id, product_in)

@router.delete("/products/{id}")
def delete_product(id: str, service: ProductsService = Depends()):
    service.delete_product(id)
    return {"message": "Product deleted successfully"}
