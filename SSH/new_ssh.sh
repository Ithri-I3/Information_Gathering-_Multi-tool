#!/bin/bash

# Check for required arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <username> <ip_address> <password>"
    exit 1
fi

# Assign input arguments to variables
USERNAME=$1
IP_ADDRESS=$2
PASSWORD=$3
LOCAL_EXECUTABLE="SSH/main"  # Path to the executable on your local machine
REMOTE_EXECUTABLE="./main"  # Path to the executable on the remote machine
REMOTE_FILE="system_info.txt"  # File to copy from the remote machine
LOCAL_DESTINATION="."  # Local path where the file will be copied

# Use sshpass to copy the executable to the remote server
sshpass -p "$PASSWORD" scp -o StrictHostKeyChecking=no "$LOCAL_EXECUTABLE" "$USERNAME@$IP_ADDRESS:$REMOTE_EXECUTABLE"

# Check if the copy was successful
if [ $? -ne 0 ]; then
    echo "Failed to copy the executable to the remote machine."
    exit 1
fi

# Use sshpass to connect to the remote server, execute the 'main' executable, and then delete it
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USERNAME@$IP_ADDRESS" "chmod +x $REMOTE_EXECUTABLE && $REMOTE_EXECUTABLE; rm -f $REMOTE_EXECUTABLE"

# Check if the execution and deletion were successful
if [ $? -ne 0 ]; then
    echo "Failed to execute or delete the executable on the remote machine."
    exit 1
fi

echo "Executable ran and was deleted from the remote machine successfully."

# Use sshpass to copy the system_info.txt file from the remote server to the local machine
sshpass -p "$PASSWORD" scp -o StrictHostKeyChecking=no "$USERNAME@$IP_ADDRESS:$REMOTE_FILE" "$LOCAL_DESTINATION"

# Check if the file copy was successful
if [ $? -ne 0 ]; then
    echo "Failed to copy $REMOTE_FILE from the remote machine."
    exit 1
fi

# Delete the system_info.txt file from the remote server
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USERNAME@$IP_ADDRESS" "rm -f $REMOTE_FILE"

# Check if the deletion was successful
if [ $? -ne 0 ]; then
    echo "Failed to delete $REMOTE_FILE from the remote machine."
    exit 1
fi

echo "$REMOTE_FILE copied to local machine and deleted from remote machine successfully."
