from fastapi import Depends
from typing import List, Optional
from v1.config.config import Settings, get_config
from v1.controller.base_service import BaseService
from v1.dao.products_dao.products_dao import ProductsDAO
from v1.model.schemas.schema import PostSchemaProductIn, PostSchemaProductOut, GetSchemaProductOut, GetSchemaProductOutByName, GetSchemaProductOutAll

_config: Settings = get_config()

class ProductsService(BaseService):
    def __init__(
            self,
            config: Settings = Depends(get_config),
            products_dao: ProductsDAO = Depends(),
    ) -> None:
        super().__init__(
            config=config,
        )
        self.products_dao = products_dao


    def create_product(self, product_in: PostSchemaProductIn) -> PostSchemaProductOut:
        self.logger.info(f"Initiating product creation")

        self.logger.debug(f"Product details: {product_in.model_dump()}")

        product = self.products_dao.create_product(product_in)
        self.logger.info(f"Support request created successfully. ID: {product.ID}")
        return product
    

    def get_products(self) -> List[GetSchemaProductOutAll]:
        products = self.products_dao.get_products()
        self.logger.info(f"{len(products)} products retrieved.")
        return products
    
    def get_product(self, ID:str) -> List[GetSchemaProductOut]:
        product = self.products_dao.get_product(ID)
        self.logger.info("product retrieved.")
        return product
    
    def get_product_byname(self, name:str) -> List[GetSchemaProductOutByName]:
        product = self.products_dao.get_product_byname(name)
        self.logger.info("product retrieved.")
        return product