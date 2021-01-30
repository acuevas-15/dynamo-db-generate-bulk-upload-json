# dynamo-db-generate-bulk-upload-json
Using a csv that has been exported by dynamodb, generates a json
file that can be bulk uploaded to dynamodb using the `aws dynamodb
batch-write-item` command. This script can be run from the cli, or the
function generate_dynamo_batch_json may be invoked by another python
script. NOTE: this script does not stream csv memory so it may not be
suitable for very large files.

## Usage

Ex:
`python dynamo-db-generate-bulk-upload-json my_file.csv`
