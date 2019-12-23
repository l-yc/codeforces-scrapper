from string import Template
import requests
from tkinter import *
from tkinter import ttk
import io
from PIL import Image, ImageTk

# Handle,Current Rating, Rank, Max Rating , Max Rank if the handle exists and print error if it dosen't. 
class ScrapperException(Exception):
    '''raise this when there's a scrapper error'''

class Scrapper():
    api = Template('https://codeforces.com/api/$methodName')

    def __init__(self):
        pass

    def fetch_data(self, username):
        response = requests.get(Scrapper.api.substitute(methodName='user.info'), params={ 'handles': username })
        print(response)
        data = response.json()
        if response and data['status'] == 'OK':
            return data['result'][0]    # only take the first user
        else:
            raise ScrapperException('Error: User with the specified username does not exist.')

    def fetch_image(self, url):
        response = requests.get(url, stream=True)
        raw_data = response.raw.read()
        image = io.BytesIO(raw_data)
        return image


# Tkinter GUI Setup
class App():
    rating_template = Template('$rating (max: $max_rating)')
    rank_template = Template('$rank (max: $max_rank)')

    def __init__(self):
        self.scrapper = Scrapper()
        self.createUI()

    def createUI(self):
        root = Tk()
        root.title('Codeforces')
        mainframe = ttk.Frame(root, padding=(3,3,24,24), borderwidth=24, relief='solid')
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.rowconfigure(0, weight=1)
        self.root = root

        # search
        self.username_label = ttk.Label(mainframe, text='Enter username:')
        self.username_label.grid(column=0, row=0, sticky='w')

        self.username = StringVar()
        self.username_entry = ttk.Entry(mainframe, width=20, textvariable=self.username)
        self.username_entry.grid(column=1, row=0, sticky='w')

        self.username_button = ttk.Button(mainframe, text='Search!', command=self.search)
        self.username_button.grid(column=2, row=0, sticky='w')

        # info
        self.title_image = None
        self.title_image_label = ttk.Label(mainframe, image=self.title_image)
        self.title_image_label.grid(column=0, row=1, rowspan=3)

        self.handle_display = StringVar()
        self.handle_label = ttk.Label(mainframe, textvariable=self.handle_display)
        self.handle_label.grid(column=1, row=1, sticky='w')

        self.rating_display = StringVar()
        self.rating_label = ttk.Label(mainframe, textvariable=self.rating_display)
        self.rating_label.grid(column=1, row=2, sticky='w')

        self.rank_display = StringVar()
        self.rank_label = ttk.Label(mainframe, textvariable=self.rank_display)
        self.rank_label.grid(column=1, row=3, sticky='w')

    def search(self):
        try:
            data = self.scrapper.fetch_data(self.username.get())
            print(data)
            image = self.scrapper.fetch_image('https:' + data['titlePhoto'])
            self.title_image = ImageTk.PhotoImage(Image.open(image))
            self.handle = data['handle']
            self.rating = data['rating']
            self.rank = data['rank']
            self.max_rating = data['maxRating']
            self.max_rank = data['maxRank']
            self.updateUI()
        except ScrapperException as e:
            pass

    def updateUI(self):
        self.title_image_label.configure(image=self.title_image)
        self.handle_display.set(self.handle)
        self.rating_display.set(App.rating_template.substitute(rating=self.rating, max_rating=self.max_rating))
        self.rank_display.set(App.rank_template.substitute(rank=self.rank, max_rank=self.max_rank))

    def run(self):
        self.root.mainloop()

App().run()
