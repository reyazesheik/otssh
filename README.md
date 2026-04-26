# OTSSH - SSH Connection Manager (Bash)

## Description

OTSSH is a Bash-based command-line utility to manage SSH connections using simple names.

## Features

* Add SSH connection
* List connections
* List with details
* Update connection
* Delete connection
* Connect to server

## Usage

### Add

./otssh.sh add -n server1 -h 192.168.1.1 -u user

### List

./otssh.sh ls

### List with details

./otssh.sh ls -d

### Update

./otssh.sh update -n server1

### Delete

./otssh.sh rm server1

### Connect

./otssh.sh connect server1

## Storage

All connections are stored in:
~/.otssh_config

## Author

Reyaze Sheik
