import boto3

# Input to be taken
region = input("Enter the region:")
availability_zone = input("Enter the availabilty zone:")
instance_type = input("Enter the instance type :")

# Defining client for services
ec2_region = boto3.client('ec2', region_name=region)
ec2 = boto3.client('ec2')
s3 = boto3.client('s3')
rds = boto3.client('rds', region_name=region)
client = boto3.client('service-quotas')

# Check if the instance type is available in the region


# count non-default vpc
def list_vpc():
        vpcs = ec2_region.describe_vpcs()
        count_vpc = 0
        for vpc in vpcs['Vpcs']:
                if not vpc['IsDefault']:
                        count_vpc += 1
                        print('VPC ID:', vpc['VpcId'])
        print(f"Number of non-default VPCs in {region}:  {count_vpc}")
        response = client.get_service_quota(
                ServiceCode='vpc',
                QuotaCode='L-F678F1CE'
        )
        print('Service quota left: ' + str(response['Quota']['Value']-count_vpc-1))
        print()


# Retrieve a list of all subnets in region
def list_subnet():
        response = ec2_region.describe_subnets()
        count_subnet = 0
        for subnet in response['Subnets']:
                if not subnet['DefaultForAz']:
                        count_subnet += 1
                        subnet_id = subnet['SubnetId']
                        vpc_id = subnet['VpcId']
                        availability_zone = subnet['AvailabilityZone']
                        cidr_block = subnet['CidrBlock']

                        subnet_response = ec2_region.describe_subnets(SubnetIds=[subnet_id])

                        available_ips = subnet_response['Subnets'][0]['AvailableIpAddressCount']

                        print(f"Subnet ID: {subnet_id}")
                        print(f"VPC ID: {vpc_id}")
                        print(f"Availability Zone: {availability_zone}")
                        print(f"CIDR Block: {cidr_block}")
                        print(f"Available IP Addresses: {available_ips}")
        response = client.get_service_quota(
                        ServiceCode='vpc',
                        QuotaCode='L-407747CB'
        )
        print('Service quota left: ' + str(response['Quota']['Value']-count_subnet))
        print()

# Count Nat gateways
def list_nat_gateways():
        nat_gateways = ec2_region.describe_nat_gateways()
        count_nat_gateways = 0
        for gateway in nat_gateways['NatGateways']:
                count_nat_gateways += 1
                print('ID:', gateway['NatGatewayId'])
                print('Subnet:', gateway['SubnetId'])
                print('Public IP:', gateway['NatGatewayAddresses'][0]['PublicIp'])
                print('Private IP:', gateway['NatGatewayAddresses'][0]['PrivateIp'])
        print(f"Number of Nat gateways created: {count_nat_gateways}")
        print()

# Count the number of Elastic IP addresses
def list_elastic_ip():
        response = ec2.describe_addresses()
        count_eip = 0
        for address in response['Addresses']:
               #if 'AssociationId' not in address:  
                count_eip += 1
                print('ElasticIp IPv4 Address:', address['PublicIp'])
                print('Associated Instance ID:', address.get('InstanceId'))

        print(f"Number of  Elastic IP addresses created: {count_eip}")
        print()

# count number of s3 buckets
def list_s3():
        s3_count = len(s3.list_buckets()['Buckets'])
        print(f"Number of  s3 bucket: {s3_count}")
        response = client.get_aws_default_service_quota(
                      ServiceCode='s3',
                      QuotaCode='L-DC2B2D3D'
        )
        print('Service quota left: ' + str(response['Quota']['Value']-s3_count))
        print()

#count number of rds db instances
def list_rds():
        rds_count = len(rds.describe_db_instances()['DBInstances'])
        print(f"Number of  rds instances in {region}: {rds_count}")
        response = client.get_service_quota(
                      ServiceCode='rds',
                      QuotaCode='L-7B6409FD'
        )
        print('Service quota left: ' + str(response['Quota']['Value']-rds_count))
        print()

list_vpc()
list_subnet()
list_nat_gateways()
list_elastic_ip()
list_s3()
list_rds()