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
import boto3

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
            self.table.put_item(data) #TODO add typing
            logger.debug(f"Created document (ID: {id})")
            return
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred creating document (ID: {id})")


    def _update(self, id: str, data: Generic[T]):
        logger.info(f"Updating a document in DynamoDB (ID: {id})")
        try:
            # Update the item in the table
            update_expression = "SET " + ", ".join(f"{k}=:{k}" for k in data.dict().keys())
            expression_attribute_values = {f":{k}": v for k, v in data.dict().items()}

            self.dynamodb_client.table.update_item(
            Key={'ID': id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
            )
            logger.debug(f"Updated document (ID: {id})")
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred updating document (ID: {id})")


    def _delete(self, id: str):
        logger.info(f"Deleting a document in DynamoDB (ID: {id})")
        try:
            self.dynamodb_client.table.delete_item(Key={'ID': id})
            logger.debug(f"Deleted document (ID: {id})")
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred deleting document (ID: {id})")

def get_repository() -> Repository:
    return Repository()