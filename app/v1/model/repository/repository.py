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
            # Convert data to a dictionary and handle float to Decimal conversion
            data_dict = data.dict()
            for key, value in data_dict.items():
                if isinstance(value, float):
                    data_dict[key] = Decimal(str(value))

            # Generate the update expression and attribute maps
            update_expression = "SET " + ", ".join(f"#{k}=:{k}" for k in data_dict.keys())
            expression_attribute_names = {f"#{k}": k for k in data_dict.keys()}
            expression_attribute_values = {f":{k}": v for k, v in data_dict.items()}

            # Update the item in the table
            self.dynamodb_client.table.update_item(
                Key={'ID': id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values
            )
            logger.debug(f"Updated document (ID: {id})")
        except HttpCustomException:
            raise
        except Exception as e:
            exception_handler.handle_custom_exception(f"An error occurred updating document (ID: {id})")
            logger.exception(e)

    def _delete(self, id: str):
        logger.info(f"Deleting a document in DynamoDB (ID: {id})")
        try:
            self.dynamodb_client.table.delete_item(Key={'ID': id})
            logger.debug(f"Deleted document (ID: {id})")
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"An error occurred deleting document (ID: {id})")
    
    def delete_product(self, id: str):
        return self._delete(id)
def get_repository() -> Repository:
    return Repository()