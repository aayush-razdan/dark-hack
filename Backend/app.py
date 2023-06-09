from flask import Flask, redirect, url_for, request
import darkweb
import text_process

app = Flask(__name__)

@app.route('/flask', methods=['GET'])
def index():
    return "Hi you have reached Nirman API"

@app.route('/flask/crawl', methods=['POST'])
def crawl():
    # url = request.json['url']
    url = request.args.get('url')
    return darkweb.crawl(url)

@app.route('/flask/scrape_body', methods=['POST'])
def scrape_body():
    # link = request.json['url']
    link = request.args.get('url')
    return darkweb.scrape_body(link)

@app.route('/flask/porns', methods=['POST'])
def text1():
    text1 = request.form['text']
    return text_process.porn_score(text1)

@app.route('/flask/drugs', methods=['POST'])
def text2():
    text2 = request.form['text']
    return text_process.drug_score(text2)

@app.route('/flask/intelligence', methods=['POST'])
def intelligence():
    text3 = request.form['text']
    return text_process.intelligence(text3)


