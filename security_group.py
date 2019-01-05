import json

import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2', region_name='ap-northeast-2')


def desc_sg():
    try:
        response = ec2.describe_security_groups()
        json.dump(response, open("Security_Groups", 'w'), indent=4)
        print(json.dumps(response, indent=4))
    except ClientError as e:
        print(e)


def create_sg():
    sg_name = input("Type Security Name: ")
    desc = input("Type Description: ")
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    try:
        response = ec2.create_security_group(GroupName=sg_name,
                                             Description=desc,
                                             VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print("Ingress Successfully Set %s" % data)
    except ClientError as e:
        print(e)


def del_sg():
    sg_name = input("Type Security Group Name: ")
    try:
        response = ec2.delete_security_group(GroupName=sg_name)
        print('Security Group Deleted')
    except ClientError as e:
        print(e)


command = input("1: Create Security Group, 2: Delete Security Group, 3: Describe Security Group \n")
if command == "1":
    create_sg()
elif command == "2":
    del_sg()
elif command == "3":
    desc_sg()
