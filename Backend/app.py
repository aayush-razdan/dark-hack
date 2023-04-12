from flask import Flask, redirect, url_for, request
import darkweb
import text_process

app = Flask(__name__)

@app.route('/flask', methods=['GET'])
def index():
    return "Flask server"

@app.route('/flask/crawl', methods=['POST'])
def crawl():
    url = request.form['url']
    return darkweb.crawl(url)

@app.route('/flask/scrape_body', methods=['POST'])
def scrape_body():
    link = request.form['link']
    return darkweb.scrape_body(link)

@app.route('/flask/text_process', methods=['POST'])
def text():
    text = request.form['text']
    return text_process.porn_score(text)

