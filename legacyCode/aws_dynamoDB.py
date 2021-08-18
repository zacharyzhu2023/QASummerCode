# Test out functionality of dynamoDB
import boto3
from boto3.dynamodb.conditions import Key, Attr # Allow for conditions to be added when querying + scanning

# Client + Resource instances
ddb = boto3.resource('dynamodb') # Create a service resource
client = boto3.client('dynamodb') # Create a client instance


# Helper method to print attributes of a given entry
def printAttributes(table, username, lastname):
	return table.get_item(
		Key = { # Can fetch an item based off of its combined partition + sort key (since here we don't necessarily have a unique partition)
			'username': username,
			'last_name': lastname
		}
	)['Item']

# Helper method to add entries to a given table
def addEntry(tableName, username, firstname, lastname, age, accounttype):
	client.put_item(
	TableName = tableName,
	Item = {
			'username': {'S': username}, # Need to specify the data type in addition to the actual entry
			'first_name': {'S': firstname},
			'last_name': {'S': lastname},
			'age': {'N': str(age)}, # Note: when adding a numeric type, still need to add as a string, but operations will occur w/ arithmetic behind the hood
			'account_type': {'S': accounttype}
	}
)

# Helper method to create a dictionary correctly formatted consistent w/ the table for a batch
def createBatch(n = 1): # Default size of items is 1
	items = []
	for i in range(n):
		Item = {
			'username': 'batch_user' + str(i),
			'first_name': 'Zach_Clone' + str(i),
			'last_name': 'Zhu',
			'age': 20,
			'account_type': 'clone_account',
			'residence': # Testing the nested structure
				{
					'city': 'San Diego',
					'state': 'CA'
				}
		}
		items.append(Item)
	return items


# Creating a sample table
try: # Create the table if it doesn't exist
	table = ddb.create_table(
		TableName = 'users', # Name of the table that will be created
		# This determines the attributes that constitute the primary key: HASH-partition key, RANGE-sort key
		KeySchema = [
			{
				'AttributeName': 'username',
				'KeyType': 'HASH'
			},
			{
				'AttributeName': 'last_name',
				'KeyType': 'RANGE'
			}
		],
		# Describes all the attributes and the corresponding data type that they are: S-String, N-number, B-binary
		AttributeDefinitions = [
			{
				'AttributeName': 'username',
				'AttributeType': 'S'
			},
			{
				'AttributeName': 'last_name',
				'AttributeType': 'S'
			},
		],
		# Provide throughput settings for a given table
		ProvisionedThroughput = {
			'ReadCapacityUnits': 5, # Allowed 5 consistent reads/second
			'WriteCapacityUnits': 5 # Allowed 5 consistent writes/second
			}
		)
except Exception as e:
	table = ddb.Table('users') # Reference an existing table
table.meta.client.get_waiter('table_exists').wait(TableName = 'users') # Ensure that table exists


# Get preliminary info about the table
print('num entries:', table.item_count) # Find number of entries in the table
print('Creation Date:', table.creation_date_time) # Get the time of creation

# Adding a new item to the existing table
table.put_item(
		Item = {
			'username': 'user1',
			'first_name': 'Zachary',
			'last_name': 'Zhu',
			'age': 19,
			'account_type': 'standard_user'
		}
	)

# Alternate way of adding an item--using client instance instead of the table itself
client.put_item(
	TableName = 'users',
	Item = {
			'username': {'S':'user2'}, # Need to specify the data type in addition to the actual entry
			'first_name': {'S':'Zachie'},
			'last_name': {'S':'Zhu'},
			'age': {'N': '22'}, # Note: when adding a numeric type, still need to add as a string, but operations will occur w/ arithmetic behind the hood
			'account_type': {'S':'alt_user'}
	}
)

