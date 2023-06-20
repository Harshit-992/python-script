import boto3
import pytest

def find_nat_gateway_subnet(region, az):
    ec2_client = boto3.client('ec2', region_name=region)

    response = ec2_client.describe_nat_gateways()
    nat_gateways = response['NatGateways']

    for nat_gateway in nat_gateways:
        subnet_id = nat_gateway['SubnetId']
        subnet_response = ec2_client.describe_subnets(SubnetIds=[subnet_id])
        subnet = subnet_response['Subnets'][0]
        if subnet['AvailabilityZone'] == az:
            return True
    return False

def test_check_az():
    region = 'us-east-1'
    az = 'us-east-1a'

    ch_az = find_nat_gateway_subnet(region, az)
    assert ch_az, f"nat gateway is not attached in az {az}"

