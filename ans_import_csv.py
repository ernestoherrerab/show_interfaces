#! /usr/bin/env python
import csv
import yaml
import json
from pathlib import Path


def read_csv(file):
    """Reads CSV file and stores it in a variable"""
    with open(file) as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        next(csv_data)
        csv_data_list = []
        for row in csv_data:
            csv_data_list.append(row)
        return csv_data_list


def create_inventory(hosts_data):
    """Creates the inventory file"""
    path_file = "hosts"
    with open(path_file, "w") as open_file:
        hosts_file = open_file.write(hosts_data)
    return hosts_file


def format_hosts():
    """Formats the inventory"""
    path_file = "hosts"
    host_file = open(path_file)
    lines = host_file.readlines()
    host_file.close()
    host_file = open(path_file, "w")
    for line in lines:
        host_file.write(line[1:])
    host_file.close()


def main():
    """Imports data from a CSV file and puts it in YAML format 
       for inventory
    """
    csv_folder = Path("data/")
    csv_path_file = csv_folder / "Mgmt_IPs.csv"
    csv_data = read_csv(csv_path_file)
    empty_host = {}
    host_list_dict = []
    for host_list in csv_data:
        empty_host[host_list[0]] = {
            "hostname": host_list[0],
            "groups": [host_list[2] + "_devices"],
        }
        host_list_dict.append(empty_host)
        empty_host = {}
    hosts_yaml = yaml.dump(host_list_dict, default_flow_style=False)
    host_yaml_init = "----\n\n" + hosts_yaml
    create_inventory(str(host_yaml_init))
    format_hosts()


if __name__ == "__main__":
    main()
