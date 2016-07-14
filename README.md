# aws-flare
An aws primitive alert framework.

aws-flare makes no assumptions on how data is gathered instead it only attempts to validate
data returned from AWS APIs. 

## Features

- Identifies common security issues
- Extensible


## Usage

    >>> from aws_flare.aws.elb import ELBSchema

    >>> elb = {
        "Subnets": ["subnet-example"],
        "CanonicalHostedZoneNameID": "Z1M58G0W56PQJA",
        "CanonicalHostedZoneName": "exampleELB.us-west-1.elb.amazonaws.com",
        "ListenerDescriptions": [{
            "Listener": {
                "InstancePort": 80,
                "LoadBalancerPort": 80,
                "Protocol": "HTTP",
                "InstanceProtocol": "HTTP"
            },
            "PolicyNames": []
        }],
        "HealthCheck": {
            "HealthyThreshold": 10,
            "Interval": 30,
            "Target": "TCP:80",
            "Timeout": 5,
            "UnhealthyThreshold": 2
        },
        "VPCId": "vpc-exampleELB",
        "BackendServerDescriptions": [],
        "Instances": [{
            "InstanceId": "i-example"
        }, {
            "InstanceId": "i-example"
        }],
        "DNSName": "exampleELB.us-west-1.elb.amazonaws.com",
        "SecurityGroups": ["sg-example"],
        "Policies": {
            "LBCookieStickinessPolicies": [],
            "AppCookieStickinessPolicies": [],
            "OtherPolicies": []
        },
        "LoadBalancerName": "exampleELB",
        "CreatedTime": 1366831849,
        "AvailabilityZones": ["us-west-1c", "us-west-1a"],
        "Scheme": "internet-facing",
        "SourceSecurityGroup": {
            "OwnerAlias": "00000000000",
            "GroupName": "exampleElb"
        }
    }

    # getting all errors retaining structure
    >>> from pprint import pprint
    >>> errors = ELBSchema().load(elb).errors
    >>> pprint(errors)

    {'listener_descriptions': ['You have an ELB but have not configured TLS/SSL. '
                               'Consider adding TLS.'],
     'scheme': ['ELB is externally facing, consider moving your service '
                'internally.'],
     'security_groups': {0: {},
                         '_schema': ['No security group primitive provided, '
                                     'security group rules will not be '
                                     'validated.']}}


    # getting all the errors without structure
    >>> from aws_flare.core import flatten_errors
    >>> pprint(flatten_errors(errors))

    ['You have an ELB but have not configured TLS/SSL. Consider adding TLS.',
     'No security group primitive provided, security group rules will not be '
     'validated.',
     'ELB is externally facing, consider moving your service internally.']

    # custom options are set via the config set them before attempt validation
    >>> from aws_flare.aws.ec2 import SecurityGroupSchema

    >>> data = {
        "IpPermissionsEgress": [],
        "Description": "example security group",
        "IpPermissions": [{
            "PrefixListIds": [],
            "FromPort": 80,
            "IpRanges": [{
                "CidrIp": "54.23.123.33/32"
            }],
            "ToPort": 80,
            "IpProtocol": "tcp",
            "UserIdGroupPairs": []
        }],
        "GroupName": "example-sg",
        "OwnerId": "000000000",
        "GroupId": "sg-example"
    }

    >>> errors = SecurityGroupSchema().load(data).errors
    >>> pprint(flatten_errors(errors))

    ['Security group allows all ranges via 0.0.0.0/0.']






