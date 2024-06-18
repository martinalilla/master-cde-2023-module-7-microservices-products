# Here you can define/import your db connection and return it to the caller
import boto3.session
from v1.config import Settings, get_config
import boto3
from mypy_boto3_dynamodb import ServiceResource

_config: Settings = get_config()

class DynamoDBClient:
    def __init__(self):
        self.db: ServiceResource = boto3.resource('dynamodb', region_name=_config.dynamodb_region)
        self.table = self.db.Table(_config.dynamodb_table)
        
 

def get_dynamodb_client() -> DynamoDBClient:
    return DynamoDBClient()