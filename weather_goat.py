import requests
import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
from itertools import count, cycle
import random

#-------------------------------------------------------------------------------
#!--- GLOBALS
current_weather = {}
weather_canv_image = ""
goat_image_1 = ""
#goat_image_2 = ""

# Weather descriptors
clear_weather  = ["clear/sunny","sunny","clear"]
cloudy_weather = ["haze","partly cloudy","cloudy","overcast","mist","fog","freezing fog"]
rainy_weather = ["rain","showers","thunder","storms","patchy rain possible","patchy rain nearby","patchy light drizzle","light rain","light rain shower","moderate rain","moderate rain at times","heavy rain","heavy rain at times","moderate or heavy rain shower","thundery outbreaks in nearby","patchy light rain in area with thunder","light drizzle","patchy light rain","torrential rain shower","patchy freezing drizzle nearby","freezing drizzle","heavy freezing drizzle","light freezing rain","moderate or heavy freezing rain","moderate or heavy rain in area with thunder"]
snowy_weather = ["light snow","moderate snow","heavy snow","patchy light snow","light snow showers","patchy heavy snow","moderate or heavy snow showers","moderate or heavy snow in area with thunder","patchy snow nearby","light sleet showers","moderate or heavy sleet showers","light showers of ice pellets","blowing snow","moderate or heavy sleet","blizzard","patchy moderate snow","patchy sleet nearby","light sleet","moderate sleet","heavy sleet","ice pellets","moderate or heavy showers of ice pellets"]


#-------------------------------------------------------------------------------
#!--- FUNCTIONS

#!--- Switch canvases around
def flip_canvas(target,destroy):
    if destroy =="n":
        Misc.lift(target)
    else:
        Misc.lift(target)
        goat_img.unload()
        weather_canvas.delete("location")
        weather_canvas.delete("location2")

#!--- Quick weather for title screen
def quick_weather_report():
    quick_url = f'http://v2.wttr.in/'

    #!--- Grab info from wttr ---#
    '''
    Format guide: (?format="%")
    %C = [0]current weather text description               %Z = [5]timezone of loc
    %h = [1]humidity                                       %S = [6]sunrise time
    %t = [2]temperature                                    %z = [7]sun zenith time
    %l = [3]location                                       %d = [8]Dusk time
    %T = [4]current time in that timezone
    '''
    quick_weather_get = requests.get(quick_url + '?format="%C*%h*%t*%l"') # REMOVED - headers={"user-agent": "curl"}
    quick_weather_format = quick_weather_get.text.strip('"').split("*")

    # Make a dict
    quick_weather = {
        "weather":quick_weather_format[0],
        "humidity":quick_weather_format[1],
        "temperature":quick_weather_format[2],
        "location":quick_weather_format[3],
    }
    return quick_weather

#!--- Detailed weather report
def detailed_weather_report(locale):
    url = f'http://v2.wttr.in/{locale}'

    #!--- Grab info from wttr ---#
    '''
    Format guide: (?format="%")
    %C = [0]current weather text description               %Z = [5]timezone of loc
    %h = [1]humidity                                       %S = [6]sunrise time
    %t = [2]temperature                                    %z = [7]sun zenith time
    %l = [3]location                                       %d = [8]Dusk time
    %T = [4]current time in that timezone
    '''
    weather_get = requests.get(url + '?format="%C*%h*%t*%l*%T*%Z*%S*%z*%d"') # REMOVED - headers={"user-agent": "curl"}
    weather_format = weather_get.text.strip('"').split("*")

    # Remove offset from time
    if "+" in weather_format[4]:
        time,plus,offset = weather_format[4].partition("+")
    elif "-" in weather_format[4]:
        time,plus,offset = weather_format[4].partition("-")

    # Make a dict
    global current_weather
    current_weather = {
        "weather":weather_format[0],
        "humidity":weather_format[1],
        "temperature":weather_format[2],
        "location":weather_format[3],
        "time":time,
        "timezone":weather_format[5],
        "sunrise":weather_format[6],
        "zenith":weather_format[7],
        "dusk":weather_format[8]
    }
    print(current_weather)
    return current_weather


#!--- Return a time value as an int with no formatting
def time_partitions(input_string,part):
    hour,sep,tail = input_string.partition(part)
    minute,sep,tail = tail.partition(part)
    time_joined = hour + minute
    time_joined = int(time_joined)
    return time_joined

