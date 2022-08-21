from bs4 import BeautifulSoup as bs
import requests as re
import pandas as pd


def wp_lookup(search):
    wp = 'https://wp.memphis.edu'
    response = re.get(wp, headers={
        'Host': 'wp.memphis.edu',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    })
    cookies = response.cookies
    a = bs(response.content, 'html.parser')
    params = {x.get('name'): x.get('value') for x in a.find_all('input')}

    response = re.post(
        f'{wp}/search/list',
        {'utf8': params['utf8'], 'authenticity_token': params['authenticity_token'], 'search': search},
        cookies=cookies
    )

    if response.status_code != 200:
        print('error on second request')
        return

    parsed = pd.read_html(response.content.decode('utf-8'))
    if len(parsed) == 0:
        print('parsing didn\'t give any value')
    else:
        a = parsed[0]
        if len(parsed) == 1:
            tmp = dict(zip([x.strip(':') for x in list(a.get(0).values)], list(a.get(1).values)))
            tmp['Name'] = bs(response.content, 'html.parser').find(id='userinfo').find(id='name').contents[0]
            # this just makes it a dataframe instead of dict
            # out = pd.DataFrame(out.values(), index=out.keys()).transpose()
            return tmp
        else:
            # it came up with a lot of names
            return a


if __name__ == '__main__':
    thing = wp_lookup('marshall lus')
    print(thing)
