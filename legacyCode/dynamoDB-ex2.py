import boto3
from boto3.dynamodb.conditions import Key, Attr # Allow for conditions to be added when querying + scanning
import datetime
import random



# Bread + Butter of dynamoDB
client = boto3.client('dynamodb') # Create a client instance
ddb = boto3.resource('dynamodb') # Create a resource instance

# Helper method to create a table if one doesn't already exist
def createTable(tableName):
	try:
		table = ddb.create_table(
			TableName = tableName, # Indicate that we want to log the QA data
			# This determines the attributes that constitute the primary key: HASH-partition key, RANGE-sort key
			KeySchema = [
				{
					'AttributeName': 'SerialNumber', # Each entry should have a unique serial #
					'KeyType': 'HASH'
				},
			],
			# Describes all the attributes and the corresponding data type that they are: S-String, N-number, B-binary
			AttributeDefinitions = [
				{
					'AttributeName': 'SerialNumber',
					'AttributeType': 'S'
				}
			],
			# Provide throughput settings for a given table
			ProvisionedThroughput = {
				'ReadCapacityUnits': 5, # Allowed 5 consistent reads/second
				'WriteCapacityUnits': 5 # Allowed 5 consistent writes/second
				}
			)
		table.meta.client.get_waiter('table_exists').wait(TableName = tableName) # Ensure that table exists
		print('Successfully created the table!')
	except client.exceptions.ResourceInUseException:
		print('Table with name ' + tableName + ' already exists')
		table = ddb.Table(tableName) # Reference an existing table
		print('Able to successfully reference the table')
	return table

table = createTable('QAResults')

# Get string version of today's date
def getDate():
	return datetime.datetime.today().strftime('%Y-%m-%d') # YYYY-MM-DD

# Helper method to add an entry to the table (based off of table name)
def addEntry(tableName, SN, batchNum, tester = 'Zachary', functionTest = 'Pass', commentary = 'Default Message'):
	item = {
		'SerialNumber': {'S': SN}, # Need to specify the data type in addition to the actual entry
		'Tester': {'S': tester},
		'BatchNumber': {'N': str(batchNum)},
		'FunctionTest': {'S': functionTest},
		'LogMessage': {'S': commentary},
		'Date': {'S': getDate()}
		
	}
	client.put_item(
		TableName = tableName,
		Item = item
	)

# Retrieve a given entry--lookup by SN
def getEntry(SN):
	try:
		item = table.get_item(
			Key = { # Can fetch an item based off of its combined partition + sort key (since here we don't necessarily have a unique partition)
				'SerialNumber': SN
			}
		)['Item']
		return item
	except Exception as e:
		print('Unable to retrieve entry:', SN)
		return None



# Populate the table
def testAddEntry():
	addEntry('QAResults', '38383JSBA0', 5, 'Zachary', 'Pass', 'Completed test results on 6-3-2021')
	addEntry('QAResults', '38383JSBA1', 5, 'Zachary', 'Pass', 'Completed test results on 6-3-2021')
	addEntry('QAResults', '38383JSBB0', 5, 'Ryan', 'Fail', 'Found a bug on camera')
	addEntry('QAResults', '38383JSBB1', 5, 'Ryan', 'Pass', 'Completed test results on 6-3-2021')
	print('Able to add entries to the table!')

# Quick way to mass generate entries in our database
possibleResults = ['Pass', 'Fail']
possibleTesters = ['Raymond', 'Abed', 'Tahani'] # Can anyone spot the trend? 
possibleIssueMessages = ['Camera Issue', 'Night mode issue', 'Movement not recognized']
passMessage = 'No issue encountered. Completed Functional Tests!'

def populateEntries(n = 1):
	try:
		prefix = '38383JSBC'
		for i in range(n):
			tester = random.choice(possibleTesters),
			res = 'Pass' if i % 4 != 0 else 'Fail'
			logMessage = random.choice(possibleIssueMessages) if res == 'Fail' else  passMessage
			addEntry('QAResults', prefix + str(i), 2, possibleTesters[i % 3], res, logMessage)
	except Exception as e:
		print('Exception in populateEntries:', e)


