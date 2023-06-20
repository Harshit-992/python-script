import boto3
import pytest

def find_nat_gateway_subnet(region, azs):
    ec2_client = boto3.client('ec2', region_name=region)

    response = ec2_client.describe_nat_gateways()
    nat_gateways = response['NatGateways']
    nat_gateway_azs = []

    for nat_gateway in nat_gateways:
        subnet_id = nat_gateway['SubnetId']
        subnet_response = ec2_client.describe_subnets(SubnetIds=[subnet_id])
        subnet = subnet_response['Subnets'][0]
        nat_gateway_azs.append(subnet['AvailabilityZone'])

    return nat_gateway_azs

def test_check_nat_gateway_availability_zones():
    region = 'us-east-2'

    ec2_client = boto3.client('ec2', region_name=region)
    response = ec2_client.describe_availability_zones()
    azs = [az['ZoneName'] for az in response['AvailabilityZones']]

    nat_gateway_azs = find_nat_gateway_subnet(region, azs)

    missing_azs = set(azs) - set(nat_gateway_azs)
    assert not missing_azs, f"Missing NAT gateway in AZs: {missing_azs}"

