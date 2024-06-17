# Here you can define/import your db connection and return it to the caller
from v1.config import Settings, get_config
import boto3

_config: Settings = get_config()

class DynamoDBClient:
    def __init__(self):
        self.db = boto3.resource('dynamodb', region_name=_config.dynamodb_region)
        
 

def get_dynamodb_client() -> DynamoDBClient:
    return DynamoDBClient()