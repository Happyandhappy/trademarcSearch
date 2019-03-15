from flask import *
import os, sys, json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

path = os.path.dirname(__file__)
app = Flask(__name__)

def getVal(querydata, name):
    return querydata[name][0] if name in querydata else ''

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
    if Count > 2000:
        Count = 2000
    sess = requests.session()
    querydata = parse_qs(urlparse(url).query)
    res = sess.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    names = [
        'wv[0]','wt[0]','weOp[0]','wv[1]','wt[1]' ,'wrOp','wv[2]','wt[2]','weOp[1]',
        'wv[3]','wt[3]','iv[0]','it[0]','ieOp[0]','iv[1]','it[1]','irOp','iv[2]',
        'it[2]','ieOp[1]','iv[3]','it[3]','wp','_sw','classList','ct','status',
        'dateType','fromDate','toDate','ia','gsd', 'endo','nameField[0]','name[0]',
        'attorney','oAcn','idList','ir','publicationFromDate','publicationToDate',
        'i','c','originalSegment'
    ]
    _csrf = soup.find('meta', {'name' : '_csrf'})['content']
    data = {}
    data['_csrf'] = _csrf
    for name in names:
        data[name] = getVal(querydata, name)
    """
    data = {
        '_csrf'     : _csrf,
        'wv[0]'     : getVal(querydata,'wv[0]'),
        'wt[0]'     : getVal(querydata,'wt[0]'),
        'weOp[0]'   : getVal(querydata,'weOp[0]'),
        'wv[1]'     : getVal(querydata,'wv[1]'),
        'wt[1]'     : getVal(querydata,'wt[1]'),
        'wrOp'      : getVal(querydata,'wrOp'),
        'wv[2]'     : getVal(querydata,'wv[2]'),
        'wt[2]'     : getVal(querydata,'wt[2]'),
        'weOp[1]'   : getVal(querydata,'weOp[1]'),
        'wv[3]'     : getVal(querydata,'wv[3]'),
        'wt[3]'     : getVal(querydata,'wt[3]'),
        'iv[0]'     : getVal(querydata,'iv[0]'),
        'it[0]'     : getVal(querydata,'it[0]'),
        'ieOp[0]'   : getVal(querydata,'ieOp[0]'),
        'iv[1]'     : getVal(querydata,'iv[1]'),
        'it[1]'     : getVal(querydata,'it[1]'),
        'irOp'      : getVal(querydata,'irOp'),
        'iv[2]'     : getVal(querydata,'iv[2]'),
        'it[2]'     : getVal(querydata,'it[2]'),
        'ieOp[1]'   : getVal(querydata,'ieOp[1]'),
        'iv[3]'     : getVal(querydata,'iv[3]'),
        'it[3]'     : getVal(querydata,'it[3]'),
        'wp'        : getVal(querydata,'wp'),
        '_sw'       : getVal(querydata,'_sw'),
        'classList' : getVal(querydata,'classList'),
        'ct'        : getVal(querydata,'ct'),
        'status'    : getVal(querydata,'status'),
        'dateType'  : getVal(querydata,'dateType'),
        'fromDate'  : getVal(querydata,'fromDate'),
        'toDate'    : getVal(querydata,'toDate'),
        'ia'        : getVal(querydata,'ia'),
        'gsd'       : getVal(querydata,'gsd'),
        'endo'      : getVal(querydata,'endo'),
        'nameField[0]': getVal(querydata,'nameField[0]'),
        'name[0]'   : getVal(querydata,'name[0]'),
        'attorney'  : getVal(querydata,'attorney'),
        'oAcn'      : getVal(querydata,'oAcn'),
        'idList'    : getVal(querydata,'idList'),
        'ir'        : getVal(querydata,'ir'),
        'publicationFromDate': getVal(querydata,'publicationFromDate'),
        'publicationToDate'  : getVal(querydata,'publicationToDate'),
        'i' : getVal(querydata,'i'),
        'c' : getVal(querydata,'c'),
        'originalSegment' : getVal(querydata,'originalSegment')
    }
    """
    rest = sess.post(url='https://search.ipaustralia.gov.au/trademarks/search/doSearch', data=data)
    tradeMarkIds = getTrademarksfromHtml(rest.text)
    URL = rest.url
    pages = int(Count/100) + 1 if Count % 100 > 0 else int(Count/100)
    for page in range(1, pages):
        res = sess.get("%s&p=%s" % (URL, page))
        tradeMarkIds = tradeMarkIds + getTrademarksfromHtml(res.text)
    return tradeMarkIds


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

@app.route('/mysearch')
def mysearch():
    return render_template("mysearch.html")

if __name__ == '__main__':
    app.run(debug=True)