# Method to allow for deletion of an entry
def deleteEntry(SN): # Again, serial number serves as the Primary Key
	try:
		table.delete_item(
			Key = { # Give identifier for what to delete
				'SerialNumber': SN
			}
		)
	except Exception as e:
		print('Unable to delete entry')

# Test Framework for delete an entry
def testDeleteEntry():
	deleteEntry('38383JSBB1') # Test deleting an entry
	print('Able to delete entry!')


# Edit an existing entry (different from delete or adding a new field) based off of the serial number
def editEntry(SN, field, newVal):
	try:
		updateExpr = 'SET #attrName = :val1' # Specify what field we actually want to change
		#print('Update Expression:', updateExpr)
		table.update_item(
			Key = { # Again, need to specify identifiers to get the right entry from the table
				'SerialNumber': SN # # Placeholder for the attribute name--otherwise can't modify any field with special characters (like space or hypen)
			},
			UpdateExpression = updateExpr,
			ExpressionAttributeNames = {
				'#attrName': field
			},
			ExpressionAttributeValues = {
				':val1': newVal # Set the field equal to the new value
			}
		)
	except Exception as e:
		print('Unable to edit an entry')
		print('Exception:', e)

def testEditEntry():
	print('Entry Info:', getEntry('38383JSBA0'))
	editEntry('38383JSBA0', 'LogMessage', 'NEW LOG MESSAGE')
	print('Entry Info (modified)', getEntry('38383JSBA0'))

# Method to allow us to delete a given field (different from deleting entire entry or modifying a field within an entry)
def deleteField(SN, field):
	try:
		updateExpr = 'REMOVE #attrName' # Specify what field we actually want to change
		#print('Update Expression:', updateExpr)
		table.update_item(
			Key = { # Again, need to specify identifiers to get the right entry from the table
				'SerialNumber': SN # # Placeholder for the attribute name--otherwise can't modify any field with special characters (like space or hypen)
			},
			UpdateExpression = updateExpr,
			ExpressionAttributeNames = {
				'#attrName': field
			}
		)
		print('Able to successfully delete a field!')
	except Exception as e:
		print('Unable to delete field from an entry')
		print('Exception:', e)

# Test Framework for removing a field from an entry
def testDeleteField():
	addEntry('QAResults', '38383JSBB2', 5, 'Ryan', 'Pass', 'Completed test results on 6-4-2021') # Add another sample entry
	print('Original Entry:', getEntry('38383JSBB2'))
	deleteField('38383JSBB2', 'FunctionTest') # Assume that we want to remove the result of function test for whatever reason
	print('Modified Entry (post-field removal):', getEntry('38383JSBB2'))


# Basic Querying/Scanning Functions

# Return all entries in the table that match a specific value within a field
# NOTE: this will not work with the primary key (serial number) but all other attributes will work
def singleFieldScan(field, val):
	try:
		relevantEntries = table.scan( # Use scan when not working with the HASH key
			FilterExpression = Attr(field).eq(val)
		)['Items']
		return relevantEntries
	except Exception as e:
		print("Error Encountered:", e)

def testSingleFieldScan():
	commonTester= singleFieldScan('Tester', 'Tahani') # Getting all results from a single tester name
	print('\n\nCommon Tester items:\n')
	for item in commonTester:
		print('Tester Item:', item)

	commonBatch = singleFieldScan('BatchNumber', 5)
	print('\n\nCommon Batch items:\n')
	for item in commonBatch:
		print('Batch item:', item)


# Get all entries between 2 dates (inclusive)
def getEntriesBetween(start, end): # Assume start and end are well-formatted strings
	try:
		relEntries = table.scan(
			FilterExpression = Attr('Date').between(start, end)
		)['Items']
		return relEntries
	except Exception as e:
		print('Unable to provide dates between')
		print('Issue encountered:', e)

