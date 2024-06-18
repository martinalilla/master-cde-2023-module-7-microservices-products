import logging
from typing import TypeVar, List, Generic, Optional
from fastapi.encoders import jsonable_encoder
from v1.config.config import Settings, get_config
from v1.model.database import get_dynamodb_client
from v1.utils.exception import HttpCustomException, custom_exception_handler
import json
from decimal import Decimal
from pydantic import BaseModel
from starlette import status

T = TypeVar('T')


_config: Settings = get_config()
logger: logging.Logger = logging.getLogger(_config.service_name)
exception_handler = custom_exception_handler()

class Condition(BaseModel):
    field: Optional[str] = None,
    operator: Optional[str] = None,
    value: Optional[str | List[str]] = None

class Repository:
    def __init__(
            self,
            collection_name: str = None,
            subcollection_name: str = None
    ):
        self.dynamodb_client = get_dynamodb_client()
        self.collection_name = collection_name
        self.subcollection_name = subcollection_name


    def _create(self, id: str, data: Generic[T]):
        logger.info("Creates a document in DynamoDB")
        try:
            self.dynamodb_client.table.put_item(TableName=_config.dynamodb_table,
                                                Item=json.loads(json.dumps(data.model_dump()), parse_float=Decimal))
            logger.debug(f"Created document (ID: {id})")
            return
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred creating document (ID: {id})")

    def _get(self, ID: str):
        try:     
            data_db = self.dynamodb_client.table.get_item(Key={'ID': ID})
            if not data_db.exists:
                raise HttpCustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document doesn't exist",
                internal_detail=f"Provided ID is invalid"
                )

            logger.debug(f"Document retrieved successfully for product with ID {ID}")
            return data_db
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An unexpected error occurred retrieving a product (ID: {ID})")


    def _get_all(self):
        try:     
            data_db = self.dynamodb_client.table.scan()
            if(len(data_db) > 0):
                logger.debug(f"Retrieved {len(data_db)} documents.")
                return data_db
            return None
        
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"Unexpected error retrieving data")


def get_repository() -> Repository:
    return Repository()