"""
Local development configuration for DynamoDB
"""
import boto3
import os

def setup_local_dynamodb():
    """Setup local DynamoDB configuration"""
    
    # Check if running locally
    if os.getenv('AWS_SAM_LOCAL') or os.getenv('LOCAL_DEV'):
        # Use DynamoDB Local
        return boto3.resource('dynamodb', 
                            endpoint_url='http://localhost:8000',
                            region_name='us-east-1',
                            aws_access_key_id='dummy',
                            aws_secret_access_key='dummy')
    else:
        # Use AWS DynamoDB
        return boto3.resource('dynamodb')

def create_local_tables():
    """Create tables for local development"""
    dynamodb = setup_local_dynamodb()
    
    # Create agent interactions table
    try:
        table = dynamodb.create_table(
            TableName='AgentInteractions',
            KeySchema=[
                {'AttributeName': 'session_id', 'KeyType': 'HASH'},
                {'AttributeName': 'message_id', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'session_id', 'AttributeType': 'S'},
                {'AttributeName': 'message_id', 'AttributeType': 'N'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print("Created AgentInteractions table")
    except Exception as e:
        print(f"Table might already exist: {e}")