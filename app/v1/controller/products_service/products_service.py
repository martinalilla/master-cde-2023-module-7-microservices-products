from fastapi import Depends, HTTPException
from v1.config.config import Settings, get_config
from v1.controller.base_service import BaseService
from v1.dao.products_dao.products_dao import ProductsDAO
from v1.model.schemas.schema import PostSchemaProductIn, PostSchemaProductOut, UpdateSchemaProductIn

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
        self.logger.info(f"Product created successfully. ID: {product.product_id}")
        return product
    #=================UPDATE  & DELETE FUNCTIONS=====================
    def update_product(self, product_id: str, product_in: UpdateSchemaProductIn) -> PostSchemaProductOut:
        self.logger.info(f"Updating product with ID: {product_id}")

        updated_product = self.products_dao.update_product(product_id, product_in)
        if not updated_product:
            self.logger.error(f"Product with ID {product_id} not found.")
            raise HTTPException(status_code=404, detail="Product not found")

        self.logger.info(f"Product with ID: {product_id} updated successfully")
        return updated_product

    def delete_product(self, product_id: str) -> None:
        self.logger.info(f"Deleting product with ID: {product_id}")

        success = self.products_dao.delete_product(product_id)
        if not success:
            self.logger.error(f"Product with ID {product_id} not found.")
            raise HTTPException(status_code=404, detail="Product not found")

        self.logger.info(f"Product with ID: {product_id} deleted successfully")