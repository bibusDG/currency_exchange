import requests
import kivy
import json
from kivy.config import Config
Config.set('graphics', 'resizable', False)  # for PC app, erase for IPHONE App
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import Screen


with open('jsons\\countries.json', errors='ignore') as countries:
    country_code = json.load(countries)
    country_data = country_code['countries']['country']


class MainScreen(Screen):

    country_A_active = 0
    country_B_active = 0
    country_A_currency = ''
    country_B_currency = ''
    country_A_name = ''
    country_B_name = ''
    value = 0
    cost = 0

    currency_code = {}

    def currency_country(self, letters):
        self.currency_code = {}
        # print(letters)
        for names in country_data:
            if names['countryName'][0:len(letters)] == letters or names['countryName'][
                                                 0:len(letters)].lower() == letters:
                self.currency_code[names['countryName']] = names['currencyCode']

    def text_on_button(self, name):
        try:
            if name == 'input_A':
                self.country_A_active = 1
                self.country_B_active = 0
                self.ids.input_A.hint_text = str(list(self.currency_code.keys())[0])
                # self.country_A_currency =
            if name == 'input_B':
                self.country_A_active = 0
                self.country_B_active = 1
                self.ids.input_B.hint_text = str(list(self.currency_code.keys())[0])
        except IndexError:
            pass

    def confirm_country(self, text):
        if self.country_A_active == 1:
            self.ids.input_A.text = str(self.ids.input_A.hint_text)
            self.country_A_currency = str(self.currency_code[self.ids.input_A.text])
            self.country_A_name = str(self.ids.input_A.hint_text)
        if self.country_B_active == 1:
            self.ids.input_B.text = str(self.ids.input_B.hint_text)
            self.ids.input_C.hint_text = 'Price in ' + str(self.currency_code[self.ids.input_B.text])
            self.country_B_currency = str(self.currency_code[self.ids.input_B.text])
            self.country_B_name = str(self.ids.input_B.hint_text)

    def value_cost(self, text):
        self.cost = int(text)

    def price_calculation(self, text):

        get_currency = requests.get('https://freecurrencyapi.net/api/v2'
                                    '/latest?apikey=a897bcc0-947e-11ec-88ff-ef8e9477feef&base_currency=' + str(self.country_B_currency))

        self.value = round(float(get_currency.json()['data'][str(self.country_A_currency)]), 1)

        self.ids.final_price.text = str(self.value * int(self.cost)) + ' ' + str(self.country_A_currency)
        pass

    pass


class Main_App(MDApp):

    def build(self):
        Window.size = (450, 750)
        GUI = Builder.load_file('main.kv')
        return GUI


if __name__ == '__main__':
    Main_App().run()
