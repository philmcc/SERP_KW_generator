
import boto3



def create_keyword_table():
 

    table = dynamodb.create_table(
        TableName='keywords2',
        KeySchema=[
            {
                'AttributeName': 'keyword',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'allintitle',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'volume',
                'AttributeType': 'N'
            },
 {
                'AttributeName': 'parent_keyword',
                'AttributeType': 'S'
            },
 {
                'AttributeName': 'processed',
                'AttributeType': 'N'
            },
 {
                'AttributeName': 'to_process',
                'AttributeType': 'N'
            },
 {
                'AttributeName': 'lastupdated',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
  
    return table


if __name__ == '__main__':

    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')


# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
    table = dynamodb.Table('keywords')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
    print(table.creation_date_time)

    keyword_table = create_keyword_table()
    print("Table status:", keyword_table.table_status)


#table.put_item(
    Item={
        'keyword': 'janedoe',
        'parent_keyword': 'Jane',
        'allintitle': {NULL:TRUE},
        'volume': {NULL:TRUE},
        'last_updated': -1,
        'processed': {"BOOL": FALSE},
        'toprocess': {"BOOL": FALSE},

    }
