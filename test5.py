import boto3
import pytest
import json

def get_instances(region, filter_key, filter_value):
    ec2_client = boto3.client('ec2', region_name=region)
    response = ec2_client.describe_instances(
        Filters=[
            {'Name': filter_key, 'Values': [filter_value]}
        ]
    )

    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])

    return instance_ids

def is_port_open(instance_id, region, port):
    ec2_client = boto3.client('ec2', region_name=region)
    response = ec2_client.describe_instances(InstanceIds=[instance_id])

    security_groups = response['Reservations'][0]['Instances'][0]['SecurityGroups']

    for security_group in security_groups:
        group_id = security_group['GroupId']

        sg_response = ec2_client.describe_security_groups(GroupIds=[group_id])
        ip_permissions = sg_response['SecurityGroups'][0]['IpPermissions']

        for permission in ip_permissions:
            if 'FromPort' in permission and permission['FromPort'] == port:
                return True

    return False

# Replace 'YOUR_REGION' with the desired AWS region
region = 'us-east-1'

# Load instance and port configurations from JSON file
with open('ports.json', 'r') as file:
    config = json.load(file)

# Define the test function outside the loop
def test_check_port_open(instance_config):
    filter_key = instance_config['filter_key']
    filter_value = instance_config['filter_value']
    ports = instance_config['ports']

    instance_ids = get_instances(region, filter_key, filter_value)

    for port in ports:
        for instance_id in instance_ids:
            open_ports = is_port_open(instance_id, region, port)
            assert open_ports, f"Port {port} is not open for instance {instance_id}"

# Dynamically generate the test functions using pytest fixtures
@pytest.fixture(params=config)
def instance_config(request):
    return request.param

@pytest.mark.parametrize("port", [config['ports'] for config in config], indirect=True)
def test_check_port_open_dynamic(instance_config, port):
    test_check_port_open(instance_config)