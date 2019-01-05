import datetime
import json

import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2', region_name='ap-northeast-2')


def datetime_to_str(data):
    if isinstance(data, datetime.datetime):
        return data.__str__()


class Ec2Operation:
    def __init__(self):
        self._instance_ids = ''

    @property
    def instance_ids(self):
        return self._instance_ids

    @instance_ids.setter
    def instance_ids(self, instance_ids):
        self._instance_ids = instance_ids

    def start_instances(self):
        try:
            ec2.start_instances(InstanceIds=[self._instance_ids], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, run start_instances without dryrun
        try:
            ec2.start_instances(InstanceIds=[self._instance_ids], DryRun=False)
            print("Instance ", self._instance_ids, ": starting\n")
            waiter = ec2.get_waiter('instance_running')
            waiter.wait(InstanceIds=[self._instance_ids])
            print("Instance ", self._instance_ids, ": running\n")
        except ClientError as e:
            print(e)

    def stop_instances(self):
        # Do a dryrun first to verify permissions
        try:
            ec2.stop_instances(InstanceIds=[self._instance_ids], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, call stop_instances without dryrun
        try:
            ec2.stop_instances(InstanceIds=self._instance_ids, DryRun=False)
            print("Instance ", self.instance_ids, ": stopping")
            waiter = ec2.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=self.instance_ids)
            print("Instance ", self.instance_ids, ": stopped\n")
        except ClientError as e:
            print(e)

    def reboot_instances(self):
        try:
            ec2.reboot_instances(InstanceIds=[self.instance_ids], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("You don't have permission to reboot instances.")
                raise

        try:
            ec2.reboot_instances(InstanceIds=[self.instance_ids], DryRun=False)
            print("Instance ", self.instance_ids, ": rebooting")
            waiter = ec2.get_waiter('instance_status_ok')
            waiter.wait(InstanceIds=[self.instance_ids])
            print("Instance ", self.instance_ids, ": running\n")
        except ClientError as e:
            print('Error', e)

    def desc_instances(self, save_to_file=False, all_instance=False):
        if all_instance:
            res = ec2.describe_instances()
            print(json.dumps(res, default=datetime_to_str, indent=4))
            if save_to_file:
                json.dump(res, open("all_instances.json", 'w'), default=datetime_to_str, indent=4)
            return res
        else:
            res = ec2.describe_instances(InstanceIds=[self.instance_ids])
            print(json.dumps(res, default=datetime_to_str, indent=4))
            if save_to_file:
                json.dump(res, open(self.instance_ids + ".json", 'w'), default=datetime_to_str, indent=4)

    def instance_status(self):
        try:
            response = ec2.describe_instances(InstanceIds=[self.instance_ids])
            status = response.get('Reservations')[0].get('Instances')[0].get('State').get('Name')
            print("Instance ", self.instance_ids, ": ", status)
            print("")
        except ClientError as e:
            print(e)

    def run_instance(self):
        pass


if __name__ == '__main__':
    all_instances = ec2.describe_instances()

    instanceId_list = []
    for reservation in all_instances["Reservations"]:
        instance_id = reservation.get('Instances')[0].get('InstanceId')
        instanceId_list.append(instance_id)

    ec2_ = Ec2Operation()

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
                ec2_.instance_ids = instanceId_list[int(selected_instance) - 1]
                ec2_.stop_instances()
            except IndexError:
                print("Wrong Number\n")
                continue
        elif command == '2':
            try:
                selected_instance = input("Instance ID to start: ")
                print("")
                ec2_.instance_ids = instanceId_list[int(selected_instance) - 1]
                ec2_.start_instances()
            except IndexError:
                print("Wrong Number\n")
                continue
        elif command == '3':
            try:
                selected_instance = input("Instance ID to reboot: ")
                print("")
                ec2_.instance_ids = instanceId_list[int(selected_instance) - 1]
                ec2_.reboot_instances()
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
                ec2_.desc_instances(all_instance=True, save_to_file=True)
            elif all_.upper() == "Y" and save_.upper() == "N":
                ec2_.desc_instances(all_instance=True)
            else:
                selected_instance = input("Instance Id to describe: ")
                if save_.upper() == "Y":
                    ec2_.instance_ids = instanceId_list[int(selected_instance) - 1]
                    ec2_.desc_instances(save_to_file=True)
                else:
                    ec2_.instance_ids = instanceId_list[int(selected_instance) - 1]
                    ec2_.desc_instances()
        elif command == '5':
            try:
                selected_instance = input("Instance ID to check status: ")
                print("")
                ec2_.instance_ids = instanceId_list[int(selected_instance) - 1]
                ec2_.instance_status()
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
