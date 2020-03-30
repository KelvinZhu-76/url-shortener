from flask import Flask, render_template, request
import requests
import json
import re

tiny_api_url = 'https://agn54nepyg.execute-api.us-east-2.amazonaws.com/beta/create'
app_title = "Kelvin's Url Shortener"

headers = {'Content-Type': 'application/json', 'X-Api-Key': 'Kelvin0123456'}

app = Flask(__name__)
application = app


def validate_url(url):
    # unicode letters range
    ul = '\u00a1-\uffff'

    # IP patterns
    ipv4_re = r'(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}'
    ipv6_re = r'\[[0-9a-f:\.]+\]'

    # Host patterns
    hostname_re = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]{0,61}[a-z' + ul + r'0-9])?'
    domain_re = r'(?:\.(?!-)[a-z' + ul + r'0-9-]{1,63}(?<!-))*'
    tld_re = (
            r'\.'  # dot 
            r'(?!-)'  # can't start with a dash 
            r'(?:[a-z' + ul + '-]{2,63}'  # domain label 
                              r'|xn--[a-z0-9]{1,59})'  # or punycode label 
                              r'(?<!-)'  # can't end with a dash 
                              r'\.?'  # may have a trailing dot
    )
    host_re = '(' + hostname_re + domain_re + tld_re + '|localhost)'

    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http(s):// or ftp(s)://
        r'(?:\S+(?::\S*)?@)?'  # user:pass authentication 
        r'(?:' + ipv4_re + '|' + ipv6_re + '|' + host_re + ')'  # localhost or ip
                                                           r'(?::\d{2,5})?'  # optional port
                                                           r'(?:[/?#][^\s]*)?'  # resource path
                                                           r'\Z', re.IGNORECASE)

    return regex.search(url) is not None


@app.route('/')
def index():
    return render_template('index.html', app_title=app_title)


@app.route('/shortened', methods=['GET', 'POST'])
def search_request():
    user_url = request.form["input"].strip()
    if not user_url:
        return render_template('error.html', app_title=app_title, res='Your URL link can not be empty!')

    if not validate_url(user_url):
        return render_template('error.html', app_title=app_title, res='Your link is not a valid http URL!')

    response = requests.post(
        tiny_api_url,
        headers=headers,
        data=json.dumps({
            "long_url": user_url
        }
        )
    )

    if response.status_code == 200:
        return render_template('result.html', app_title=app_title, res=response.content.decode("utf-8"))
    else:
        return render_template('error.html', app_title=app_title, res=response.content.decode("utf-8"))


if __name__ == '__main__':
    app.run(passthrough_errors=False)
