import tkinter
import requests
from tkinter import ttk, LEFT, BOTH
from PIL import ImageTk, Image
from io import BytesIO
from fonts_and_colors import large_font, small_font, search_color, below_10, between_10_and_0, \
    between_0_and_10, between_10_and_20, between_20_and_30, over_30
from country_code import country_list, country_code
import ipinfo


class WeatherGui(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title('Weather App')
        self.geometry('550x600')
        self.iconbitmap('weather.ico')
        self.option_add('*TCombobox*Listbox.font', small_font)
        self.resizable(False, False)

        self.current_background_color = below_10

        self.city_name_label = tkinter.Label(self, text='City Name: ', font=small_font)
        self.city_name_label.pack(padx=60, pady=10, anchor='w')

        self.city_name_entry = tkinter.Entry(self, width=38, font=small_font, borderwidth=4)
        self.city_name_entry.pack(padx=60, pady=(0, 10), anchor='center')

        self.country_name_label = tkinter.Label(self, text='Country Name: ', font=small_font)
        self.country_name_label.pack(padx=60, pady=(0, 10), anchor='w')

        self.country_name_dropdown = ttk.Combobox(self, justify=LEFT, width=37, values=country_list, font=small_font)
        self.country_name_dropdown.pack(padx=60, pady=(0, 10), anchor='center')
        self.country_name_dropdown.set(country_list[0])

        self.search_button = tkinter.Button(self, text='Search', command=self.search, font=small_font, borderwidth=2,
                                            bg=search_color, activebackground=search_color)
        self.search_button.pack(pady=(10, 10), padx=60, anchor='center', fill=BOTH)

        self.country_name_label_2 = tkinter.Label(self, font=small_font)
        self.country_name_label_2.pack(pady=10, padx=60)

        self.description_label = tkinter.Label(self, font=small_font)
        self.description_label.pack(pady=(0, 10), padx=60)

        self.temp_label = tkinter.Label(self, font=large_font)
        self.temp_label.pack(pady=(0, 10), padx=60)

        self.image = ''

        self.image_label = tkinter.Label(self)
        self.image_label.pack(pady=(0, 20), padx=60)

        self.add_information_in_gui_at_first_run()

    def search(self):
        """access openweathermap API based on city or/and country"""
        self.country_name_dropdown.selection_clear()

        api_key = 'b524906f00443e7ccc82cd58e2454296'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={self.city_name_entry.get()}, ' \
              f'{country_code.get(self.country_name_dropdown.get())}&appid={api_key}&units={"metric"}'
        response = requests.request('GET', url).json()
        self.make_gui(response)

    def make_gui(self, response: dict):
        """place information from API response in GUI"""

        current_temp = float(response['main']['temp'])
        self.find_background_color(current_temp)

        self.config(bg=self.current_background_color)

        self.city_name_label.configure(bg=self.current_background_color)

        self.country_name_label.configure(bg=self.current_background_color)

        self.country_name_label_2.configure(text=f"{response['name']}, {response['sys']['country']}",
                                            bg=self.current_background_color)

        self.description_label.configure(text=f"{response['weather'][0]['description']}", font=small_font,
                                         bg=self.current_background_color)

        self.temp_label.configure(text=f"{response['main']['temp']}°C", bg=self.current_background_color)

        # create url based on current_icon_id
        url_icon = f'https://openweathermap.org/img/wn/{response["weather"][0]["icon"]}@4x.png'
        # download icon
        icon_response = requests.get(url_icon, stream=True)
        # convert icon in a format understood by tkinter and python
        image_data = icon_response.content
        # open image data in a format that can be accessed as an image
        self.image = ImageTk.PhotoImage(Image.open(BytesIO(image_data)))
        # set upper image to image_label
        self.image_label.configure(image=self.image, bg=self.current_background_color)

    def add_information_in_gui_at_first_run(self):
        """access ipify API to find public ip and based on lat and long of current location access openweather API, get
         information and put them in GUI at first run of app"""

        # find public ip address
        ip_response = requests.get("https://api.ipify.org?format=json").json()
        current_public_ip = ip_response['ip']
        # obtain current location
        access_token = 'e2491b6b12485f'
        handler = ipinfo.getHandler(access_token)
        details = handler.getDetails(current_public_ip)
        lat = round(float(details.loc.split(',')[0]), 2)
        lon = round(float(details.loc.split(',')[1]), 2)

        api_key = 'b524906f00443e7ccc82cd58e2454296'
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={str(lat)}&lon={str(lon)}&appid={api_key}' \
              f'&units={"metric"}'
        response = requests.request('GET', url).json()
        self.make_gui(response)

    def find_background_color(self, current_temp: float):
        """based on current_temp find background color"""
        if current_temp < -10:
            self.current_background_color = below_10
        elif -10 <= current_temp <= 0:
            self.current_background_color = between_10_and_0
        elif 0 < current_temp <= 11:
            self.current_background_color = between_0_and_10
        elif 11 < current_temp <= 21:
            self.current_background_color = between_10_and_20
        elif 21 < current_temp <= 30:
            self.current_background_color = between_20_and_30
        elif current_temp > 30:
            self.current_background_color = over_30