# Get an item from a table
response = table.get_item(
	Key = { # Can fetch an item based off of its combined partition + sort key (since here we don't necessarily have a unique partition)
		'username': 'user1',
		'last_name': 'Zhu'
	}
)
item = response['Item'] # Uses the fact that the response contains a dictionary of item--which contains entry info, consumedcapacity, index info, etc.
print('One entry info:', item) # Print the entry info

# Update an item within the table
# Additional note: can't use update_item to modify primary key attributes; rather, need to delete + add a new item
table.update_item(
	Key = { # Again, need to specify identifiers to get the right entry from the table
		'username': 'user2',
		'last_name': 'Zhu'
	},
	UpdateExpression = 'SET age = :val1', # Can specify whether we want to set (change or create new attribute), remove (get rid of attributes), or add attributes
	ExpressionAttributeValues = {
		':val1': 16 # We created a reference to age as val1--> access + modify it with ExpressionAttributeValues
	}
)
print('new vals of user2:', printAttributes(table, 'user2', 'Zhu'))

# Try a modified update
table.update_item(
	Key = { # Again, need to specify identifiers to get the right entry from the table
		'username': 'user2',
		'last_name': 'Zhu'
	},
	UpdateExpression = 'REMOVE age SET newAttr = :val1, first_name = :val2', # Can specify whether we want to set (change or create new attribute), remove (get rid of attributes), or add attributes
	ExpressionAttributeValues = {
		':val1': 'whateverwewant',
		':val2': 'Mike'
	}
)
print('vals of user1:', printAttributes(table, 'user1', 'Zhu'))
print('new vals of user2:', printAttributes(table, 'user2', 'Zhu'))


# Adding more entries to our table
addEntry('users', 'user3', 'Megan', 'Gantz', 35, 'alt_user')
addEntry('users', 'user4', 'Morgan', 'Freeman', 80, 'alt_user')
addEntry('users', 'user1', 'ZZ', 'Zhang', 4, 'standard_user')
addEntry('users', 'user1', 'ZZ', 'Zhuang', 4, 'standard_user')
addEntry('users', 'user1', 'ZZ', 'Zeng', 4, 'standard_user')
addEntry('users', 'user6', 'ZZ', 'Zhang', 18, 'standard_user')

# Delete an entry
numEntriesPreDelete = table.item_count # NOTE: this gets updated every 6 hours--may not immediately get reflected; is there a way to access this more quickly?
table.delete_item(
	Key = { # Give identifier for what to delete
		'username': 'user1',
		'last_name': 'Zhang'
	}
	)
numEntriesPostDelete = table.item_count
print('prev item count:', numEntriesPreDelete, 'new item count:', numEntriesPostDelete)
print('all our tables:', client.list_tables()['TableNames']) # Get all the table names associated with a given client

# Batch Add Operations--would allow for fewer write requests

with table.batch_writer() as batch: # Reference the table + indicate we want to write multiple items to the table @ the same time (limit: 50)
	batchToAdd = createBatch(5) # Create 5 new entries to add
	#print(batchToAdd)
	for item in batchToAdd: # Integrate each of the items from the batch into the table
		batch.put_item(item)


# Query + Scan

# Get all the entries where username is uniformly user1
userOnes = table.query(
	KeyConditionExpression = Key('username').eq('user1')
)['Items']
print('\n\nuser1s:\n')
for user1 in userOnes:
	print(user1)

# NOTE: syntax when working with non-key col's is slightly different--retain only entries with zhu
zhuFamily = table.scan( # Use scan when not working with the HASH key
	FilterExpression = Attr('last_name').eq('Zhu')
)['Items']
print('\n\nzhufamily:\n')
for zhu in zhuFamily:
	print(zhu)

# Building a more complex scan query
# What if we only wanted to retain the old (< 18 years old) or those whose last name is not Zhu

complexSubset = table.scan(
	FilterExpression = ~Attr('last_name').eq('Zhu') | Attr('age').lt(18)
)['Items']

print('\n\nComplex Subset:\n')
for item in complexSubset:
	print(item)




























