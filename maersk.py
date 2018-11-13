from constants import MAERSKURL
from utils import make_soup
import requests


class Maersk:
    def __init__(self, bl_number):
        self.bl_number = bl_number
        url = MAERSKURL.format(bl_number)
        response = requests.get(url)
        self.json_page = response.json()

    def get_loading_port(self):
        return self.json_page['origin']['city']

    def get_departure_date(self):
        return self.json_page['containers'][0]['locations'][1]['events'][0]['expected_time']

    def get_discharge_port(self):
        return self.json_page['destination']['city']

    def get_arrival_date(self):
        return self.json_page['containers'][0]['eta_final_delivery']

    def get_containers(self):
        container_list = []
        containers_dict = self.json_page['containers']
        for container in containers_dict:
            container_num = container['container_num']
            container_size = container['container_size']
            container_list.append((container_num, container_size))
        return container_list

    def get_all_info(self):
        containers = self.get_containers()
        load_port = self.get_loading_port()
        etd = self.get_departure_date()
        discharge_port = self.get_discharge_port()
        eta = self.get_arrival_date()
        return {'MBL': self.bl_number, 'Info': {'POL': load_port,
                                                'ETD': etd,
                                                'POD': discharge_port,
                                                'ETA': eta,
                                                'Containers': containers}}
