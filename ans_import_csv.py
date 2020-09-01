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
    path_file = "hosts_stage.yml"
    with open(path_file, "w") as open_file:
        hosts_file = open_file.write(hosts_data)
    return hosts_file


def clean_yaml_file(input_file, output_file):
    """Clean Yaml files"""
    with open(input_file, 'r') as infile, \
         open(output_file, 'w') as outfile:
        data = infile.read()
        to_clean = ["''"]
        for data_elements in to_clean:
            data = data.replace(data_elements, "")
        outfile.write(data)
    #Path.unlink(input_file)


def main():
    """Imports data from a CSV file and puts it in YAML format 
       for inventory
    """
    csv_folder = Path("data/")
    csv_path_file = csv_folder / "Mgmt_IPs.csv"
    csv_data = read_csv(csv_path_file)
    empty_host = {}
    empty_host['all'] = {}
    empty_host['all']['vars'] = {}
    empty_host['all']['vars']['ansible_python_interpreter'] = '/usr/bin/python3'
    empty_host['all']['children'] = {}   
    for host_list in csv_data:
        if host_list[2] == 'ios':
            if 'ios' in empty_host['all']['children']:
                empty_host['all']['children']['ios']['hosts'][host_list[0]]=''
            else:
                empty_host['all']['children']['ios'] = {}
                empty_host['all']['children']['ios']['hosts'] = {}
                empty_host['all']['children']['ios']['hosts'][host_list[0]] = ''
                empty_host['all']['children']['ios']['vars'] = {}
                empty_host['all']['children']['ios']['vars']['ansible_connection'] = 'network_cli'
                empty_host['all']['children']['ios']['vars']['ansible_network_os'] = 'ios'
                empty_host['all']['children']['ios']['vars']['ansible_user'] = "{{username}}"
                empty_host['all']['children']['ios']['vars']['ansible_ssh_pass'] = "{{password}}"    
    hosts_yaml = yaml.dump(empty_host, default_flow_style=False)
    create_inventory(str(hosts_yaml))
    clean_yaml_file('hosts_stage.yml', 'hosts.yml')
    

if __name__ == "__main__":
    main()
