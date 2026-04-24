#!/usr/bin/env python3

import json
import os
import argparse
import subprocess

CONFIG_FILE = os.path.expanduser("~/.otssh_config.json")


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def build_ssh_command(c):
    cmd = ["ssh"]

    if c.get("identity"):
        cmd += ["-i", c["identity"]]

    if c.get("port"):
        cmd += ["-p", str(c["port"])]

    cmd.append(f"{c['user']}@{c['host']}")

    return cmd


def add_connection(args):
    data = load_config()

    data[args.name] = {
        "host": args.host,
        "user": args.user,
        "port": args.port or 22,
        "identity": args.identity
    }

    save_config(data)
    print(f"{args.name} added")


def list_connections(args):
    data = load_config()

    for name, c in data.items():
        if args.detail:
            cmd = "ssh "
            if c.get("identity"):
                cmd += f"-i {c['identity']} "
            if c.get("port"):
                cmd += f"-p {c['port']} "
            cmd += f"{c['user']}@{c['host']}"
            print(f"{name}: {cmd}")
        else:
            print(name)


def update_connection(args):
    data = load_config()

    if args.name not in data:
        print("Server not found")
        return

    if args.host:
        data[args.name]["host"] = args.host
    if args.user:
        data[args.name]["user"] = args.user
    if args.port:
        data[args.name]["port"] = args.port
    if args.identity:
        data[args.name]["identity"] = args.identity

    save_config(data)
    print(f"{args.name} updated")


def delete_connection(args):
    data = load_config()

    if args.name in data:
        del data[args.name]
        save_config(data)
        print(f"{args.name} deleted")
    else:
        print("Server not found")


def connect(args):
    data = load_config()

    if args.name not in data:
        print("[ERROR]: Server information is not available, please add server first")
        return

    c = data[args.name]
    cmd = build_ssh_command(c)

    print(f"Connecting to {args.name}...")
    subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(prog="otssh")

    subparsers = parser.add_subparsers(dest="command")

    # add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("-n", "--name", required=True)
    add_parser.add_argument("-H", "--host", required=True)
    add_parser.add_argument("-u", "--user", required=True)
    add_parser.add_argument("-p", "--port", type=int)
    add_parser.add_argument("-i", "--identity")
    add_parser.set_defaults(func=add_connection)

    # list
    list_parser = subparsers.add_parser("ls")
    list_parser.add_argument("-d", "--detail", action="store_true")
    list_parser.set_defaults(func=list_connections)

    # update
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("-n", "--name", required=True)
    update_parser.add_argument("-H", "--host")
    update_parser.add_argument("-u", "--user")
    update_parser.add_argument("-p", "--port", type=int)
    update_parser.add_argument("-i", "--identity")
    update_parser.set_defaults(func=update_connection)

    # delete
    delete_parser = subparsers.add_parser("rm")
    delete_parser.add_argument("name")
    delete_parser.set_defaults(func=delete_connection)

    # connect
    connect_parser = subparsers.add_parser("connect")
    connect_parser.add_argument("name")
    connect_parser.set_defaults(func=connect)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
