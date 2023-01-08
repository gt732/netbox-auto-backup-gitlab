# netbox-auto-backup-gitlab

# Automated Configuration Backup and Gitlab Upload
This code is designed to retrieve configuration backups from a set of networking devices and upload them to a version control repository (Gitlab).

# How it works
This code is a script for retrieving configuration backups from networking devices and uploading them to a version control repository (Gitlab). It uses the Nornir automation framework and the Napalm plugin to connect to devices and retrieve their configuration. The script also includes a function for retrieving a list of devices from the Netbox API and writing them to a CSV file which can be used as an inventory by Nornir. Finally, the script includes a series of Git commands to add the new configuration files to the repository, commit them with a message, and push them to the remote repository.

# Use any automated scheduler of your choice to run the python script
