from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_csv.plugins.inventory import CsvInventory
from nornir.core.plugins.inventory import InventoryPluginRegister
import csv
import requests
from rich import print as rprint
from datetime import datetime
import os
import time

netbox_endpoint = os.environ.get('NETBOX_ENDPOINT')
api_token = os.environ.get('API_TOKEN')

now = datetime.now()
year = now.year
month = now.month
day = now.day
sec = now.second


def retrieve_backup():
    InventoryPluginRegister.register("CsvInventoryPlugin", CsvInventory)

    nr = InitNornir(
        config_file="./inventory/config.yaml"
    )
    results = nr.run(task=napalm_get, getters=['get_config'])
    print('*' * 100)
    rprint('[yellow]Connecting to devices to retrieve configuration backup.[/yellow]')
    for device, multi_result in results.items():
        if multi_result[0].failed == False:
            config = multi_result[0].result['get_config']['running']
            with open(f'./networking/network-backups/cisco/{device}/{device}-{month}-{day}-{year}-{sec}', 'w') as f:
                f.write(config)
        else:
            rprint(
                f'[red]Unable to connect to {device}[/red]')
    time.sleep(1)


def git_push():
    print('*' * 100)
    rprint('[yellow]Pushing configs to Gitlab.[/yellow]')
    print('*' * 100)
    os.chdir('./networking')
    os.system('git add .')
    add_result = os.system('git add .')
    if add_result != 0:
        rprint("[red]GIT ERROR ADDING FILES[/red]")
    commit_result = os.system('git commit -m "hello"')
    if commit_result != 0:
        rprint("[red]GIT ERROR COMMITTING[/red]")
    print(commit_result)
    push_result = os.system('git push')
    if push_result != 0:
        rprint("[red]GIT ERROR PUSHING[/red]")
    print(push_result)
    print('*' * 100)
    rprint('[green]Configuration backups retrieved and uploaded to Gitlab successfully.[/green]')
    print('*' * 100)


def netbox_get_devices():
    try:
        url = f"http://{netbox_endpoint}/api/dcim/devices/"
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Token {api_token}"}
        response = requests.get(url, headers=headers).json()
        print('*' * 100)
        rprint('[yellow]Getting Devices from Netbox Inventory.[/yellow]')
        with open('./inventory/hosts.csv', 'w', encoding='UTF8', newline='') as file:
            header = ['name', 'hostname', 'platform']
            writer = csv.writer(file)
            writer.writerow(header)
            for i in response['results']:
                name = i['display']
                ip_address = i['primary_ip']['address'].split("/")[0]
                data = [f'{name}', f'{ip_address}', 'ios']
                writer.writerow(data)
        rprint('[green]Nornir host.csv created.[/green]')
    except Exception as e:
        print(e)
        rprint("[red]Error getting devices from Netbox.[/red]")


if __name__ == '__main__':
    netbox_get_devices()
    retrieve_backup()
    git_push()
