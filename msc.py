from constants import MSCURL
from utils import Driver
import time


class MSC:
    def __init__(self, bl_number):
        # Instantiates Driver class and opens url in headless browser
        self.driver = Driver()
        self.driver.get_page(MSCURL)
        self.driver.add_cookies({'name': 'newsletter-signup-cookie', 'value': 'temp-hidden'})
        self.bl_number = bl_number

        # Locates search box and inputs BL number
        element = self.driver.find_id_element("ctl00_ctl00_plcMain_plcMain_TrackSearch_txtBolSearch_TextField")
        element.send_keys('MEDUQ' + self.bl_number)  # BL Format: 1312550

        # Locates search button and clicks
        search_button_xpath = '//*[@id="ctl00_ctl00_plcMain_plcMain_TrackSearch_pnlTrackSearchForm"]/div/div[2]'
        search = self.driver.find_xpath_element(search_button_xpath)
        search.click()

    def get_loading_port(self):
        pol_xpath = '//*[@id="ctl00_ctl00_plcMain_plcMain_rptBOL_ctl00_pnlBOLContent"]/table/tbody[1]/tr/td[3]'
        load_port_element = self.driver.find_xpath_element(pol_xpath)
        loading_port = load_port_element.text.split(',')
        return loading_port[0]

    def get_departure_date(self):
        etd_xpath = '//*[@id="ctl00_ctl00_plcMain_plcMain_rptBOL_ctl00_pnlBOLContent"]/table/tbody[1]/tr/td[1]/span'
        etd_element = self.driver.find_xpath_element(etd_xpath)
        departure_date = etd_element.text.split('/')
        return departure_date[1] + departure_date[0]

    def get_discharge_port(self):
        pod_xpath = '//*[@id="ctl00_ctl00_plcMain_plcMain_rptBOL_ctl00_rptContainers_ctl01_pnlContainer"]' \
                    '/table[2]/tbody/tr[1]/td[1]/span'
        pod_element = self.driver.find_xpath_element(pod_xpath)
        discharge_port = pod_element.text.split(',')[:2]
        return ','.join(discharge_port)

    def get_arrival_date(self):
        global arrival_date, arrival_info
        eta_xpath = '//*[@id="ctl00_ctl00_plcMain_plcMain_rptBOL_ctl00_rptContainers_ctl01_pnlContainer"]/table[2]/tbody/tr'
        eta_elements = self.driver.find_xpath_elements(eta_xpath)
        for element in eta_elements:
            if 'Discharged' or 'Arrival' in element.text:
                arrival_info = element.text.split(' ')
                break
        for item in arrival_info:
            if '/' in item:
                arrival_date = item.split('/')
        return arrival_date[1] + arrival_date[0]

    def get_containers(self):
        # Locates containers (e.g. ABCD1234567) elements on page
        container_list = []
        container_elements = self.driver.find_xpath_elements('//*[@class="containerToggle"]')
        time.sleep(1)
        i = 1
        for element in container_elements:
            element.click()
            raw_container = element.text.split(' ')
            container_number = raw_container[1]
            container_size_element = self.driver.find_xpath_element('//*[@id="ctl00_ctl00_plcMain_plcMain_rptBOL_ctl00_'
                                                                    'rptContainers_ctl0{}_pnlContainer"]/table[1]/tbody[1]'
                                                                    '/tr/td[1]/span'.format(i))
            container_size = container_size_element.text[:2]
            container_list.append((container_number, container_size))
            i += 1
        cookie_popup = self.driver.find_xpath_element('//*[@id="cookiePolicyModal"]/div/div/a')
        cookie_popup.click()
        container_elements[0].click()
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

