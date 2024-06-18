import logging
import uuid
from fastapi import Depends
from v1.config.config import Settings, get_config
from v1.model.db_schemas.db_schema import Product
from v1.model.repository.products_repository.products_repository import ProductsRepository
from v1.model.repository.products_repository.products_repository import get_repository
from v1.model.schemas.schema import PostSchemaProductIn, PostSchemaProductOut, GetSchemaProductOut
from v1.utils.exception import HttpCustomException, custom_exception_handler
from datetime import datetime
from typing import List, Optional

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

    def get_products(self, limit: int, last_product_id: Optional[str] = None, product_type: Optional[List[str]] = None, product_category: Optional[List[str]] = None) -> List[GetSchemaProductOut]:
        try:
            products = self.repository.get_products(limit, last_product_id, product_type, product_category)
            logger.debug(f"Successfully retrieved {len(products)} products.")  
            return products
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"Unexpected error retrieving products")