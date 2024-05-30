import ipfsapi
import sys

api = ipfsapi.Client('0.0.0.0',5003)

# The hash of the file you want to fetch
file_hash = "file hash" #sys.argv[1]

# Get the file from IPFS
try:
    api.get(file_hash)
    print(f'File with hash {file_hash} has been successfully fetched and saved locally.')
except Exception as e:
    print(f'An error occurred: {e}')
