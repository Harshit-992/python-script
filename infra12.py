import boto3

# Input to be taken
region = input("Enter the region:")

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
                
                count_vpc += 1
                       
        response = client.get_service_quota(
                ServiceCode='vpc',
                QuotaCode='L-F678F1CE'
        )
        if(int(response['Quota']['Value']-count_vpc)==0):
                print("Vpc quota exhausted")
        else:
                print("Vpc quota available")
        print()


# Retrieve a list of all subnets in region
def list_subnet():
        response = ec2_region.describe_subnets()
        count_subnet = 0
        for subnet in response['Subnets']:
                
                count_subnet += 1
                subnet_id = subnet['SubnetId']
                vpc_id = subnet['VpcId']
                availability_zone = subnet['AvailabilityZone']
                cidr_block = subnet['CidrBlock']

                subnet_response = ec2_region.describe_subnets(SubnetIds=[subnet_id])

                available_ips = subnet_response['Subnets'][0]['AvailableIpAddressCount']

                #print(f"Available IP Addresses: {available_ips}")
        response = client.get_service_quota(
                        ServiceCode='vpc',
                        QuotaCode='L-407747CB'
        )
        if(int(response['Quota']['Value']-count_subnet)==0):
                print("Subnet quota exhausted")
        else:
                print("Subnet quota available")
        print()

# Count Nat gateways
def list_nat_gateways():
        nat_gateways = ec2_region.describe_nat_gateways()
        count_nat_gateways = 0
        for gateway in nat_gateways['NatGateways']:
                count_nat_gateways += 1
               
        response = client.get_service_quota(
                        ServiceCode='vpc',
                        QuotaCode='L-FE5A380F'
        )        
      
        if(int(response['Quota']['Value']-count_nat_gateways)==0):
                print("Nat gateway quota exhausted")
        else:
                print("Nat gateway quota available")
        print()

# Count the number of Elastic IP addresses
def list_elastic_ip():
        response = ec2.describe_addresses()
        count_eip = 0
        for address in response['Addresses']:
               #if 'AssociationId' not in address:  
                count_eip += 1
        response = client.get_service_quota(
                ServiceCode='ec2',
                QuotaCode='L-0263D0A3'
        )
        if(int(response['Quota']['Value']-count_eip)==0):
                print("Elastic IP quota exhausted")
        else:
                print("Elastic IP quota available")
        print()

# count number of s3 buckets
def list_s3():
        s3_count = len(s3.list_buckets()['Buckets'])
        response = client.get_aws_default_service_quota(
                      ServiceCode='s3',
                      QuotaCode='L-DC2B2D3D'
        )
        if(int(response['Quota']['Value']-s3_count)==0):
                print("S3 quota exhausted")
        else:
                print("S3 quota available")
        print()

#count number of rds db instances
def list_rds():
        rds_count = len(rds.describe_db_instances()['DBInstances'])
        response = client.get_service_quota(
                      ServiceCode='rds',
                      QuotaCode='L-7B6409FD'
        )
        if(int(response['Quota']['Value']-rds_count)==0):
                print("Rds quota exhausted")
        else:
                print("Rds quota available")
        print()

list_vpc()
list_subnet()
list_nat_gateways()
list_elastic_ip()
list_s3()
list_rds()