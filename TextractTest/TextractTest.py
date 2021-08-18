import boto3
from collections import Counter
import re
import base64


# Start up a client instance for textract
client = boto3.client('textract')
# All the sample pathways to test SN generation
paths = ['catalina-4-19-21.jpg', 'catalina-10-5-21.jpg', 'indoor-5-17-21.jpg', 'mini-3-5-2021.jpg',
         'mini-4-22-20.jpg', 'mini-5-31-21.jpg', 'mini-10-5-21.jpg', 'mini-12-21-20.jpg', 'mini-26-4-21.jpg']
paths = ['catalina-4-19-21.jpg', 'catalina-10-5-21.jpg', 'indoor-5-17-21.jpg', 'mini-3-5-2021.jpg',
         'mini-4-22-20.jpg']
paths = ['catalina-4-19-21.jpg']


# Function to extract text from an image
def analyzeDocument(path):
    with open(path, 'rb') as raw_image: # Open the image from path
        tempImage = raw_image.read() # Read in the image
        # print('readImage:', tempImage)
        byteImage = bytearray(tempImage) # Convert to a byte array
        # print('byteImage', byteImage)
        b64Str = base64.b64encode(tempImage)
        decoded = base64.b64decode(b64Str)
        print(decoded == tempImage) # Prints true --> ensures that the base64 module properly encodes + decodes an image
        # print('base64string:', b64Str)
    response = client.detect_document_text(Document = {'Bytes': byteImage}) # Call text detection method
    # Bucket path lies below
    '''
    response = client.detect_document_text(
        Document = {
            'S3Object': {
                'Bucket': 'dashboard-textract-bucket',
                'Name': path
            }
        }
    )
    '''
    return response
# analyzeDocument(paths[0])

# Alternate method that uses the documnet analysis method (for "table" data)
def extractText(path):
    with open(path, 'rb') as raw_image:
        tempImage = raw_image.read()
        byteImage = bytearray(tempImage)
    response = client.analyze_document(Document = {'Bytes': byteImage}, FeatureTypes = ['TABLES'])
    return response


'''
Intuition for the filter
- We know that the SN has to be of a sufficient length (with some buffer in case some characters are filtered out)
- Some queries will include excessive spaces (we know that in theory the SN should be one big blob)
    - Can remove any queries that don't have any digits or alphabetical characters since SN should contain both
'''

def testRelevant():
    cleaned = []
    allText = []
    for path in paths: # Iterate across all paths
        results = analyzeDocument(path) # Analyze the given image
        blocks = results['Blocks'] # Extract only relevant information
        tableData = [x['Text'] for x in blocks if x['BlockType'] == 'LINE'] # Only keep data that is a "line"
        cleanedData = [] # Use a list b/c algorithm can produce duplicates
        for t in tableData:
            if len(t) > 8 and any(c.isdigit() for c in t) and any(c.isalpha() for c in t) and 'Date' not in t and t.count(' ') <= 1:
                cleanedData.append(t) # Only include non-filtered out data
        cleaned.append(cleanedData)
        allText.append(tableData)
    return (allText, cleaned)

allText, serialNums = testRelevant()

# Helper method to find the "majority" ruling
def mostCommonElement(lst):
    temp = Counter(lst).most_common(1) # Get the most frequent element + its count
    return temp[0][0] # Return the most frequently appearing element

# Entries that are deemed suspicious
def flagEntries(lst):
    prefixes = [s[:7] for s in lst] # Get the first 7 characters
    lengths = [len(s) for s in lst] # Get the length of the sequence
    isDuplicate = [lst.count(s) > 1 for s in lst] # Check to see if they're are duplicates
    allowedChars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-') # Only possible characters in SN
    containsIrreg = [bool(re.search('[^A-za-z0-9-]', s)) for s in lst] # Look for suspicious characters
    mcp = mostCommonElement(prefixes) # Get most common prefix
    mcl = mostCommonElement(lengths) # Get most commonly appearing length
    suspicious = [prefixes[i] != mcp or lengths[i] != mcl or isDuplicate[i] or containsIrreg[i] for i in range(len(lst))] # Corresponds to suspicious entries
    return suspicious

# print(serialNums[0]) # Sanity Check

# Getting the serial numbers for each batch along with their "suspicion based on criteria above"
suspectLists = [flagEntries(lst) for lst in serialNums]
for i in range(len(serialNums)):
    pass
    # print(serialNums[i])
    # print(suspectLists[i], '\n\n')
#print(flagEntries(serialNums[0]))


# Check to see what the "sloppy" data looks like
# for rawText in allText:
#     print(rawText, '\n\n')



