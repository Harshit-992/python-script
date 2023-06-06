import yaml
import shutil

def copy_yaml_file(source_path, destination_path):
    shutil.copy2(source_path, destination_path)

def modify_yaml_one(file_path,a,user_input):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    data[a] = user_input
    with open(file_path, 'w') as file:
        yaml.dump(data, file,sort_keys=False)

def modify_yaml_two(file_path,a,b,user_input):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    data[a][b] = user_input
    with open(file_path, 'w') as file:
        yaml.dump(data, file,sort_keys=False)

def modify_yaml_three(file_path,a,b,c,user_input):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    data[a][b][c] = user_input
    with open(file_path, 'w') as file:
        yaml.dump(data, file,sort_keys=False)

def modify_yaml_four(file_path,a,b,c,d,user_input):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    data[a][b][c][d] = user_input
    with open(file_path, 'w') as file:
        yaml.dump(data, file,sort_keys=False)

def modify_yaml_key(file_path, old_key, new_key):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    modified = False
    def modify_data(data):
        nonlocal modified
        if isinstance(data, dict):
            for key, value in list(data.items()):
                if key == old_key:
                    data[new_key] = data.pop(old_key)
                    modified = True
                elif isinstance(value, (dict, list)):
                    modify_data(value)

    modify_data(data)

    if modified:
        with open(file_path, 'w') as file:
            yaml.safe_dump(data, file,sort_keys=False)
        print(f"Key '{old_key}' has been changed to '{new_key}' in the YAML file.")
    else:
        print(f"No occurrences of the key '{old_key}' found in the YAML file.")
#copying config-template.yml
source_file = 'config-template.yml'
destination_file = input("Enter the new file name:") + '.yml' 
copy_yaml_file(source_file, destination_file)

#role
user_input = input("Enter the aws role:")      
modify_yaml_four(destination_file,"workspaces","vr-demo","aws","role",user_input)
#account_id
user_input = input("Enter the aws role:")      
modify_yaml_four(destination_file,"workspaces","vr-demo","aws","account_id",user_input)
#change region 
user_input = input("Enter the aws role:")      
modify_yaml_four(destination_file,"workspaces","vr-demo","aws","region",user_input)
#account_name
user_input = input("Enter the account_name:")      
modify_yaml_three(destination_file,"workspaces","vr-demo","account_name",user_input)
#key_name
user_input = input("Enter the key_name:")      
modify_yaml_three(destination_file,"workspaces","vr-demo","key_name",user_input)
#project_name
user_input = input("Enter the project_name:")      
modify_yaml_three(destination_file,"workspaces","vr-demo","project_name",user_input)
#environment_name
user_input = input("Enter the project_name:")      
modify_yaml_three(destination_file,"workspaces","vr-demo","environment_name",user_input)
#kms_policy role_name
user_input = input("Enter the kms_policy role_name:")      
modify_yaml_four(destination_file,"workspaces","vr-demo","kms_policy","role_name",user_input)
#key
user_input = input("Enter the key:")      
modify_yaml_key(destination_file,"vr-demo",user_input)