#!--- Check current time and weather and assign correct sprites and correct positioning
def time_check(weather):
    # Sky sprite
    #   Partition the time arg so we just look at an int of the hour and relevant time comparisons
    int_time = time_partitions(weather["time"],":")
    int_sunrise = time_partitions(weather["sunrise"],":")
    int_zenith = time_partitions(weather["zenith"],":")
    int_dusk = time_partitions(weather["dusk"],":")
    int_temperature,part,tail = weather["temperature"].partition("°")
    int_temperature = int(int_temperature)
    return int_time,int_sunrise,int_zenith,int_dusk,int_temperature

def goat_x_y(passed_goat):
    if "bath" in passed_goat:
        return 46,418
    elif "guitar" in passed_goat:
        return 434,419
    elif "stars" in passed_goat:
        return 679,442
    elif "sleep" in passed_goat:
        return 528,176
    elif "umbrella" in passed_goat:
        return 271,431
    elif "sweat" in passed_goat:
        return 354,214
    elif "code" in passed_goat:
        return 328,229
    elif "worry" in passed_goat:
        return 433,402
    elif "paint" in passed_goat:
        return 492,506


#!--- Grab weather report
def get_weather():
    global weather_canv_image
    global goat_image_1
    #global goat_image_2

    # Weather descriptors go here if everything breaks with them in global

    # goat animations
    #   Standard animations
    clear_day_goats = ["g_sunny_d_bath.gif","g_sunny_d_guitar.gif","g_sunny_d_stars.gif","g_sunny_d_paint.gif"]
    clear_night_goats = ["g_clear_n_bath.gif","g_clear_n_code.gif","g_clear_n_guitar.gif","g_clear_n_sleep.gif","g_clear_n_stars.gif","g_clear_n_worry.gif",]
    cloudy_day_goats = ["g_sunny_d_bath.gif","g_sunny_d_guitar.gif","g_sunny_d_stars.gif","g_sunny_d_paint.gif"]
    cloudy_night_goats = ["g_cloudy_n_bath.gif","g_cloudy_n_guitar.gif","g_cloudy_n_sleep.gif","g_cloudy_n_worry.gif"]
    rainy_day_goats = ["g_rain_d_bath.gif","g_rain_d_guitar.gif","g_rain_d_umbrella.gif","g_rain_d_code.gif"]
    rainy_night_goats = ["g_rain_n_bath.gif","g_rain_n_guitar.gif","g_rain_n_sleep.gif","g_rain_n_umbrella.gif","g_rain_n_code.gif","g_rain_n_worry.gif"]
    snow_day_goats = ["g_snow_d_bath.gif","g_snow_d_code.gif","g_snow_d_worry.gif","g_snow_d_guitar.gif","g_snow_d_umbrella.gif"]
    snow_night_goats = ["g_clear_n_bath.gif","g_clear_n_guitar.gif","g_clear_n_sleep.gif"]
    #   Sweaty animations
    clear_day_goats_sweaty = ["g_sunny_d_sweat.gif","g_sunny_d_guitar.gif","g_sunny_d_stars.gif","g_sunny_d_paint.gif"]
    clear_night_goats_sweaty = ["g_clear_n_guitar.gif","g_clear_n_sweat.gif","g_clear_n_stars.gif"]
    cloudy_day_goats_sweaty = ["g_sunny_d_bath.gif","g_sunny_d_guitar.gif","g_sunny_d_sweat.gif","g_sunny_d_paint.gif"]
    cloudy_night_goats_sweaty = ["g_cloudy_n_sweat.gif","g_cloudy_n_guitar.gif","g_cloudy_n_sleep.gif"]
    rainy_day_goats_sweaty = ["g_rain_d_sweat.gif","g_rain_d_guitar.gif","g_rain_d_umbrella.gif"]
    rainy_night_goats_sweaty = ["g_rain_n_sweat.gif","g_rain_n_guitar.gif","g_rain_n_sleep.gif","g_rain_n_umbrella.gif"]


    locale = location_entry.get()
    if locale !="":
        detailed_weather = detailed_weather_report(locale)

        #-- Canvas setup
        time,sunrise,zenith,dusk,temperature = time_check(detailed_weather)
        #goat_img = ImageLabel(weather_canvas,bd=0)
        goat_img.unload()


        print(f"{time},{sunrise},{zenith},{dusk},{temperature}")

        # GRAPHICS PLACEMENT
        # Daytime and not sweaty
        if time >= sunrise and time <= dusk and temperature <= 25:
            if detailed_weather["weather"].lower() in clear_weather:
                #   BG
                weather_canv_image = PhotoImage(file="./ui/house_sunny_day.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)


                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(clear_day_goats)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

            elif detailed_weather["weather"].lower() in cloudy_weather:
                # BG
                weather_canv_image = PhotoImage(file="./ui/house_cloudy_day.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(cloudy_day_goats)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

            elif detailed_weather["weather"].lower() in rainy_weather:
                # BG
                weather_canv_image = PhotoImage(file="./ui/house_rain_day.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)                

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(rainy_day_goats)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

            elif detailed_weather["weather"].lower() in snowy_weather:
                # BG
                weather_canv_image = PhotoImage(file="./ui/house_snow_day.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(snow_day_goats)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)
        
        # It's a sweaty day!
        elif time >= sunrise and time <= dusk and temperature > 25:
            if detailed_weather["weather"].lower() in clear_weather:
                #   BG
                weather_canv_image = PhotoImage(file="./ui/house_sunny_day.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(clear_day_goats_sweaty)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

            elif detailed_weather["weather"].lower() in cloudy_weather:
                #   BG
                weather_canv_image = PhotoImage(file="./ui/house_cloudy_day.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(cloudy_day_goats_sweaty)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

            elif detailed_weather["weather"].lower() in rainy_weather:
                #   BG
                weather_canv_image = PhotoImage(file="./ui/house_rain_day.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(rainy_day_goats_sweaty)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

            elif detailed_weather["weather"].lower() in snowy_weather:
                #   BG
                weather_canv_image = PhotoImage(file="./ui/house_snow_day.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(snow_day_goats)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

        # It's a sweaty night (yuck)(the worst)
        elif temperature > 25:
            if detailed_weather["weather"].lower() in clear_weather:
                # BG
                weather_canv_image = PhotoImage(file="./ui/house_clear_night.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(clear_night_goats_sweaty)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

            elif detailed_weather["weather"].lower() in cloudy_weather:
                # BG
                weather_canv_image = PhotoImage(file="./ui/house_cloudy_night.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(cloudy_night_goats_sweaty)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

            elif detailed_weather["weather"].lower() in rainy_weather:
                # BG
                weather_canv_image = PhotoImage(file="./ui/house_rain_night.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(rainy_night_goats_sweaty)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

            elif detailed_weather["weather"].lower() in snowy_weather:
                # BG
                weather_canv_image = PhotoImage(file="./ui/house_snow_night.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(snow_night_goats)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

        # Standard night
        else:
            if detailed_weather["weather"].lower() in clear_weather:
                # BG
                weather_canv_image = PhotoImage(file="./ui/house_clear_night.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(clear_night_goats)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

            elif detailed_weather["weather"].lower() in cloudy_weather:
                # BG
                weather_canv_image = PhotoImage(file="./ui/house_cloudy_night.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(cloudy_night_goats)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

            elif detailed_weather["weather"].lower() in rainy_weather:
                # BG
                weather_canv_image = PhotoImage(file="./ui/house_rain_night.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(rainy_night_goats)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)

            elif detailed_weather["weather"].lower() in snowy_weather:
                # BG
                weather_canv_image = PhotoImage(file="./ui/house_snow_night.png")
                weather_canvas.place(x=0,y=0)
                weather_canvas.create_image(0,0,image=weather_canv_image,anchor=NW)

                # Goat
                goat_image_1 = "./ui/goats/" + random.choice(snow_night_goats)
                # Get the x and y placement
                goat_x,goat_y = goat_x_y(goat_image_1)
                goat_img.place(x = goat_x,y = goat_y)
                goat_img.load(goat_image_1)



        #-- UI
        stats_x = 761
        weather_canvas.create_image(713,12,image=house_stat_ui,anchor=NW)
        weather_canvas.create_text(400,25,font=("Verdana",18,"bold"),fill="Black",text=detailed_weather["location"] + ", " + detailed_weather["timezone"],tag="location")
        weather_canvas.create_text(400,22,font=("Verdana",18,"bold"),fill="White",text=detailed_weather["location"] + ", " + detailed_weather["timezone"],tag="location2")

        weather_canvas.create_text(stats_x,52,font=("Verdana",14,"bold"),fill="Black",text=detailed_weather["temperature"])
        weather_canvas.create_text(stats_x,49,font=("Verdana",14,"bold"),fill="White",text=detailed_weather["temperature"])

        weather_canvas.create_text(stats_x,116,font=("Verdana",14,"bold"),fill="Black",text=detailed_weather["humidity"])
        weather_canvas.create_text(stats_x,113,font=("Verdana",14,"bold"),fill="White",text=detailed_weather["humidity"])

        weather_canvas.create_text(stats_x+20,179,font=("Verdana",14,"bold"),fill="Black",text=detailed_weather["sunrise"])
        weather_canvas.create_text(stats_x+20,176,font=("Verdana",14,"bold"),fill="White",text=detailed_weather["sunrise"])

        weather_canvas.create_text(stats_x+20,245,font=("Verdana",14,"bold"),fill="Black",text=detailed_weather["dusk"])
        weather_canvas.create_text(stats_x+20,242,font=("Verdana",14,"bold"),fill="White",text=detailed_weather["dusk"])

        # Return to quick view - Buggy cos of animation handling
        goto_quick_view = Button(weather_canvas,font=("Verdana",14,"bold"),width=10,background="#39a3bf",fg="white",text="Back",command=lambda: flip_canvas(title_canvas,"y"))
        goto_quick_view.place(x=12,y=615)

        flip_canvas(weather_canvas,"n")
    else:
        messagebox.showwarning("warning", "Please enter a location!")



#-------------------------------------------------------------------------------
#!--- CLASSES

#!--- Allows animated gifs
class ImageLabel(tkinter.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)



#-------------------------------------------------------------------------------
#!--- TKINTER LOOP FROM HERE ---#
#-------------------------------------------------------------------------------
# Set up our main window
win = Tk()

# Window width, height, x-pos, and y-pos
win.geometry('860x666+500+200')

# Prog title, window BG colour, and disallow user resizing of the window
win.title('Bahhrometer')
win.config(bg="#33BBFF")
win.resizable(width = False, height = False)

# Get the user's weather by IP
weather_by_ip = quick_weather_report()
print(weather_by_ip)

'''
THE FIRST CANVAS OPERATES AS A TITLE SCREEN. THIS IS FLIPPED IN Z-DEPTH TO REVEAL THE UNDERLYING CANVAS ONCE SUBMIT IS PRESSED
'''
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!--- FIRST CANVAS: Inputting locale ---#
title_canvas = Canvas(win,width=860,height=666,bd=-2)
title_canv_image = PhotoImage(file="./ui/title_ui.png")
title_canvas.place(x=0,y=0)
title_canvas.create_image(0,0,image=title_canv_image,anchor=NW)

# stats
if weather_by_ip["weather"].lower() in clear_weather:
    weather_gfx = PhotoImage(file="./ui/t_symbol_sun.png")
elif weather_by_ip["weather"].lower() in cloudy_weather:
    weather_gfx = PhotoImage(file="./ui/t_symbol_cloud.png")
elif weather_by_ip["weather"].lower() in rainy_weather:
    weather_gfx = PhotoImage(file="./ui/t_symbol_rain.png")
elif weather_by_ip["weather"].lower() in snowy_weather:
    weather_gfx = PhotoImage(file="./ui/t_symbol_snow.png")

title_canvas.create_image(115,454,image=weather_gfx,anchor=NW)
title_canvas.create_text(447,498,justify='center',font=("Verdana",20,"bold"),fill="White",text=weather_by_ip["humidity"])
title_canvas.create_text(683,498,justify='center',font=("Verdana",20,"bold"),fill="White",text=weather_by_ip["temperature"])


quick_location = title_canvas.create_text(430,409,justify='center',font=("Verdana",30,"bold"),fill="#2b271d",text=weather_by_ip["location"].upper())
quick_location = title_canvas.create_text(430,406,justify='center',font=("Verdana",30,"bold"),fill="White",text=weather_by_ip["location"].upper())

location_parse,remove,tail = weather_by_ip["location"].partition(",")

# buttons for info - Weather gfx, temp, humidity

location_entry = Entry(title_canvas,font=("Arial",14),width=40,bg="white")
location_entry.insert(0,location_parse)
location_entry.place(x=208,y=599)

location_submit = Button(title_canvas,font=("Verdana",14,"bold"),width=10,background="#39a3bf",fg="white",text="Submit",command=get_weather)
location_submit.place(x=663,y=592)


'''
THE SECOND CANVAS HOUSES THE HOUSE AND ALL THE SPRITES AND ANIMATIONS.
'''
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!--- SECOND CANVAS: Weather report ---#
weather_canvas = Canvas(win,width=860,height=666,bd=-2)
goat_img = ImageLabel(weather_canvas,bd=0)
house_stat_ui = PhotoImage(file="./ui/house_ui_stats.png")
weather_canvas.create_image(713,12,image=house_stat_ui,anchor=NW)


Misc.lift(title_canvas)


#----------------------------------------------------------------------------------
# Equivalent to a main loop, runs infinitely to keep the window up on screen
win.mainloop()