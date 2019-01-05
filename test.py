import unittest
import json

import boto3

from ec2 import *


ec2 = boto3.client('ec2', region_name='ap-northeast-2')


class TestEC2(unittest.TestCase):
    def test_desc_all_instances(self):
        direct_call = ec2_.describe_instances()
        func_call = desc_instances()

        self.assertIn(func_call, direct_call)

    def test_desc_specific_instance(self):
        direct_call = ec2_.describe_instances(InstanceIds=["i-03acb151a841367d3"])
        func_call = desc_instances(ins_id=["i-03acb151a841367d3"])

        self.assertEqual(direct_call, func_call)

    def test_to_save_into_json_all_instances(self):
        pass

    def test_stop_instances(self):
        pass

    def test_start_instances(self):
        pass

    def test_reboot_instances(self):
        pass


if __name__ == '__main__':
    unittest.main()
