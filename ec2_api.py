"""
client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN,
)

# Or via the Session
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN,
)

session = boto3.Session(profile_name='dev')
# Any clients created from this session will use credentials
# from the [dev] section of ~/.aws/credentials.
dev_s3_client = session.client('s3')
"""

import json

import boto3


ec2 = boto3.client('ec2', region_name='ap-northeast-2')


def describe_instance_status(**kwargs):
    """
    Describes the status of one or more instances.
    By default, only running instances are described,
    unless you specifically indicate to return the status of all instances.
    :param kwargs:
    :return:
    """
    pass


def describe_regions():
    region_list = []

    response = ec2.describe_regions()

    for region in response.get('Regions'):
        region_list.append(region['RegionName'])

    return region_list


def describe_availability_zones():
    """
    Describes one or more of the Availability Zones that are available to you.
    The results include zones only for the region you're currently using.
    If there is an event impacting an Availability Zone,
    you can use this request to view the state and any provided message for that Availability Zone.
    :return:
    """
    zone_list = []

    response = ec2.describe_availability_zones()

    for zone in response.get('AvailabilityZones'):
         zone_list.append(zone['ZoneName'])

    return zone_list


def describe_images():
    response = ec2.describe_images(ExecutableUsers=['all'], Filters=[
        {
            'Name': 'architecture',
            'Values': [
                'x86_64',
            ]
        },
        {
            'Name': 'owner-alias',
            'Values': [
                'amazon',
            ]
        },
        {
            'Name': 'root-device-type',
            'Values': [
                'ebs',
            ]
        },
        {
            'Name': 'virtualization-type',
            'Values': [
                'hvm',
            ]
        }
    ])

    print(json.dumps(response, indent=4))


def run_instances(**kwargs):
    """
    Launches the specified number of instances using an AMI for which you have permissions.

    Request Syntax

    response = client.run_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'DeleteOntermination': True|False,
                    'VolumeSize': 123,
                    'VolumeType': 'gp2'(SSD),
                    'VolumeId': 'string',
                },
            },
        ],
        ImageId='string',
        InstanceType='t1.micro'|'t2.nano'|'t2.micron'|'t2.small',
        KeyName='string',
        MaxCount(Required)=123,
        MinCount(Required)=123,
        Placement={
            'AvailabilityZone': 'string',
            'Tenancy': 'default'
        },
        SecurityGroupIds=['string',],
        SubnetId='string',
        UserData='string',
        DisableApiTermination=True|False(default),
        DryRun=True|False,
        InstanceInitiatedShutdownBehavior='stop(default)'|'terminate',
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True(default)|False,
                'DeleteOnTermination': True|False,
                'Description': 'string',
                'Groups':['string',],
                'PrivateIpAddress': 'string',
                'PrivateIpAddresses': [
                    {
                        'Primary': True|False,
                        'PrivateIpAddress': 'string'
                    },
                ],
                'SubnetId': 'string'
            },
        ],
        PrivateIpAddress='string',
        TagSpecifications=[
            {
                'ResourceType': 'instance'|'volume',
                'Tags': [
                    {
                        'Key': 'string',
                        'Value': 'string'
                    },
                ],
            },
        ],
        LaunchTemplate={
            'LaunchTemplateId': 'string',
            'LaunchTemplateName': 'string',
            'Version': 'string'
        },
    )
    :param kwargs:
    :return:
    """
    pass


