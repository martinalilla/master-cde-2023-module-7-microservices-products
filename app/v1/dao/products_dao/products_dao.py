from fastapi import Depends
from v1.config.config import Settings, get_config
from v1.model.repository.products_repository.products_repository import ProductsRepository
from v1.model.repository.repository import get_repository
from v1.model.schemas.schema import PostSchemaProductIn, PostSchemaProductOut, PutSchemaProductOut, PutSchemaProductIn, DeleteSchemaProductOut
from v1.utils.exception import HttpCustomException, custom_exception_handler
from datetime import datetime
from v1.model.database import get_dynamodb_client

import logging
import uuid
from typing import TypeVar, Generic
from pydantic import BaseModel

_config: Settings = get_config()
T = TypeVar('T', bound=BaseModel)
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
            ID = str(uuid.uuid4())
            created_at = datetime.now()

            product = PostSchemaProductIn(
                **product_in.model_dump(),
                created_at=created_at
            )
            self.repository.create_product(ID, product)
            logger.debug(f"Created product (ID: {ID})")
        
            return PostSchemaProductOut(
                product_id=ID,
                created_at=created_at
            )
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred creating product")
    #=================UPDATE  & DELETE FUNCTIONS=====================

    def update_product(self, ID: str,data: PutSchemaProductIn)->dict:
        logger.info(f"Updating product with ID: {ID}")
        try:
            self.repository._update(ID, data)
            logger.info(f"Product with ID: {ID} updated successfully")
        except Exception as e:
            logger.error(f"Failed to update product with ID: {ID}: {str(e)}")
            raise

    def delete_product(self, ID: str):
        try:
            self.repository.delete_product(ID)
            logger.debug(f"Product deleted with ID {ID}")
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred deleting product")
