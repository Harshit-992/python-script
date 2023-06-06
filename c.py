import yaml

def modify_yaml_file(val,file_path, old_key, new_key):
    # Load the YAML file
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Modify the data for all occurrences of the key
    modified = False
    def modify_data(data):
        nonlocal modified
        if val == "value":
            if isinstance(data, dict):
                for key, value in list(data.items()):
                    if key == old_key:
                        data[key] = new_key
                        modified = True
                    elif isinstance(value, (dict, list)):
                        modify_data(value)
        else:            
            if isinstance(data, dict):
                for key, value in list(data.items()):
                    if key == old_key:
                        data[new_key] = data.pop(old_key)
                        modified = True
                    elif isinstance(value, (dict, list)):
                         modify_data(value)
    # Call the modify_data function to modify all occurrences
    modify_data(data)

    # Write the modified data back to the YAML file
    if modified:
        with open(file_path, 'w') as file:
            yaml.safe_dump(data, file)
        
    else:
        print(f"No occurrences of the key '{old_key}' found in the YAML file.")

file_path = 'file.yml'

#vpn_cidr
val = 'value'
input_user = input("Enter the vpn cidr: ")
modify_yaml_file(val,file_path,"vpn_cidr" , input_user)
#account_name
val = 'value'
input_user = input("Enter the account_name: ")
modify_yaml_file(val,file_path,"account_name" , input_user)
#account_id
val = 'value'
input_user = input("Enter the account_id: ")
modify_yaml_file(val,file_path,"account_id" , input_user)
#change region
val = 'value'
input_user = input("Enter the region: ")
modify_yaml_file(val,file_path,"region" , input_user)
#project_name
val = 'value'
input_user = input("Enter the project_name: ")
modify_yaml_file(val,file_path,"project_name" , input_user)
#key change
val = 'key'
new_key = input("Enter the new key name: ")
modify_yaml_file(val,file_path,"nonprod" , new_key)





