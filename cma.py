from constants import CMAURL
from utils import make_soup


class CMA:
    def __init__(self, bl_number):
        url = CMAURL.format(bl_number)
        self.response = make_soup(url)

    def get_loading_port(self):
        pass

    def get_departure_date(self):
        pass

    def get_discharge_port(self):
        pass

    def get_arrival_time(self):
        pass

    def get_cma_containers(self):
        container_numbers = [container.text for container in self.response('td', {'data-ctnr': 'id'})]
        container_sizes = [size.text for size in self.response('td', {'data-ctnr': 'size'})]
        containers = zip(container_numbers, container_sizes)
        return containers


cma = CMA('CNSE416431')
info = cma.get_cma_containers()
print(info)





