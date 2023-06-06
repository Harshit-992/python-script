import yaml
import shutil

def copy_yaml_file(source_path, destination_path):
    shutil.copy2(source_path, destination_path)

def modify_yaml_file(val,file_path, old_key, new_key):

    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    modified = False
    def modify_data(data):
        nonlocal modified
        if val == "value":
            if isinstance(data, dict):
                for key, value in list(data.items()):
                    if value == old_key:
                        data[key] = new_key
                        modified = True
                    elif isinstance(value, (dict, list)):
                        modify_data(value)
            elif isinstance(data, list):
                for index, item in enumerate(data):
                    if item == old_key:
                        data[index] = new_key
                        modified = True
                    elif isinstance(item, (dict, list)):
                        modify_data(item)        
        else:            
            if isinstance(data, dict):
                for key, value in list(data.items()):
                    if key == old_key:
                        data[new_key] = data.pop(old_key)
                        modified = True
                    elif isinstance(value, (dict, list)):
                         modify_data(value)
    
    modify_data(data)

    # Write the modified data back to the YAML file
    if modified:
        with open(file_path, 'w') as file:
            yaml.safe_dump(data, file,sort_keys=False)
        
    else:
        print(f"No occurrences of the key '{old_key}' found in the YAML file.")

source_file = 'config-template.yml'
env = input("Enter environment:")
region = input("Enter region:") 
destination_file = 'config-' + env + '-' + region + '.yml' 
copy_yaml_file(source_file, destination_file)

val = 'value' 
#ROLE
input_user = input("Enter the aws role: ")
modify_yaml_file(val,destination_file,"ROLE" , input_user)
#KMS_ROLE
modify_yaml_file(val,destination_file,"KMS_ROLE" , input_user)
#ACCOUNT_ID
input_user = input("Enter the aws ACCOUNT_ID: ")
modify_yaml_file(val,destination_file,"ACCOUNT_ID" , input_user)
#REGION
modify_yaml_file(val,destination_file,"REGION" , region)
#ACCOUNT_NAME
input_user = input("Enter the aws account_name: ")
modify_yaml_file(val,destination_file,"ACCOUNT_NAME" , input_user)
#KEY_NAME
input_user = input("Enter the aws key name: ")
modify_yaml_file(val,destination_file,"KEY_NAME" , input_user)
#PROJECT_NAME
project_name = input("Enter the aws project_name: ")
modify_yaml_file(val,destination_file,"PROJECT_NAME" , project_name)
#ENV_NAME
modify_yaml_file(val,destination_file,"ENV_NAME" , env)
#HOSTED_ZONE
input_user = input("Enter the hosted_zone: ")
modify_yaml_file(val,destination_file,"HOSTED_ZONE" , input_user)
#CIDR Range
input_user = input("Enter the CIDR range: ")
modify_yaml_file(val,destination_file,"CIDR" , input_user)
#QUEUE_DB
modify_yaml_file(val,destination_file,"QUEUE_DB" , project_name + "_queue")
#RDS_DB
modify_yaml_file(val,destination_file,"RDS_DB" , project_name + "_db")
#S3_NAME
modify_yaml_file(val,destination_file,"S3_NAME" , project_name + "-datastore")
#EKS_CLUSTER_NAME
modify_yaml_file(val,destination_file,"EKS_CLUSTER_NAME" , project_name + "-cluster")
#MONGO_ADDONS_DB
modify_yaml_file(val,destination_file,"MONGO_ADDONS_DB" , project_name + env)
#AVAILABILTY_ZONE
modify_yaml_file(val,destination_file,"AVAILABILITY_ZONE_1" , region + "a")
modify_yaml_file(val,destination_file,"AVAILABILITY_ZONE_2" , region + "b")
#key change
val = 'key'
modify_yaml_file(val,destination_file,"WORKSPACE", project_name + "-" + env)



