from fastapi import Depends
from v1.config.config import Settings, get_config
from v1.model.db_schemas.db_schema import Product
from v1.model.repository.products_repository.products_repository import ProductsRepository
from v1.model.schemas.schema import PostSchemaProductIn, PostSchemaProductOut, PutSchemaProductOut, PutSchemaProductIn, DeleteSchemaProductOut, GetSchemaProductOut
from v1.utils.exception import HttpCustomException, custom_exception_handler
from datetime import datetime

import logging
import uuid
from typing import TypeVar, Generic
from pydantic import BaseModel
from v1.model.repository.products_repository.products_repository import get_repository
from typing import List

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
            created_at = datetime.now().isoformat()

            product = Product(
                **product_in.model_dump(),
                ID=ID,
                created_at=created_at
            )
            self.repository.create_product(ID, product)
            logger.debug(f"Created product (ID: {ID})")
        
            return PostSchemaProductOut(
                ID=ID,
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
            exception_handler.handle_custom_exception(f"Failed to update product with ID: {ID}")

    def delete_product(self, ID: str):
        try:
            self.repository.delete_product(ID)
            logger.debug(f"Product deleted with ID {ID}")
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred deleting product")

    def get_products(self) -> List[GetSchemaProductOut]:
        try:
            products = self.repository.get_products()
            logger.debug(f"Successfully retrieved {len(products)} products.")  
            return products
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"Unexpected error retrieving products")

    def get_product(self, ID:str) -> List[GetSchemaProductOut]:
        try:
            product = self.repository.get_product(ID)
            logger.debug(f"Successfully retrieved product with the ID: {ID}.")  
            return product
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"Unexpected error retrieving the product")

    def get_product_byname(self, name:str) -> List[GetSchemaProductOut]:
        try:
            product = self.repository.get_product_byname(name)
            logger.debug(f"Successfully retrieved product with the name: {name}.")  
            return product
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"Unexpected error retrieving the product")
