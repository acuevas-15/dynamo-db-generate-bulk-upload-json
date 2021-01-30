from __future__ import print_function
import csv
import json
import ntpath
import sys

def generate_dynamo_batch_json_file(name):
    """
    takes a file name pointing to a csv that has been exported from dynamo db, or conforms
    to the expected format: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html
    """
    input_filename = name
    name = ntpath.basename(name).split('.')[0]
    with open(input_filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader, None)
        fields = []
        for field in header:
            field_metadata = {}
            parts = field.split(' ') # ex: 'CountryId (S)' yields ['CountryId', '(S)']
            field_metadata["field_name"] = parts[0]
            field_metadata["field_type"] = parts[1][1:-1]
            fields.append(field_metadata)

        output_items = []
        for row in csvreader:
            output_item = {}
            for i, column_value in enumerate(row):
                field_name = fields[i]["field_name"]
                field_type = fields[i]["field_type"]
                field_value = column_value
                field = { field_type: field_value }
                output_item[field_name] = field
    
            output_items.append({
                "PutRequest": {
                    "Item": output_item
                }
            })
    
        return json.dumps({"RequestItems": { name: output_items }}, indent=2)

if __name__ == "__main__":
    arg_len = len(sys.argv)
    if arg_len > 2:
        print("ERROR: missing input csv file name", file=sys.stderr)
        print("       usage: python generate_dynamo_json.py [input_filename]", file=sys.stderr)
        sys.exit()
    elif arg_len == 1:
        print("usage: python generate_dynamo_json.py [input_filename]")
        sys.exit()

    file_name = sys.argv[1]
    print(generate_dynamo_batch_json_file(file_name))
