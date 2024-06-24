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
            response = self.dynamodb_client.table.get_item(Key={'ID': ID})
            item = response.get('Item')

            if item is None:
                logger.info(f"No document found for product with ID {ID}")
                raise HttpCustomException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product doesn't exist with this {ID}",
                    internal_detail=f"Provided ID {ID} is invalid"
                )

            logger.debug(f"Document retrieved successfully for product with ID {ID}")
            return item

        except HttpCustomException:
            raise
        except Exception as e:
            exception_handler.handle_custom_exception(f"An unexpected error occurred retrieving a product (ID: {ID})")


    def _get_all(self):
        try:     
            data_db = self.dynamodb_client.table.scan()
            items = data_db.get('Items')
            if(len(data_db) > 0):
                logger.debug(f"Retrieved {len(data_db)} documents.")
                return items
            return None
        
        except HttpCustomException:
            raise
        except Exception:
            exception_handler.handle_custom_exception(f"Unexpected error retrieving data")

    
    def _get_byname(self, name: str):
        try:
            response = self.dynamodb_client.table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('name').eq(name))
            item = response.get('Items')[0]

            if item is None:
                logger.info(f"No document found for product with name {name}")
                raise HttpCustomException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product doesn't exist with this name: {name}",
                    internal_detail=f"Provided name {name} is invalid"
                )

            logger.debug(f"Document retrieved successfully for product with name {name}")
            return item

        except HttpCustomException:
            raise
        except Exception as e:
            exception_handler.handle_custom_exception(f"An unexpected error occurred retrieving a product (name: {name})")


    def _update(self, id: str, data: Generic[T]):
        logger.info(f"Updating a document in DynamoDB (ID: {id})")
        try:
            self._get(id) # Check if item exists
            # Convert data to a dictionary and handle float to Decimal conversion
            data_dict = data.model_dump(exclude_none=True)
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

    def _delete(self, id: str):
        logger.info(f"Deleting a document in DynamoDB (ID: {id})")
        try:
            self._get(id) # Check if item exists
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