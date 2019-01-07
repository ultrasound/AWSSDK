AMI_LIST = [
    {
        'ubuntu': {
            'ImageId': 'ami-0e0f4ff1154834540',
            'Description': 'Canonical, Ubuntu, 16.04 LTS, amd64 xenial image build on 2018-09-12'
        }
    },
    {
        'ami': {
            'ImageId': 'ami-0b4fdb56a00adb616',
            'Description': 'Amazon Linux 2 AMI 2.0.20181114 x86_64 HVM gp2'
        }
    }
]

INSTANCE_TYPE = [
    't1.micro'
]

REGIONS = [
    'us-east-1',
    'us-east-2',
    'us-west-1',
    'us-west-2',
    'us-gov-west-1',
    'eu-west-1',
    'eu-west-2',
    'eu-central-1',
    'ca-central-1',
    'ap-southeast-1',
    'ap-southeast-2',
    'ap-northeast-1',
    'ap-northeast-2',
    'ap-south-1',
    'sa-east-1',
    'cn-north-1',
]

template_data = {
    "EbsOptimized": False,
    "BlockDeviceMappings": [
        {
            "DeviceName": "/dev/sda1",
            "Ebs": {
                "DeleteOnTermination": True,
                "SnapshotId": "snap-0f728a67a25236be2",
                "VolumeSize": 10,
                "VolumeType": "gp2"
            }
        }
    ],
    "NetworkInterfaces": [
        {
            "AssociatePublicIpAddress": True,
            "DeleteOnTermination": True,
            "Description": "Primary network interface",
            "DeviceIndex": 0,
            "Groups": [
                "sg-0ba0c2220b4bbdaa4"
            ],
            "Ipv6Addresses": [],
            "PrivateIpAddresses": [
                {
                    "Primary": True
                }
            ],
            "SubnetId": "subnet-bd0c23d5"
        }
    ],
    "ImageId": "ami-0e0f4ff1154834540",
    "InstanceType": "t2.micro",
    "KeyName": "ubuntu",
    "Monitoring": {
        "Enabled": False
    },
    "Placement": {
        "AvailabilityZone": "ap-northeast-2a",
        "GroupName": "",
        "Tenancy": "default"
    },
    'DisableApiTermination': False,
    'InstanceInitiatedShutdownBehavior': 'stop',
    "CreditSpecification": {
        "CpuCredits": "standard"
    },
    "CapacityReservationSpecification": {
        "CapacityReservationPreference": "open"
    }
}