# Get all entries before a specific date
def getEntriesBefore(before):
	return getEntriesBetween('0000-00-00', before)

# Get all entries after a specific date
def getEntriesAfter(after):
	return getEntriesBetween(after, getDate())

# Query by specific year--assume in YY format
def getYearEntries(date): # Date refers to a specific year
	return getEntriesBetween(date + '-00-00', date + '-12-31')
# Query by specific month + year combination--input: YYYY-MM
def getMonthEntries(date):
	startDate = date + '-01'
	endDate = date + '-31'
	print('Start/End', startDate, endDate)
	return getEntriesBetween(startDate, endDate)

# Query by a specific date (month/day/year)
def getDateEntries(date):
	try:
		relEntries = table.scan(
			FilterExpression = Attr('Date').eq(date)
		)
	except Exception as e:
		print('Encountered error when trying to fetch all entries by specific date')
		print('Error:', e)

# Get only entries with error
def getErrorEntries():
	return singleFieldScan('Function Test', 'Pass') # Use the helper method defined above

# Test the date methods above
def addMoreDates():
	pivot = '2021-06-01'
	before = '2021-05-29'
	after = '2021-06-02'
	for i in range(15):
		sn = '38383JSBA0-dateChange' + str(i)
		addEntry('QAResults', sn, 5, 'Zachary', 'Pass', 'Completed test results on 6-3-2021')
		editEntry(sn, 'Date', before if i % 2 == 0 else after)

def testDateFramework():
	betweenEntries = getEntriesBetween('2021-05-29', '2021-06-02')
	afterEntries = getEntriesAfter('2021-06-01')
	beforeEntries = getEntriesBefore('2021-06-01')
	print('\nEntries between:', '2021-05-29', 'and', '2021-06-02\n\n')
	for item in betweenEntries:
		print('Between Entry:', item)
	print('\nEntries after:', '2021-06-01\n\n')
	for item in beforeEntries:
		print('BEFORE Entry:', item)
	print('\nEntries before', '2021-06-01\n\n')
	for item in afterEntries:
		print('AFTER Entry:', item)

def makeMoreDates():
	dates = ['2020-05-22', '2020-05-22', '2019-04-02', '2019-06-21', '2020-05-02']
	for i in range(20):
		sn = 'prefix-start-' + str(i)
		addEntry('QAResults', sn, 5, 'MiiTester', 'Pass', 'Completed test results on time')
		editEntry(sn, 'Date', dates[i % 5])


def testMoreDateFunctions():
	year19 = getYearEntries('2019')
	may20 = getMonthEntries('2020-05')
	may22_2020 = getDateEntries('2020-05-02')
	print('\n\nYear Tests:\n')
	for e in year19:
		print('Entry for 2019:', e)
	print('\n\nMonth/Year Tests:\n')
	for e in may20:
		print('Entry May 2020:', e)
	print('\n\nDate Tests:\n')
	for e in may22_2020:
		print('Entry for May 22, 2020:', e)

