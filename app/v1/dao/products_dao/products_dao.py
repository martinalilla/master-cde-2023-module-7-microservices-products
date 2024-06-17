from fastapi import Depends
from v1.config.config import Settings, get_config
from v1.model.repository.products_repository.products_repository import ProductsRepository
from v1.model.repository.repository import get_repository
from v1.model.schemas.schema import PostSchemaProductIn, PostSchemaProductOut, UpdateSchemaProductIn
from v1.utils.exception import HttpCustomException, custom_exception_handler
from datetime import datetime
import logging
import uuid

_config: Settings = get_config()
logger: logging.Logger = logging.getLogger(_config.service_name)
exception_handler = custom_exception_handler()

class ProductsDAO:
    def __init__(
            self,
            repository: ProductsRepository = Depends(get_repository)
    ):
        self.repository = repository


    def create_product(self, product_in: PostSchemaProductIn) -> PostSchemaProductOut:
        logger.info("Creates a new product for a user")
        try:
            product_id = str(uuid.uuid4())
            created_at = datetime.now()

            product = PostSchemaProductIn(
                **product_in.model_dump(),
                created_at=created_at
            )
            self.repository.create_product(product_id, product)
            logger.debug(f"Created product (ID: {product_id})")
        
            return PostSchemaProductOut(
                product_id=product_id,
                created_at=created_at
            )
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred creating product")
    #=================UPDATE  & DELETE FUNCTIONS=====================
    def update_product(self, product_id: str, product_in: UpdateSchemaProductIn) -> PostSchemaProductOut:
        logger.info(f"Updating product with ID: {product_id}")
        try:
            updated_product = self.repository.update_product(product_id, product_in)
            return PostSchemaProductOut(
                product_id=product_id,
                created_at=updated_product.created_at  
            )
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred updating product with ID: {product_id}")

    def delete_product(self, product_id: str) -> bool:
        logger.info(f"Deleting product with ID: {product_id}")
        try:
            success = self.repository.delete_product(product_id)
            return success
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred deleting product with ID: {product_id}")