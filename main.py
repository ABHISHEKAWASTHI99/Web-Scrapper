import requests
from bs4 import BeautifulSoup
import csv
from tkinter import  messagebox
import pprint

res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.titlelink')  # heads up! .storylink changed to .titlelink
subtext = soup.select('.subtext')
links2 = soup2.select('.titlelink')  # heads up! .storylink changed to .titlelink
subtext2 = soup2.select('.subtext')

mega_links = links + links2
mega_subtext = subtext + subtext2


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


#pprint.pprint(create_custom_hn(mega_links, mega_subtext))


def write():
    mydict = create_custom_hn(mega_links, mega_subtext)

    fields = ['title', 'link', 'votes']

    filename = "scrapedata.csv"

    # writing to csv file
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        writer.writeheader()

        writer.writerows(mydict)

        return messagebox.showinfo('Web Scrapper','News saved in the excel file')
