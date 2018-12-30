from constants import DRIVERLOC, APLURL, MONTHTONUMDICT
from selenium import webdriver
from datetime import datetime


class APL:
    def __init__(self, bl_number):
        self.bl_number = bl_number  # BL Format : 063986479
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome(DRIVERLOC, options=self.options)  # Instantiates headless Chrome browser
        self.driver.get(APLURL.format(self.bl_number))
        self.driver.switch_to.frame(self.driver.find_element_by_name('bodyframe'))
        self.routing_table = self.driver.find_elements_by_xpath('//*[@id="bodytable"]/tbody/tr[3]/'
                                                                'td/form/table[1]/tbody/tr')

    def get_loading_port(self):
        """ Port of Loading usually located in China """
        pol_xpath = '//*[@id="bodytable"]/tbody/tr[3]/td/form/table[1]/tbody/tr[3]/td[2]/a'
        pol_element = self.driver.find_element_by_xpath(pol_xpath)
        raw_pol = pol_element.text.split(',')
        load_port = raw_pol[0]
        return load_port

    def get_departure_date(self):
        """ Estimated time of departure from Port of Loading """
        etd_xpath = '//*[@id="bodytable"]/tbody/tr[3]/td/form/table[1]/tbody/tr[3]/td[5]'
        etd_element = self.driver.find_element_by_xpath(etd_xpath)
        raw_etd = etd_element.text
        raw_etd = raw_etd[:-6].split(' ')
        month = MONTHTONUMDICT[raw_etd[1]]
        day = raw_etd[0]
        etd = month + day
        return etd

    def get_discharge_port(self):
        """ Discharge port usually located in the US """
        pod_xpath = '//*[@id="bodytable"]/tbody/tr[3]/td/form/table[1]/tbody/tr[{}]/td[2]/a'.format(
                len(self.routing_table) - 1)
        pod_element = self.driver.find_element_by_xpath(pod_xpath)
        raw_pod = pod_element.text
        if ',' in raw_pod:
            raw_pod = raw_pod.split(',')
            discharge_port = raw_pod[0]
        else:
            discharge_port = raw_pod
        return discharge_port

    def get_arrival_date(self):
        """ Estimated time of arrival for container to reach port of discharge """
        eta_info = self.routing_table[len(self.routing_table) - 2]
        raw_eta = eta_info.text.split(')')
        raw_eta = raw_eta[1].lstrip()
        raw_eta = raw_eta.split(' ')
        month = MONTHTONUMDICT[raw_eta[1]]
        day = raw_eta[0]
        eta = month + day
        return eta

    def get_container_number(self):
        """ Locates containers (e.g. ACBD1234567) and appends to list """
        container_list = []
        container_table = self.driver.find_elements_by_xpath('//*[@id="pnlGrid"]/table/tbody/tr')
        for container in container_table[1:]:
            if container.text != '':
                container_info= container.text.split(' ')
                container = container_info[0].replace('-', "")
                container_size = container_info[3]
                raw_container_type = container_info[5]
                if '9' in raw_container_type:
                    container_type = '\'HQ'
                elif '8' in raw_container_type:
                    container_type = '\''
                else:
                    print('Double check container type')
                container_specs = container_size + container_type
                container_list.append((container, container_specs))
            else:
                pass
        return container_list

    def get_all_info(self):
        containers = self.get_container_number()
        load_port = self.get_loading_port()
        etd = self.get_departure_date()
        discharge_port = self.get_discharge_port()
        eta = self.get_arrival_date()
        return {'MBL': self.bl_number, 'Info': {'POL': load_port,
                                                'ETD': etd,
                                                'POD': discharge_port,
                                                'ETA': eta,
                                                'Containers': containers}}


# Use this block to test speeds

# startTime = datetime.now()
# apl_list = ['062605013', '101225200', '660349252', '660349346', '660349375', '660349383', '751064070', '751064107']
# for mbl in apl_list:
#     apl = APL(mbl)
#     print(apl.get_all_info())
# print(datetime.now() - startTime)
