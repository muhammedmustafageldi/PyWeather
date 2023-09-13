import requests
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import datetime
import ApiKey

API_KEY = ApiKey.myApiKey

url = 'https://api.openweathermap.org/data/2.5/weather'

root = Tk()


def window_settings():
    root.title(string='PyWeather')
    root.iconbitmap('app_icon.ico')
    root.geometry('900x500+300+200')
    root.resizable(False, False)


def get_widgets():
    # Search Box
    search_bg = Image.open('search.png')
    search_bg_img = ImageTk.PhotoImage(search_bg)

    search_label = Label(root, image=search_bg_img)
    search_label.image = search_bg_img
    search_label.pack(padx=20, pady=20)

    # Search entry
    city_entry = Entry(search_label, justify='center', width=20, font=('poppins', 25, 'bold'), bg='#404040', border=0,
                       fg='white')
    city_entry.place(x=50, y=20)
    city_entry.focus()

    search_icon = Image.open('search_icon.png')
    resized_search_img = search_icon.resize((50, 50), Image.LANCZOS)
    search_icon_img = ImageTk.PhotoImage(resized_search_img)

    search_button = Button(root, image=search_icon_img, borderwidth=0, cursor='hand2', bg='#404040',
                           command=lambda: place_data(city_entry, city_label, icon_label, weather_text,
                                                      desc_and_feel_text, wind_txt, humidity_txt, desc_txt,
                                                      pressure_txt))
    search_button.image = search_icon_img
    search_button.place(x=600, y=34)

    # City and time Label
    location_icon = Image.open('location.png')
    resized_location_img = location_icon.resize((50, 50), Image.LANCZOS)
    location_icon_img = ImageTk.PhotoImage(resized_location_img)

    city_label = Label(root, text='... / ...', font=('poppins', 25, 'bold'), fg='#404040', compound=LEFT,
                       image=location_icon_img)
    city_label.image = location_icon_img
    city_label.place(x=50, y=110)

    # Weather icon
    weather_icon = Image.open('unknown.png')
    resized_weather_img = weather_icon.resize((128, 128), Image.LANCZOS)
    weather_img = ImageTk.PhotoImage(resized_weather_img)

    icon_label = Label(root, image=weather_img)
    icon_label.image = weather_img
    icon_label.place(x=60, y=190)

    # Weather text
    weather_text = Label(root, text='...°', font=('poppins', 65, 'bold'), fg='#404040')
    weather_text.place(x=210, y=195)

    # Desc and feel text
    desc_and_feel_text = Label(root, text='... / ...', font=('poppins', 25, 'bold'), fg='#404040')
    desc_and_feel_text.place(x=400, y=225)

    # Bottom box
    bottom_box_icon = Image.open('bottom_box.png')
    resized_bottom_box = bottom_box_icon.resize((700, 110), Image.LANCZOS)
    bottom_box_img = ImageTk.PhotoImage(resized_bottom_box)

    bottom_box = Label(root, image=bottom_box_img)
    bottom_box.image = bottom_box_img
    bottom_box.pack(side=BOTTOM)

    # Bottom labels
    label_wind = Label(root, text='WIND', font=('Helvetica', 15, 'bold'), fg='white', bg='#404040')
    label_wind.place(x=150, y=410)

    label_humidity = Label(root, text='HUMIDITY', font=('Helvetica', 15, 'bold'), fg='white', bg='#404040')
    label_humidity.place(x=300, y=410)

    label_desc = Label(root, text='DESC', font=('Helvetica', 15, 'bold'), fg='white', bg='#404040')
    label_desc.place(x=450, y=410)

    label_pressure = Label(root, text='PRESSURE', font=('Helvetica', 15, 'bold'), fg='white', bg='#404040')
    label_pressure.place(x=600, y=410)

    # Bottom box txt
    wind_txt = Label(text='...', font=('arial', 20, 'bold'), bg='#404040')
    wind_txt.place(x=155, y=435)

    humidity_txt = Label(text='...', font=('arial', 20, 'bold'), bg='#404040')
    humidity_txt.place(x=325, y=435)

    desc_txt = Label(text='     ...', font=('arial', 17, 'bold'), bg='#404040')
    desc_txt.place(x=430, y=435)

    pressure_txt = Label(text='...', font=('arial', 20, 'bold'), bg='#404040')
    pressure_txt.place(x=630, y=435)


def get_the_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    response = requests.get(url=url, params=params)

    if response.status_code == 200:
        data = response.json()
        city = data['name']
        weather = data['weather'][0]
        main = data['main']

        desc = weather['description']
        icon = weather['icon']
        main_str = weather['main']
        temp = int(main['temp'])
        feels_like = int(main['feels_like'])
        pressure = main['pressure']
        humidity = main['humidity']
        wind = data['wind']['speed']

        data_dict = {'city': city,
                     'desc': desc,
                     'icon': icon,
                     'temp': temp,
                     'feels_like': feels_like,
                     'pressure': pressure,
                     'humidity': humidity,
                     'wind': wind,
                     'main_str': main_str
                     }
        return data_dict

    else:
        print('Error! Request failed. HTTP code: ', response.status_code)
        messagebox.showinfo(title='Error', message='Error. Request failed. Please try again.')


def place_data(city_entry, city_label, icon_label, weather_text, desc_and_feel_text, wind_txt, humidity_txt, desc_txt, pressure_txt):
    city = city_entry.get()
    if city != '':
        # Get data as dict
        data_dict = get_the_weather_data(city)
        # Put data into components
        weather_text.config(text=f"{data_dict.get('temp')}°")
        desc_and_feel_text.config(text=f"{data_dict.get('main_str')} / Feels like {data_dict.get('feels_like')}°")
        wind_txt.config(text=data_dict.get('wind'))
        humidity_txt.config(text=data_dict.get('humidity'))
        desc_txt.config(text=data_dict.get('desc'))
        pressure_txt.config(text=data_dict.get('pressure'))

        # Get current time
        current_time = datetime.datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute

        city_label.config(text=f"{data_dict.get('city')} / {current_hour}:{current_minute}")

        # Get the weather icon
        icon_code = data_dict.get('icon')
        icon_path = f'weather icon/{icon_code}.png'
        selected_icon = Image.open(icon_path)
        resized_selected_icon = selected_icon.resize((128, 128), Image.LANCZOS)
        weather_icon = ImageTk.PhotoImage(resized_selected_icon)
        icon_label.config(image=weather_icon)
        icon_label.image = weather_icon

    else:
        messagebox.showerror(title='Error', message='Please enter a valid location name.')


window_settings()
get_widgets()
root.mainloop()
