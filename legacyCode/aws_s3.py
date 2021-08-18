# Amazon S3

import boto3
import random
import logging
from botocore.exceptions import ClientError

# Core functionalities
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

# Helper method to return the name of the buckets in a list format
def getBucketNames():
	return [b.name for b in s3.buckets.all()] # Return current bucket names

# Helper method to get all the objects w/in a bucket
def getBucketObjectNames(bucket):
	objects = list(s3.Bucket(bucket).objects.all()) # Get a list of the existing objects in a bucket
	return [o.key for o in objects] # Print out all the existing keys

# Helper method to allow generic upload of a file to an s3 bucket
def uploadFile(filePath, bucket, objectName = None):
	'''
	filePath: specifies the local path/file name to access the actual file
	bucket: provides name fo the bucket that we're uploading the file to
	objectName: can provide a name if we don't want it to default to filePath
	'''
	if objectName is None: # If no name was specified
		objectName = filePath # Default to the file path for the name of the object
	try:
		s3_client.upload_file(filePath, bucket, objectName) # Upload the file to the desired bucket w/ a specific name if specified
	except ClientError as e: # Encountered an error upon upload
		logging.error(e) # Register that an error occurred in the logger
		return False # Indicate that the operation was unsuccessful
	return True # Able to successfully upload

def createBuckets(n = 1): # Create n new buckets
	for i in range(10, n + 10):
		#print('iteration:', i)
		s3.create_bucket(Bucket = 'ztzhu' + str(i)) 
		#print('worked at: ', i)
# for bucket in s3.buckets.all(): # Get all the names of the buckets
# 	print('bucket name:', bucket.name)
createBuckets(5)
print(getBucketNames()) # Get the names of all buckets at our disposal

# Add objects to these buckets
bucketNames = ['ztzhu1' + str(i) for i in range(5)]
filePathsToAdd = ['s' + str(i) + '.xlsx' for i in range(1, 6)]
print(filePathsToAdd)
print(bucketNames)

tempBucket = s3.Bucket('ztzhu10')

#s3_client.upload_file(filePathsToAdd[0], 'ztzhu10', 's1.xlsx')

# Upload a .xlsx file to each of the original buckets
for i in range(5):
	uploadFile(filePathsToAdd[i], bucketNames[i])

# Print out the objects contained in each bucket
for bucket in bucketNames:
	print('bucket:', bucket, 'obj names:', getBucketObjectNames(bucket))

# Using the sample test data
specialBucket = s3.create_bucket(Bucket = 'ztzhu-special') # Create a bucket to experiment with the given data
uploadSpecial = uploadFile('sampleTestLog.xlsx', 'ztzhu-special') # Upload the test data to this bucket
print('uploaded test data?', uploadSpecial)


# Downloading data from a bucket
downloadSpecial = s3_client.download_file('ztzhu-special', 'sampleTestLog.xlsx', 'sampleTestLog-copy.xlsx') # Parameters: bucket name (FROM), object name (FROM), file name (SAVED TO)
print('able to download?', downloadSpecial)



# data = open('test.png', 'rb') # Read in the image saved in the awsSample directory
# s3.Bucket('ztzhu1').put_object(Key = 'test.png', Body = data) # Key: specify what object we're putting into the bucket of our choosing, Body...?


# getBucketNames() # Call method defined above
# newBucket = s3.Bucket('ztzhu3') # Create a new bucket--specify name as an identifier
# print('Does this bucket ever show up?', newBucket)
# #print([b.name for b in s3.buckets.all()]) # Print current bucket names

# # Add a random object to each bucket--batch actions
# def addRandomObjs():
# 	for b in s3.buckets.all():
# 		rand = random.randint(0, int(len(list(s3.buckets.all())))) # Generate a random integer
# 		b.put_object(Key = 's' + str(rand) + '.xlsx')

# # Creating a bucket
# ztzhu2_bucket = s3.create_bucket(Bucket = 'ztzhu2') # Try creating a new bucket
# #print('new list of buckets:', list(s3.buckets.all())) # Get the current bucket objects



# # Get object information & reference objects
# obj1 = s3.Object('ztzhu1', 'id1') # Reference object in bucket ztzhu1, with the identifier: id1 (doesn't exist but non-issue b/c lazy computation)
# obj2 = s3.Object('ztzhu2', 'id2') # New object in new bucket w/ different identifier; see above
# objSummary = s3.ObjectSummary('ztzhu1', 'id1') # Get info about an object from a bucket
# print('object summary:', objSummary.bucket_name, objSummary.key) # We can specify object info w/o them actually existing


# client3 = boto3.client('s3') # Create a client instance

# # Try deleting an object from a bucket?
# ableToDelete = client3.delete_object(
# 	Bucket = 'ztzhu1',
# 	Key = 's3.xlsx'
# 	)
# print('Delete success?', ableToDelete) # Successfully deleted it

# # Delete an overall bucket--cannot rerun this code b/c once the bucket is deleted, raises an error trying to delete non-existent bucket
# '''
# weirdBucket = s3.Bucket('access-log-685568857978us-east-2') # Create a bucket with a given name
# weirdBucket.objects.all().delete() # Access all the objects and empty the bucket
# print('weirdBucket objects:', list(weirdBucket.object_versions.all())) # See if this bucket is indeed empty
# deleteBucket = client3.delete_bucket(Bucket = 'access-log-685568857978us-east-2') # Delete bucket once empty
# print('Delete bucket?', deleteBucket) # Check to make sure delete was successful
# '''

# # Delete when versioning is enabled
# # ztzhu4_bucket = s3.create_bucket(Bucket = 'ztzhu4') # Create bucket
# # ztzhu4_bucket.put_object(Key = 's1.xlsx', Body = data) # Give it something
# '''
# deleteVersioningBucket = s3.Bucket('ztzhu4') # Access original folder
# dvbObjs = deleteVersioningBucket.object_versions.all() # Get all the versioned objects currently in this bucket
# print('curr list dvbobs:', list(dvbObjs)) 
# versionsdeleteObjs =  dvbObjs.delete() # Delete all the objects originally in this bucket
# print('successful delete?', versionsdeleteObjs) # Make sure no errors
# deleteBucket2 = client3.delete_bucket(Bucket = 'ztzhu4') # Get rid of bucket entirely
# print('Delete ztzhu4?', deleteBucket2) # Check to make sure delete was successful
# '''

# # Copy an object from one bucket to another
# print('prev ztzhu2 objects:', list(s3.Bucket('ztzhu2').objects.all()))
# copy_source = {
# 	'Bucket': 'ztzhu1', # Need to provide name of the bucket we want to copy from
# 	'Key': 'test.png' # Specify name of key that gets copied FROM
# }
# destination = s3.Bucket('ztzhu2') # Reference another bucket
# copySuccess = destination.copy(copy_source, 'newTest.png') # Create a copy of this object
# print(copySuccess)
# print('new ztzhu2 objects:', list(s3.Bucket('ztzhu2').objects.all()))


# # print([b.name for b in s3.buckets.all()]) # Print current bucket names








