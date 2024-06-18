import logging
from typing import TypeVar, List, Generic
from fastapi.encoders import jsonable_encoder
from v1.config.config import Settings, get_config
from v1.model.database import get_dynamodb_client
from v1.utils.exception import HttpCustomException, custom_exception_handler
import json
from decimal import Decimal
T = TypeVar('T')


_config: Settings = get_config()
logger: logging.Logger = logging.getLogger(_config.service_name)
exception_handler = custom_exception_handler()

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


def get_repository() -> Repository:
    return Repository()