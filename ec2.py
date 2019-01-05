import datetime
import json
import time

import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2', region_name='ap-northeast-2')

all_instances = ec2.describe_instances()

instanceId_list = []
for reservation in all_instances["Reservations"]:
    instance_id = reservation.get('Instances')[0].get('InstanceId')
    instanceId_list.append(instance_id)


def datetime_to_str(object):
    if isinstance(object, datetime.datetime):
        return object.__str__()


def desc_instances(ins_id=[], save_to_file=False):
    if len(ins_id) > 0:
        res = ec2.describe_instances(InstanceIds=ins_id)
        print(json.dumps(res, default=datetime_to_str, indent=4))
        if save_to_file:
            json.dump(res, open(ins_id[0] + ".json", 'w'), default=datetime_to_str, indent=4)
    else:
        res = ec2.describe_instances()
        print(json.dumps(res, default=datetime_to_str, indent=4))
        if save_to_file:
            json.dump(res, open("all_instances.json", 'w'), default=datetime_to_str, indent=4)
        return res


def start_instances(ins_id=[]):
    try:
        ec2.start_instances(InstanceIds=ins_id, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        ec2.start_instances(InstanceIds=ins_id, DryRun=False)
        print("Instance ", ins_id[0], ": starting\n")
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=ins_id)
        print("Instance ", ins_id[0], ": running\n")
    except ClientError as e:
        print(e)


def stop_instances(ins_id=[]):
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=ins_id, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        ec2.stop_instances(InstanceIds=ins_id, DryRun=False)
        print("Instance ", ins_id[0], ": stopping")
        waiter = ec2.get_waiter('instance_stopped')
        waiter.wait(InstanceIds=ins_id)
        print("Instance ", ins_id[0], ": stopped\n")
    except ClientError as e:
        print(e)


def reboot_instances(ins_id=[]):
    try:
        ec2.reboot_instances(InstanceIds=ins_id, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            print("You don't have permission to reboot instances.")
            raise

    try:
        ec2.reboot_instances(InstanceIds=ins_id, DryRun=False)
        print("Instance ", ins_id[0], ": rebooting")
        waiter = ec2.get_waiter('instance_status_ok')
        waiter.wait(InstanceIds=ins_id)
        print("Instance ", ins_id[0], ": running\n")
    except ClientError as e:
        print('Error', e)


def instance_status(ins_id=[]):
    try:
        response = ec2.describe_instances(InstanceIds=ins_id)
        status = response.get('Reservations')[0].get('Instances')[0].get('State').get('Name')
        print("Instance ", ins_id[0], ": ", status)
        print("")
    except ClientError as e:
        print(e)


def launch_instance(ami_id, instance_type, key_name, tag=''):
    pass


def describe_images(ExecutableUsers=[], Filters=[]):
    response = ec2.describe_images(ExecutableUsers=ExecutableUsers, Filters=Filters)


if __name__ == '__main__':
    while True:
        print("Instances List")

        for idx, instanceId in enumerate(instanceId_list, 1):
            print(idx, ": ", instanceId)

        print("")

        command = input("Operation\n"
                        "1: Stop Instances\n"
                        "2: Start Instances\n"
                        "3: Reboot Instances\n"
                        "4: Describe Instances\n"
                        "5: Check instance status\n"
                        "6: Launch instance\n"
                        "7: Exit\n:")

        if command not in ['1', '2', '3', '4', '5', '6']:
            print("Wrong number\n")
            continue

        print("")

        if command == '1':
            try:
                selected_instance = input("Instance ID to stop: ")
                print("")
                stop_instances(ins_id=[instanceId_list[int(selected_instance) - 1], ])
            except IndexError:
                print("Wrong Number\n")
                continue
        elif command == '2':
            try:
                selected_instance = input("Instance ID to start: ")
                print("")
                start_instances(ins_id=[instanceId_list[int(selected_instance) - 1], ])
            except IndexError:
                print("Wrong Number\n")
                continue
        elif command == '3':
            try:
                selected_instance = input("Instance ID to reboot: ")
                print("")
                reboot_instances(ins_id=[instanceId_list[int(selected_instance) - 1], ])
            except IndexError:
                print("Wrong Number\n")
                continue
        elif command == '4':
            while True:
                all_ = input("Do you want to describe all instances?(Y/N)\n")
                if all_.upper() not in ['Y', 'N']:
                    print("Type only Y or N\n")
                    continue
                break

            while True:
                save_ = input("Do you want to save describe into file?(Y/N)\n")
                if save_.upper() not in ['Y', 'N']:
                    print("Type only Y or N\n")
                    continue
                break

            if all_.upper() == "Y" and save_.upper() == "Y":
                desc_instances(save_to_file=True)
            elif all_.upper() == "Y" and save_.upper() == "N":
                desc_instances()
            else:
                selected_instance = input("Instance Id to describe: ")
                if save_.upper() == "Y":
                    desc_instances(ins_id=[instanceId_list[int(selected_instance) - 1], ], save_to_file=True)
                else:
                    desc_instances(ins_id=[instanceId_list[int(selected_instance) - 1], ])
        elif command == '5':
            try:
                selected_instance = input("Instance ID to check status: ")
                print("")
                instance_status(ins_id=[instanceId_list[int(selected_instance) - 1], ])
            except IndexError:
                print("Wrong Number\n")
                continue

        elif command == '6':
            pass

        elif command == '7':
            break

        else:
            print("Wrong Number")
            print("")
