import boto3
import json


ec2 = boto3.client('ec2', region_name='ap-northeast-2')


def create_key(key_name):
    response =  ec2.create_key_pair(KeyName=key_name)
    key = response["KeyMaterial"]
    keyName = key_name + ".pem"
    with open(keyName, 'w') as f:
        f.write(key)


def del_key(key_name):
    response = ec2.delete_key_pair(KeyName=key_name)
    print(json.dumps(response, indent=4))


def desc_keys():
    response = ec2.describe_key_pairs()
    print(json.dumps(response, indent=4))


command = input("1: Create Key, 2: Delete Key, 3: Listing Keys \n")

if command == "1":
    key_name = input("Type Key Name: ")
    create_key(key_name)
elif command == "2":
    key_name = input("Type Key Name: ")
    del_key(key_name)
elif command == "3":
    desc_keys()
