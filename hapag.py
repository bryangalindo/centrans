from constants import HAPAGURL
import time


class Hapag:
    def __init__(self, driver, bl_number):
        # Instantiates the Driver class and loads url on headless browser
        url = HAPAGURL.format(bl_number) # BL Format : XM1180708438
        self.bl_number = bl_number
        self.driver = driver
        self.driver.get_page(url)

    def get_loading_port(self):
        return self.loading_port_info.split(' ')[2]

    def get_departure_date(self):
        return self.__get_date_process(func=self.loading_port_info)

    def get_discharge_port(self):
        raw_discharge = self.discharge_port_info.split(' ')
        pod_list = []
        for item in raw_discharge[2:]:
            if '2018' in item:
                break
            else:
                pod_list.append(item)
        return ' '.join(pod_list)

    def get_arrival_date(self):
        return self.__get_date_process(func=self.discharge_port_info)

    def get_containers(self):
        # Locates and creates a list of containers (e.g. ABCD1234567)
        container_list = []
        xpath_locator = '//*[@id="tracing_by_booking_f:hl27"]/tbody/tr'
        container_elements = self.driver.find_xpath_elements(xpath_locator)
        for container in container_elements:
            container_info = container.text.split(' ')
            container_size = container_info[0][:2] + '\''
            container_number = container_info[1] + container_info[2]
            container_list.append((container_number, container_size))
        return container_list

    def get_all_info(self):
        containers = self.get_containers()
        time.sleep(1)
        self.__get_logistics_process()
        load_port = self.get_loading_port()
        etd = self.get_departure_date()
        discharge_port = self.get_discharge_port()
        eta = self.get_arrival_date()
        return {'MBL': self.bl_number, 'Info': {'POL': load_port, 'ETD': etd, 'POD': discharge_port,
                                                'ETA': eta, 'Containers': containers}}

    def __get_date_process(self, func):
        port_info = func.split(' ')
        for item in port_info:
            if '-' in item:
                date = item.split('-')
                break
        month = date[1]
        day = date[2]
        return month + day

    def __get_logistics_process(self):
        # Closes cookie popup
        cookie_xpath = '//*[@id="hal-cookieconsent-button"]'
        cookie_button = self.driver.find_xpath_element(cookie_xpath)
        cookie_button.click()

        # Opens main frame where info is located
        button_xpath = '//*[@id="tracing_by_booking_f:hl27"]/tbody/tr'
        button_element = self.driver.find_xpath_element(button_xpath)
        button_element.click()

        # Opens table containing container logistics
        details_button_xpath = '//*[@id="tracing_by_booking_f:hl27:hl53"]'
        details_button = self.driver.find_xpath_element(details_button_xpath)
        details_button.click()

        # Grabs table element with eta, etd, pol, pod
        logistics_table_xpath = '//*[@id="tracing_by_booking_f:hl66"]/tbody/tr'
        logistics_table = self.driver.find_xpath_elements(logistics_table_xpath)

        # Locates row element containing port of load info
        for element in logistics_table:
            if 'Vessel departed' in element.text:
                self.loading_port_info = element.text
                break

        # Locates row element containing discharge port info
        for element in logistics_table:
            if 'Vessel arrival' in element.text:
                self.discharge_port_info = element.text
                break
