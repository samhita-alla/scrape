from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)
import csv
import sys
from bs4 import BeautifulSoup
import urllib.request

@app.route('/', methods=['GET', 'POST'])
def fetch_url():
    if request.method == "POST":
        weblink = request.form['weblink']
        heading = request.form.getlist('hello1')
        link = request.form.getlist('hello2')
        # print("#####################")
        print(request.form.getlist('hello1'))
        # print("#####################")
        return redirect(url_for('show_content', weblink=weblink, heading=heading, link=link))
    return render_template('form.html')


@app.route('/show_content')
def show_content():
    weblink = request.args.get('weblink')
    heading = str(request.args.getlist('hello1'))
    link = str(request.args.getlist('hello2'))
    url = urllib.request.urlopen(weblink)
    soup = BeautifulSoup(url, "lxml")
    f = csv.writer(open("contents.csv", "w"))  
    if heading=="['Headings']":
        links = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        print('h')
        for l in links:
            f.writerow(l)
        print("Data got stored in a 'contents.csv' file.")

    if link=="['Links']":
        links = soup.find_all('a')
        print('l')
        for l in links:
            names = l.text
            fullLink = l.get('href')
            f.writerow([names,fullLink])
        print("Data got stored in a 'contents.csv' file.")    
    return render_template('show_content.html',
      weblink=weblink,
      heading=heading,
      link=link)

if __name__ == "__main__":
  app.run(debug=True)
