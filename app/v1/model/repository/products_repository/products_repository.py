import logging
from v1.config.config import Settings, get_config
from v1.model.db_schemas.db_schema import ProductEssential
from v1.model.repository.repository import Repository
from v1.model.db_schemas.db_schema import ProductEssential, UpdateSchemaProductIn
from v1.utils.exception import HttpCustomException, custom_exception_handler

_config: Settings = get_config()
logger: logging.Logger = logging.getLogger(_config.service_name)
exception_handler = custom_exception_handler()

class ProductsRepository(Repository):
    def __init__(
            self,
            collection_name: str = 'users',
            subcollection_name: str = 'products'
    ) -> None:
        super().__init__(
            collection_name = collection_name,
            subcollection_name = subcollection_name,
        )

    def create_product(self, product_id: str, data: ProductEssential):
        logger.info("Creates a Product document in Firestore")
        try:
            self._create(product_id, data)
            logger.debug(f"Created product document (ID: {product_id})")
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred creating product document (ID: {product_id})")
    #=================UPDATE  & DELETE FUNCTIONS=====================


    def update_product(self, product_id: str, data: UpdateSchemaProductIn) -> ProductEssential:
        logger.info(f"Updating Product document (ID: {product_id}) in Firestore")
        try:
            # Fetch the current product data
            existing_product = self._get_by_id(product_id)
            if not existing_product:
                raise HttpCustomException(status_code=404, detail="Product not found")

            # Merge the existing product data with the updates
            updated_data = existing_product.copy(update=data.dict(exclude_unset=True))
            self._update(product_id, updated_data)
            logger.debug(f"Updated product document (ID: {product_id})")
            return updated_data
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred updating product document (ID: {product_id})")

    def delete_product(self, product_id: str) -> bool:
        logger.info(f"Deleting Product document (ID: {product_id}) in Firestore")
        try:
            success = self._delete(product_id)
            if not success:
                raise HttpCustomException(status_code=404, detail="Product not found")

            logger.debug(f"Deleted product document (ID: {product_id})")
            return True
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred deleting product document (ID: {product_id})")