def create_launch_template(**kwargs):
    """
    Creates a launch template.
    A launch template contains the parameters to launch an instance.
    When you launch an instance using RunInstances ,
    you can specify a launch template instead of providing the launch parameters in the request.

    Request Syntax

    response = client.create_launch_template(
    DryRun=True|False,
    ClientToken='string',
    LaunchTemplateName='string',
    VersionDescription='string',
    LaunchTemplateData={
        'KernelId': 'string',
        'EbsOptimized': True|False,
        'IamInstanceProfile': {
            'Arn': 'string',
            'Name': 'string'
        },
        'BlockDeviceMappings': [
            {
                'DeviceName': 'string',
                'VirtualName': 'string',
                'Ebs': {
                    'Encrypted': True|False,
                    'DeleteOnTermination': True|False,
                    'Iops': 123,
                    'KmsKeyId': 'string',
                    'SnapshotId': 'string',
                    'VolumeSize': 123,
                    'VolumeType': 'standard'|'io1'|'gp2'|'sc1'|'st1'
                },
                'NoDevice': 'string'
            },
        ],
        'NetworkInterfaces': [
            {
                'AssociatePublicIpAddress': True|False,
                'DeleteOnTermination': True|False,
                'Description': 'string',
                'DeviceIndex': 123,
                'Groups': [
                    'string',
                ],
                'Ipv6AddressCount': 123,
                'Ipv6Addresses': [
                    {
                        'Ipv6Address': 'string'
                    },
                ],
                'NetworkInterfaceId': 'string',
                'PrivateIpAddress': 'string',
                'PrivateIpAddresses': [
                    {
                        'Primary': True|False,
                        'PrivateIpAddress': 'string'
                    },
                ],
                'SecondaryPrivateIpAddressCount': 123,
                'SubnetId': 'string'
            },
        ],
        'ImageId': 'string',
        'InstanceType': 't1.micro'|'t2.nano'|'t2.micro'|'t2.small'|'t2.medium'|'t2.large'|'t2.xlarge'|'t2.2xlarge'|'t3.nano'|'t3.micro'|'t3.small'|'t3.medium'|'t3.large'|'t3.xlarge'|'t3.2xlarge'|'m1.small'|'m1.medium'|'m1.large'|'m1.xlarge'|'m3.medium'|'m3.large'|'m3.xlarge'|'m3.2xlarge'|'m4.large'|'m4.xlarge'|'m4.2xlarge'|'m4.4xlarge'|'m4.10xlarge'|'m4.16xlarge'|'m2.xlarge'|'m2.2xlarge'|'m2.4xlarge'|'cr1.8xlarge'|'r3.large'|'r3.xlarge'|'r3.2xlarge'|'r3.4xlarge'|'r3.8xlarge'|'r4.large'|'r4.xlarge'|'r4.2xlarge'|'r4.4xlarge'|'r4.8xlarge'|'r4.16xlarge'|'r5.large'|'r5.xlarge'|'r5.2xlarge'|'r5.4xlarge'|'r5.8xlarge'|'r5.12xlarge'|'r5.16xlarge'|'r5.24xlarge'|'r5.metal'|'r5a.large'|'r5a.xlarge'|'r5a.2xlarge'|'r5a.4xlarge'|'r5a.12xlarge'|'r5a.24xlarge'|'r5d.large'|'r5d.xlarge'|'r5d.2xlarge'|'r5d.4xlarge'|'r5d.8xlarge'|'r5d.12xlarge'|'r5d.16xlarge'|'r5d.24xlarge'|'r5d.metal'|'x1.16xlarge'|'x1.32xlarge'|'x1e.xlarge'|'x1e.2xlarge'|'x1e.4xlarge'|'x1e.8xlarge'|'x1e.16xlarge'|'x1e.32xlarge'|'i2.xlarge'|'i2.2xlarge'|'i2.4xlarge'|'i2.8xlarge'|'i3.large'|'i3.xlarge'|'i3.2xlarge'|'i3.4xlarge'|'i3.8xlarge'|'i3.16xlarge'|'i3.metal'|'hi1.4xlarge'|'hs1.8xlarge'|'c1.medium'|'c1.xlarge'|'c3.large'|'c3.xlarge'|'c3.2xlarge'|'c3.4xlarge'|'c3.8xlarge'|'c4.large'|'c4.xlarge'|'c4.2xlarge'|'c4.4xlarge'|'c4.8xlarge'|'c5.large'|'c5.xlarge'|'c5.2xlarge'|'c5.4xlarge'|'c5.9xlarge'|'c5.18xlarge'|'c5d.large'|'c5d.xlarge'|'c5d.2xlarge'|'c5d.4xlarge'|'c5d.9xlarge'|'c5d.18xlarge'|'c5n.large'|'c5n.xlarge'|'c5n.2xlarge'|'c5n.4xlarge'|'c5n.9xlarge'|'c5n.18xlarge'|'cc1.4xlarge'|'cc2.8xlarge'|'g2.2xlarge'|'g2.8xlarge'|'g3.4xlarge'|'g3.8xlarge'|'g3.16xlarge'|'g3s.xlarge'|'cg1.4xlarge'|'p2.xlarge'|'p2.8xlarge'|'p2.16xlarge'|'p3.2xlarge'|'p3.8xlarge'|'p3.16xlarge'|'p3dn.24xlarge'|'d2.xlarge'|'d2.2xlarge'|'d2.4xlarge'|'d2.8xlarge'|'f1.2xlarge'|'f1.4xlarge'|'f1.16xlarge'|'m5.large'|'m5.xlarge'|'m5.2xlarge'|'m5.4xlarge'|'m5.12xlarge'|'m5.24xlarge'|'m5a.large'|'m5a.xlarge'|'m5a.2xlarge'|'m5a.4xlarge'|'m5a.12xlarge'|'m5a.24xlarge'|'m5d.large'|'m5d.xlarge'|'m5d.2xlarge'|'m5d.4xlarge'|'m5d.12xlarge'|'m5d.24xlarge'|'h1.2xlarge'|'h1.4xlarge'|'h1.8xlarge'|'h1.16xlarge'|'z1d.large'|'z1d.xlarge'|'z1d.2xlarge'|'z1d.3xlarge'|'z1d.6xlarge'|'z1d.12xlarge'|'u-6tb1.metal'|'u-9tb1.metal'|'u-12tb1.metal'|'a1.medium'|'a1.large'|'a1.xlarge'|'a1.2xlarge'|'a1.4xlarge',
        'KeyName': 'string',
        'Monitoring': {
            'Enabled': True|False
        },
        'Placement': {
            'AvailabilityZone': 'string',
            'Affinity': 'string',
            'GroupName': 'string',
            'HostId': 'string',
            'Tenancy': 'default'|'dedicated'|'host',
            'SpreadDomain': 'string'
        },
        'RamDiskId': 'string',
        'DisableApiTermination': True|False,
        'InstanceInitiatedShutdownBehavior': 'stop'|'terminate',
        'UserData': 'string',
        'TagSpecifications': [
            {
                'ResourceType': 'customer-gateway'|'dedicated-host'|'dhcp-options'|'elastic-ip'|'fleet'|'fpga-image'|'image'|'instance'|'internet-gateway'|'launch-template'|'natgateway'|'network-acl'|'network-interface'|'reserved-instances'|'route-table'|'security-group'|'snapshot'|'spot-instances-request'|'subnet'|'transit-gateway'|'transit-gateway-attachment'|'transit-gateway-route-table'|'volume'|'vpc'|'vpc-peering-connection'|'vpn-connection'|'vpn-gateway',
                'Tags': [
                    {
                        'Key': 'string',
                        'Value': 'string'
                    },
                ]
            },
        ],
        'ElasticGpuSpecifications': [
            {
                'Type': 'string'
            },
        ],
        'ElasticInferenceAccelerators': [
            {
                'Type': 'string'
            },
        ],
        'SecurityGroupIds': [
            'string',
        ],
        'SecurityGroups': [
            'string',
        ],
        'InstanceMarketOptions': {
            'MarketType': 'spot',
            'SpotOptions': {
                'MaxPrice': 'string',
                'SpotInstanceType': 'one-time'|'persistent',
                'BlockDurationMinutes': 123,
                'ValidUntil': datetime(2015, 1, 1),
                'InstanceInterruptionBehavior': 'hibernate'|'stop'|'terminate'
            }
        },
        'CreditSpecification': {
            'CpuCredits': 'string'
        },
        'CpuOptions': {
            'CoreCount': 123,
            'ThreadsPerCore': 123
        },
        'CapacityReservationSpecification': {
            'CapacityReservationPreference': 'open'|'none',
            'CapacityReservationTarget': {
                'CapacityReservationId': 'string'
            }
        },
        'HibernationOptions': {
            'Configured': True|False
        },
        'LicenseSpecifications': [
            {
                'LicenseConfigurationArn': 'string'
            },
        ]
    }
)
    :param kwargs:
    :return:
    """
    response = ec2.create_launch_template(
        DryRun=False,
        LaunchTemplateName='Jenkins_template',
        VersionDescription='V1',
        LaunchTemplateData={
            'EbsOptimized': False,
            'BlockDeviceMapping': [
                {
                    'DeviceName': '/dev/sda',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': 10,
                        'VolumeType': 'gp2'
                    },
                },
            ],
            'NetworkInterFaces': [
                {
                    'AssociatePublicIpAddress': True,
                    'DeleteOnTermination': True,
                    'Description': 'Jenkins',
                    'Groups': [
                        'sg-0ba0c2220b4bbdaa4',
                    ],
                    'SubnetId': 'subnet-bd0c23d5',
                },
            ],
            'ImageId': 'ami-0e0f4ff1154834540',
            'InstanceType': 't2.micro',
            'KeyName': 'ubuntu.pem',
            'Placement': {
                'AvailabilityZone': 'ap-northeast-2a',
                'Tenancy': 'default',
            },
            'DisableApiTermination': False,
            'InstanceInitiatedShutdownBehavior': 'stop',
        },

    )
    print(json.dumps(response, indent=4))


if __name__ == '__main__':
    create_launch_template()
