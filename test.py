import boto3
import pytest

def get_instance_ids(region):
    ec2_client = boto3.client('ec2', region_name=region)
    response = ec2_client.describe_instances()
    
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    
    return instance_ids

def get_open_ports(instance_id, region):
    ec2_client = boto3.client('ec2', region_name=region)
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    
    security_groups = response['Reservations'][0]['Instances'][0]['SecurityGroups']
    open_ports = []
    
    for security_group in security_groups:
        group_id = security_group['GroupId']
        group_name = security_group['GroupName']
        
        sg_response = ec2_client.describe_security_groups(GroupIds=[group_id])
        ip_permissions = sg_response['SecurityGroups'][0]['IpPermissions']
        
        for permission in ip_permissions:
            if 'FromPort' in permission:
                from_port = permission['FromPort']
                to_port = permission['ToPort']
                protocol = permission['IpProtocol']
                
                open_ports.append((group_name, from_port, to_port, protocol))
    
    return open_ports

# Replace 'YOUR_REGION' with the desired AWS region
region = 'us-east-1'

# Get all instance IDs in the region
instance_ids = get_instance_ids(region)

@pytest.mark.parametrize("instance_id", instance_ids)
def test_check_open_ports(instance_id):
    # Get open ports in the instance's security groups
    open_ports = get_open_ports(instance_id, region)
    
    # Check if any open ports are found
    assert open_ports, f"No open ports found for instance {instance_id}"
    
    # Output open ports for the instance
    print(f"Instance ID: {instance_id}")
    print("Open ports:")
    for group_name, from_port, to_port, protocol in open_ports:
        print(f"- Security Group: {group_name}")
        print(f"  Port Range: {from_port} - {to_port}")
        print(f"  Protocol: {protocol}")
    
    print()

    
    