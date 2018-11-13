from constants import COSCOURL
from utils import Driver


class Cosco:
    def __init__(self, bl_number):
        self.driver = Driver()
        dummy_url = '/error404'
        self.bl_number = bl_number # BL format : 6194326880
        self.driver.get_page(COSCOURL+dummy_url)
        self.driver.add_cookies()
        self.driver.get_page(COSCOURL+'/cargoTracking')

        # Locates search box and inputs BL number
        search_element = self.driver.find_xpath_element('//*[@id="wrap"]/input')
        search_element.send_keys(bl_number)

        # Locates search button and clicks
        search_xpath = '/html/body/div[1]/div[4]/div[1]/div/div[1]/div/div[2]/form/div/div[2]/button'
        search_button = self.driver.find_xpath_element(search_xpath)
        search_button.click()

        # Locates table containing majority of information
        main_info_table = self.driver.find_class_element('ivu-c-detailPart')
        main_info_text = main_info_table.text
        raw_info = main_info_text.replace(' ', '')
        self.main_info = raw_info.split('\n')

        # Locates table containing secondary information
        secondary_xpath = '/html/body/div[1]/div[4]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[2]/div'
        secondary_table = self.driver.find_xpath_element(secondary_xpath)
        secondary_info_text = secondary_table.text
        self.secondary_info = secondary_info_text.split('\n')

    def get_cosco_pol(self):
        raw_pol = self.main_info[9]
        load_port = raw_pol.split('-')
        return load_port[0]

    def get_cosco_etd(self):
        raw_etd = self.secondary_info[7]
        raw_etd = raw_etd.replace('-', ' ')
        raw_etd_split = raw_etd.split(' ')
        etd = raw_etd_split[1] + raw_etd_split[2]
        return etd

    def get_cosco_pod(self):
        raw_pod = self.main_info[11]
        discharge_port = raw_pod.split('-')
        return discharge_port[0]

    def get_cosco_eta(self):
        raw_eta = self.secondary_info[-5]
        raw_eta = raw_eta.replace('-', ' ')
        raw_eta_split = raw_eta.split(' ')
        eta = raw_eta_split[1] + raw_eta_split[2]
        return eta

    def get_cosco_containers(self):
        container_xpath = '/html/body/div[1]/div[4]/div[1]/div/div[2]' \
                          '/div/div/div[2]/div[1]/div[5]/div/div/div[2]/table/tbody/tr'
        container_table = self.driver.find_xpath_elements(container_xpath)
        container_list = []
        for container in container_table:
            raw_container = container.text
            raw_container = raw_container.split('\n')
            container_number = raw_container[0]
            container_type = raw_container[1]
            container = (container_number, container_type)
            container_list.append(container)
        return container_list

    def get_cosco_telex(self):
        telex = self.main_info[23]
        if telex == 'SeaWayBill':
            telex_released = 'Yes'
        else:
            telex_released = 'No'
        return telex_released

    def get_all_cosco_info(self):
        port_of_discharge = self.get_cosco_pod()
        port_of_loading = self.get_cosco_pol()
        telex = self.get_cosco_telex()
        etd = self.get_cosco_etd()
        eta = self.get_cosco_eta()
        containers = self.get_cosco_containers()
        return {'MBL': self.bl_number, 'Info': {'POL': port_of_loading,
                                                'ETD': etd,
                                                'POD': port_of_discharge,
                                                'ETA': eta,
                                                'Containers': containers,
                                                'TELEX': telex}}
