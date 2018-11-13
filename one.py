from utils import Driver
from constants import ONEURL
import time
from datetime import datetime


class One:
    def __init__(self, bl_number, driver):
        self.driver = driver
        self.bl_number = bl_number # BL Format : TA8PZ3543400
        self.driver.get_page(ONEURL)

        # Locates search box, inputs params, clicks search button
        search_box = self.driver.find_id_element('searchName')
        search_box.send_keys(self.bl_number)
        search_button = self.driver.find_xpath_element('//*[@id="btnSearch"]')
        search_button.click()

        # Displays servlet with vital logistic data points
        container_link = self.driver.find_xpath_element('//*[@id="1"]/td[4]/a')
        container_link.click()
        time.sleep(2)

        # Locates Sailing Information Box
        self.sailing_elements = self.driver.find_xpath_elements('//*[@id="sailing"]/tbody/tr')

        # Resets text box to search for multiple mbl
        self.driver.find_id_element('searchName').clear()

    def get_oney_pol(self):
        global port_index
        raw_pol = self.sailing_elements[0].text.split(' ')
        for item in raw_pol:
            if ',' in item:
                port_index = raw_pol.index(item)
                break
        load_port = raw_pol[port_index].replace(',', '')
        return load_port

    def get_oney_etd(self):
        global etd_index
        raw_etd = self.sailing_elements[0].text.split(' ')
        for item in raw_etd[:10]:
            if '-' in item:
                etd_index = raw_etd.index(item)
                break
        etd_info = raw_etd[etd_index].split('-')
        etd = etd_info[1] + etd_info[2]
        return etd

    def get_oney_pod(self):
        if len(self.sailing_elements) == 1:
            discharge_port = self.__pod_extraction_process(index=0)
        else:
            discharge_port = self.__pod_extraction_process(index=1)
        return discharge_port

    def get_oney_eta(self):
        if len(self.sailing_elements) == 1:
            eta = self.__eta_extraction_process(index=0)
        else:
            eta = self.__eta_extraction_process(index=1)
        return eta

    def get_oney_containers(self):
        # Locates containers (e.g. ABCD1234567) and appends to list
        containers_xpath = '//*[@id="main-grid"]/tbody'
        container_elements = self.driver.find_xpath_element(containers_xpath)
        time.sleep(.5)   # Text attribute from element would lag
        raw_containers = container_elements.text.split('KGS')
        container_list = []

        for container in raw_containers[:-1]:
            raw_container = container.lstrip(' ')
            raw_container = raw_container.split(' ')
            container_number = raw_container[1]
            container_size = raw_container[3]
            container_type = raw_container[4].strip('.')
            if container_type == 'ST':
                container_type = ''
            container_specs = container_size[:2] + container_type
            container_list.append((container_number, container_specs))
        return container_list

    def get_all_oney_info(self):
        load_port = self.get_oney_pol()
        etd = self.get_oney_etd()
        discharge_port = self.get_oney_pod()
        eta = self.get_oney_eta()
        containers = self.get_oney_containers()
        return {'MBL': self.bl_number, 'Info': {'POL': load_port,
                                                'ETD': etd,
                                                'POD': discharge_port,
                                                'ETA': eta,
                                                'Containers': containers}}

    def __pod_extraction_process(self, index):
        raw_pod = self.sailing_elements[index].text.split(',')
        raw_pod = raw_pod[len(raw_pod) - 3].split(':')
        raw_pod = ''.join([i for i in raw_pod[-1] if not i.isdigit()])
        discharge_port = raw_pod.lstrip(' ')
        return discharge_port

    def __eta_extraction_process(self, index):
        raw_eta = self.sailing_elements[index].text.split(' ')
        for item in raw_eta[10:]:
            if '-' in item:
                eta_index = raw_eta.index(item)
                break
        eta_info = raw_eta[eta_index].split('-')
        eta = eta_info[1] + eta_info[2]
        return eta

oney_list = ['TA8PV8615500', 'TA8PV8631300', 'TA8PV8648400', 'TA8PV8649500', 'TA8PV8651500', 'TA8PV8664900', 'TA8PV8693400', 'TA8PV8694500', 'TA8PVA114600', 'TA8PVA115700', 'TA8PZ2010600', 'TA8PZ2046800', 'TA8PZ3581600', 'TA8PZ3582700', 'TA8PZ3583800', 'TS8NU4149900']
i = 0
driver = Driver()
startTime = datetime.now()
while i != (len(oney_list)):
    for mbl in oney_list:
        one = One(mbl, driver=driver)
        info = one.get_all_oney_info()
        print(info)
        i += 1

one.driver.close
print(datetime.now() - startTime)

