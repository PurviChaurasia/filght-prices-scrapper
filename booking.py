import Booking.constants as const
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from Booking.bookingReport import BookingReport
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd
import csv


# constructor
class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\Users\Purvi\SeleniumDriver", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    #TODO - fix webdriver exception


    def select_flight(self):
        flight = self.find_element(By.CSS_SELECTOR, 'a[data-decider-header="flights"]')
        # time.sleep(10)
        flight.click()
        # self.implicitly_wait(15)

    def select_one_way(self):
        one_way = self.find_element(By.CSS_SELECTOR, 'div[data-testid="searchbox_controller_trip_type_ONEWAY"]')
        one_way.click()

    def select_destination(self, place_to_go):
        selected_field = self.find_element(By.CLASS_NAME, "css-g0pg3f-SearchboxInput")
        selected_field.click()
        input_field = self.find_element(By.CSS_SELECTOR, 'input[data-testid = "searchbox_destination_input"]')
        input_field.clear()
        input_field.send_keys(place_to_go)
        first_result = self.find_element(By.CLASS_NAME, "css-2r1cd1")
        first_result.click()

    def select_date(self, depart_date):
        select_button = self.find_element(By.CSS_SELECTOR, 'button[aria-label = "Depart"]')
        select_button.click()
        depart_date = self.find_element(By.CSS_SELECTOR, f'td[data-date="{depart_date}"]')
        depart_date.click()

    def select_class(self, class_name = "Economy"):
        select_class = self.find_element(By.CLASS_NAME, "css-1k0jlfl")
        select_class.click()

        if class_name != 'Economy':
            selected_class = self.find_element(By.CSS_SELECTOR, f'option[value = "{class_name.upper()}"]')
            selected_class.click()

    def select_passengers(self, count=1):
        select_adults = self.find_element(By.CSS_SELECTOR, 'div[data-testid = "input_occupancy_desktop_passengers_trigger"]')
        select_adults.click()

        '''
        while True:
            decrease_adults = self.find_element(By.CSS_SELECTOR, 'button[data-testid = "input_occupancy_modal_adults_decrease"]')
            decrease_adults.click()

            adults_value_element = self.find_element(By.CLASS_NAME, "css-1uzx2ul")
            adults_value = adults_value_element.get_attribute('div')
            if adults_value == 1:
                break
        '''
        increase_adults = self.find_element(By.CSS_SELECTOR, 'button[data-testid = "input_occupancy_modal_adults_increase"]')
        for _ in range(count-1):
            increase_adults.click()

    def select_search(self):
        select = self.find_element(By.CSS_SELECTOR, 'button[data-testid = "searchbox_submit"]')
        select.click()

    def get_data(self):
        airline = []
        departure = []
        arrival = []
        price = []
        time = []
        for i in range(0, 15):
            first_flight = self.find_element(By.ID, f"flightcard-{i}").find_element(By.CLASS_NAME, "css-1dimx8f").find_element(By.CLASS_NAME, "Text-module__root--variant-small_1___3ikf7").get_attribute('innerHTML').strip()
            depart_time = self.find_element(By.ID, f"flightcard-{i}").find_element(By.CSS_SELECTOR, 'div[style = "text-align: left;"]').find_element(By.CLASS_NAME, "Text-module__root--variant-strong_1___1HBHI").get_attribute('innerHTML').strip()
            arrival_time = self.find_element(By.ID, f"flightcard-{i}").find_element(By.CSS_SELECTOR, 'div[style = "text-align: right;"]').find_element(By.CLASS_NAME, "Text-module__root--variant-strong_1___1HBHI").get_attribute('innerHTML').strip()
            duration = self.find_element(By.ID, f"flightcard-{i}").find_element(By.CLASS_NAME, "css-1wnqz2m").find_element(By.CSS_SELECTOR, 'div[data-testid="flight_card_segment_duration"]').get_attribute('innerHTML').strip()
            cost = self.find_element(By.ID, f"flightcard-{i}").find_element(By.CLASS_NAME, "css-1ltp57x").find_element(By.CSS_SELECTOR, 'div[data-test-id="flight_card_price_main_price"]').get_attribute('innerHTML').strip()
            airline.append(first_flight)
            departure.append(depart_time)
            arrival.append(arrival_time)
            price.append(cost)
            time.append(duration)
        out = {"Airline": airline, "Departure": departure, "Arrival": arrival, "Price":price}
        df = pd.DataFrame.from_dict(out)

        print(df)














