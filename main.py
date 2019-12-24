from string import Template
import requests
from tkinter import *
from tkinter import ttk
import io
from PIL import Image, ImageTk

# API interface
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


# Tkinter GUI setup
class App():
    rating_template = Template('$rating (max: $max_rating)')
    rank_template = Template('$rank (max: $max_rank)')

    def __init__(self):
        self.scrapper = Scrapper()
        self.createUI()

    def createUI(self):
        self.root = Tk()
        self.root.title('Codeforces')

        # search
        self.form = ttk.Frame(self.root, padding=(16,16), borderwidth=8, relief='raised')
        self.form.pack(fill=X, anchor=N, expand=True)

        self.username_label = ttk.Label(self.form, text='Search username:')
        self.username_label.pack(side=LEFT, padx=8, pady=8)

        self.username = StringVar()
        self.username_entry = ttk.Entry(self.form, width=20, textvariable=self.username)
        self.username_entry.pack(side=LEFT, padx=8, pady=8)

        self.search_button = ttk.Button(self.form, text='Go', command=self.search)
        self.search_button.pack(side=RIGHT)

        # info
        self.info = ttk.Frame(self.root, padding=(16,16), borderwidth=8, relief='sunken')
        self.info.pack(fill=BOTH, expand=True)

        self.error_display = StringVar()
        self.error_label = ttk.Label(self.info, textvariable=self.error_display)
        self.error_label.grid(column=0, row=0, columnspan=2)

        self.avatar = None
        self.avatar_label = ttk.Label(self.info, image=self.avatar)
        self.avatar_label.grid(column=0, row=1, rowspan=3, padx=8)

        self.handle_display = StringVar()
        self.handle_label = ttk.Label(self.info, textvariable=self.handle_display)
        self.handle_label.grid(column=1, row=1, sticky='w')

        self.rating_display = StringVar()
        self.rating_label = ttk.Label(self.info, textvariable=self.rating_display)
        self.rating_label.grid(column=1, row=2, sticky='w')

        self.rank_display = StringVar()
        self.rank_label = ttk.Label(self.info, textvariable=self.rank_display)
        self.rank_label.grid(column=1, row=3, sticky='w')

    def search(self):
        try:
            data = self.scrapper.fetch_data(self.username.get())
            print(data)
            self.error = None;
            image = self.scrapper.fetch_image('https:' + data['avatar'])
            self.avatar = ImageTk.PhotoImage(Image.open(image))
            self.handle = data['handle']
            self.rating = data['rating']
            self.rank = data['rank']
            self.max_rating = data['maxRating']
            self.max_rank = data['maxRank']    
        except ScrapperException as e:
            print(e)
            self.error = e
        self.updateUI()

    def updateUI(self):
        if self.error is None:
            self.error_label.grid_remove()
            self.avatar_label.configure(image=self.avatar)
            self.handle_display.set(self.handle)
            self.rating_display.set(App.rating_template.substitute(rating=self.rating, max_rating=self.max_rating))
            self.rank_display.set(App.rank_template.substitute(rank=self.rank, max_rank=self.max_rank))
        else:
            self.error_display.set(self.error)
            self.error_label.grid()
            self.avatar_label.configure(image='')
            self.handle_display.set('')
            self.rating_display.set('')
            self.rank_display.set('')

    def run(self):
        self.root.mainloop()


def main():
    App().run()


if __name__ == '__main__':
    main()
