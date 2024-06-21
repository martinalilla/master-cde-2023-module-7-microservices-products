from fastapi import Depends, HTTPException
from v1.config.config import Settings, get_config
from v1.controller.base_service import BaseService
from v1.dao.products_dao.products_dao import ProductsDAO
from v1.model.schemas.schema import PostSchemaProductIn, PostSchemaProductOut, PutSchemaProductOut, PutSchemaProductIn, DeleteSchemaProductOut
from datetime import datetime

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
        self.logger.info(f"Product created successfully. ID: {product.ID}")
        return product
    #=================UPDATE  & DELETE FUNCTIONS=====================
    def update_product(self, ID: str, data: PutSchemaProductIn) -> PutSchemaProductOut:
        self.logger.info(f"Updating product with ID {ID}")
        updated_at = datetime.now()
        self.products_dao.update_product(ID, data)
        self.logger.info(f"Product with ID {ID} updated")
        return PutSchemaProductOut(ID=ID, updated_at=updated_at)

    def delete_product(self, ID: str) -> DeleteSchemaProductOut:
        self.logger.info(f"Deleting product with ID {ID}")
        self.products_dao.delete_product(ID)
        self.logger.info(f"Product with ID {ID} deleted")
        return DeleteSchemaProductOut(ID=ID, message=f"Product with ID '{ID}' has been deleted")