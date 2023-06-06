#!/bin/bash

# Prompt the user for the path to the text file
read -p "Enter name: " name
read -p "Enter path to the text file: " file_path
var=""
# Read key-value pairs from the text file
while IFS='=' read -r key value; do
   var="--set $key=$value $var"
  # Perform any desired operations with the key and value here
done < "$file_path"

helm install $var $name ./
                     