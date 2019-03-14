from flask import *
import os, sys, json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

path = os.path.dirname(__file__)
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/getCountofResult', methods=['POST'])
def cntofResult():
    originUrl = request.form['url']
    url = originUrl.replace('advanced','count')
    res = requests.get(url)
    data = json.loads(res.text)
    # scrape url
    Ids = scrap(originUrl, data['count'])
    return json.dumps({"data" : data, "trademarks" :  Ids})

# extract tradenark Ids from html content
def getTrademarksfromHtml(html):
    soup = BeautifulSoup(html, "html.parser")
    try:
        table_bodys = soup.find('table', id='resultsTable').find_all('tbody')
    except:
        return []
    tradeMarkIds = []
    for row in table_bodys:
        tradeMarkIds.append(row['data-mark-id'])
    return tradeMarkIds

# scrap function
def scrap(url, Count):
    sess = requests.session()
    querydata = parse_qs(urlparse(url).query)
    res = sess.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    _csrf = soup.find('meta', {'name' : '_csrf'})['content']

    data = {
        '_csrf'     : _csrf,
        'wv[0]'     : querydata['wv[0]'][0] if 'wv[0]' in querydata else '',
        'wt[0]'     : querydata['wt[0]'][0] if 'wt[0]' in querydata else '',
        'weOp[0]'   : querydata['weOp[0]'][0] if 'weOp[0]' in querydata else '',
        'wv[1]'     : querydata['wv[1]'][0] if 'wv[1]' in querydata else '',
        'wt[1]'     : querydata['wt[1]'][0] if 'wt[1]' in querydata else '',
        'wrOp'      : querydata['wrOp'][0] if 'wrOp' in querydata else '',
        'wv[2]'     : querydata['wv[2]'][0] if 'wv[2]' in querydata else '',
        'wt[2]'     : querydata['wt[2]'][0] if 'wt[2]' in querydata else '',
        'weOp[1]'   : querydata['weOp[1]'][0] if 'weOp[1]' in querydata else '',
        'wv[3]'     : querydata['wv[3]'][0] if 'wv[3]' in querydata else '',
        'wt[3]'     : querydata['wt[3]'][0] if 'wt[3]' in querydata else '',
        'iv[0]'     : querydata['iv[0]'][0] if 'iv[0]' in querydata else '',
        'it[0]'     : querydata['it[0]'][0] if 'it[0]' in querydata else '',
        'ieOp[0]'   : querydata['ieOp[0]'][0] if 'ieOp[0]' in querydata else '',
        'iv[1]'     : querydata['iv[1]'][0] if 'iv[1]' in querydata else '',
        'it[1]'     : querydata['it[1]'][0] if 'it[1]' in querydata else '',
        'irOp'      : querydata['irOp'][0] if 'irOp' in querydata else '',
        'iv[2]'     : querydata['iv[2]'][0] if 'iv[2]' in querydata else '',
        'it[2]'     : querydata['it[2]'][0] if 'it[2]' in querydata else '',
        'ieOp[1]'   : querydata['ieOp[1]'][0] if 'ieOp[1]' in querydata else '',
        'iv[3]'     : querydata['iv[3]'][0] if 'iv[3]' in querydata else '',
        'it[3]'     : querydata['it[3]'][0] if 'it[3]' in querydata else '',
        'wp'        : querydata['wp'][0] if 'wp' in querydata else '',
        '_sw'       : querydata['_sw'][0] if '_sw' in querydata else '',
        'classList' : querydata['classList'][0] if 'classList' in querydata else '',
        'ct'        : querydata['ct'][0] if 'ct' in querydata else '',
        'status'    : querydata['status'][0] if 'status' in querydata else '',
        'dateType'  : querydata['dateType'][0] if 'dateType' in querydata else '',
        'fromDate'  : querydata['fromDate'][0] if 'fromDate' in querydata else '',
        'toDate'    : querydata['toDate'][0] if 'toDate' in querydata else '',
        'ia'        : querydata['ia'][0] if 'ia' in querydata else '',
        'gsd'       : querydata['gsd'][0] if 'gsd' in querydata else '',
        'endo'      : querydata['endo'][0] if 'endo' in querydata else '',
        'nameField[0]': querydata['nameField[0]'][0] if 'nameField[0]' in querydata else '',
        'name[0]'   : querydata['name[0]'][0] if 'name[0]' in querydata else '',
        'attorney'  : querydata['attorney'][0] if 'attorney' in querydata else '',
        'oAcn'      : querydata['oAcn'][0] if 'oAcn' in querydata else '',
        'idList'    : querydata['idList'][0] if 'idList' in querydata else '',
        'ir'        : querydata['ir'][0] if 'ir' in querydata else '',
        'publicationFromDate': querydata['publicationFromDate'][0] if 'publicationFromDate' in querydata else '',
        'publicationToDate'  : querydata['publicationToDate'][0] if 'publicationToDate' in querydata else '',
        'i' : querydata['i'][0] if 'i' in querydata else '',
        'c' : querydata['c'][0] if 'c' in querydata else '',
        'originalSegment' : querydata['originalSegment'][0] if 'originalSegment' in querydata else ''
    }

    rest = sess.post(url='https://search.ipaustralia.gov.au/trademarks/search/doSearch', data=data)
    tradeMarkIds = getTrademarksfromHtml(rest.text)
    URL = rest.url
    for page in range(1, int(Count/100)+1):
        res = sess.get("%s&p=%s" % (URL, page))
        tradeMarkIds = tradeMarkIds + getTrademarksfromHtml(res.text)
    return tradeMarkIds

if __name__ == '__main__':
    app.run(debug=True)