# Function to experiment with more querying/scanning
def testSQL():
	entry = """{
		'SerialNumber': '555RGSW5',
		'Tester': 'Zach',
		'BatchNumber': '444',
		'FunctionTest': 'Pass',
		'LogMessage': 'All Passed',
		'Date': '2021-06-07'
	}"""
	# q1 = "SELECT * FROM QAResults" #  WHERE Serial Number = 38383JSBB2
	# r1 = client.execute_statement(Statement = q1)['Items']
	# for item in r1:
	# 	print('Query1:', item)

	# Query that gets all the Ryan Results
	q2 = "SELECT * FROM QAResults where Tester = 'Ryan'"
	r2 = client.execute_statement(Statement = q2)['Items'] # Execute the query--keep only the relevant info
	print('\n\nQuery2 results\n')
	for item in r2:
		print('Query2:', item)

	# Query that gets all dates prior to 06/02/21
	q3 = "SELECT * FROM QAResults where \"Date\" < '06/02/21'" # Need to use quotes whenever using a reserved word--use backslash as escape character for python
	r3 = client.execute_statement(Statement = q3)['Items']
	print('\n\nQuery3 results\n')
	for item in r3:
		print('Query3:', item) # This will return all items such that the date is prior to 506/02/21

	# Testing adding an entry using INSERT via Query
	try:
		q4 = "INSERT INTO QAResults value " + entry
		print(q4)
		#q4 = "INSERT INTO QAResults"
		r4 = client.execute_statement(Statement = q4)['Items']
		print('\n\nInsert via query success!')
	except Exception as e:
		print('Problem:', e)

	# Testing more complex queries

	# Query that keeps all the *Ray* testers (meaning Ray appears in the tester)
	print('\n\nQuery5 Results\n')
	q5 = "SELECT * FROM QAResults where contains(Tester, 'Ray')"
	r5 = client.execute_statement(Statement = q5)['Items']
	for item in r5:
		print('Query5:', item)

	# Retain all entries that have a log message including the word "Functional" or having a BatchNumber of 2 or 444
	print('\n\nQuery6 Results\n')
	q6 = "SELECT BatchNumber, LogMessage FROM QAResults where contains(LogMessage, 'Functional') or BatchNumber in ['2', '444']" 
	r6 = client.execute_statement(Statement = q6)['Items']
	for item in r6:
		print('Query6:', item)


	# Testing the update function
	q7 = "UPDATE QAResults SET Tester = 'FakeTester' where begins_with(FunctionTest, 'F') and SerialNumber = '38383JSBC0'" # Needs to reference only a single entry
	r7 = client.execute_statement(Statement = q7)
	print('\n\nAble to successfully update with partiQL!')
	# #q5 = "UPDATE QAResults SET tester = 'FakeTester' where Tester contains(Tester, 'Tahani')" #and contains(FunctionTest, 'P')
	# r5 = client.execute_statement(Statement = q5)
	# print(r5)


	#q3 = "SELECT * FROM QAResults WHERE date = 05/27/21"
	#q2 = "INSERT INTO QA-results value " + str(entry)
	#print(q2)
	#r2 = client.execute_statement(Statement = q2)

def makeMoreBatches():
	for i in range(10):
		addEntry('QAResults', 'ztzhu' + str(i), 10, 'Hippy', 'Pass', 'Completed test results on 6-3-2021')

	for i in range(10):
		addEntry('QAResults', 'ztzhu2' + str(i), 15, 'Hippy22', 'Neither', 'New Message')
	print('Able to add more entries for makeMoreBatches!')


def testBatch():
	q1 = "UPDATE QAResults SET Tester = 'Fake Hippy' where BatchNumber = '10'"
	#q1 = "SELECT * FROM QAResults where contains(Tester, 'Ray')"
	r1 = client.execute_transaction(TransactStatements = [{'Statement':q1}])
	print('Executed batch1!')

	# q2 = "DELETE FROM QAResults where BatchNumber = '15'"
	# r2 = client.execute_transaction(TransactStatements = [q2])
	# print('Executed batch2!')
# Testing the partiQL operations with 
def testTransactions():
	return

testAddEntry()
testDeleteEntry()
testEditEntry()
testDeleteField()
populateEntries(20)
makeMoreBatches()
# testSingleFieldScan()
# testDateFramework()
# testSQL()
# testBatch()
addMoreDates()
makeMoreDates()
#testDateFramework()
testMoreDateFunctions()
'''
TODO's
- Brainstorm other queries that might be relevant before single serial number, date between/before/after + matching an exact field
- Work on developing a working GUI as an interface between the backend database and the testers
	- Think about what features would be necessary based off of the flow diagram
	- Save prior results (for particular fields) to avoid repeat work on tester end
- How can scanning a QR code (which generates a number) be automatically added to the database?
	- Link: https://stackoverflow.com/questions/27233351/how-to-decode-a-qr-code-image-in-preferably-pure-python
- Potential (REACH): 
'''





















