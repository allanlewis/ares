from __future__ import print_function

from pprint import pprint

import requests

BASE_URL = 'https://api.ssllabs.com/api/v2'


def get_url(endpoint):
    return '{}/{}'.format(BASE_URL, endpoint)


def get_response(endpoint, **params):
    url = get_url(endpoint)
    response = requests.get(url, params=params)
    return response.json()


def pprint_response(endpoint, **params):
    response = get_response(endpoint, **params)
    pprint(response)


def main():
#    pprint_response('info')
    host_info = get_response('analyze', host='www1.firstdirect.com', fromCache='on', all='done')
    pprint(host_info)
    ip_addrs = [endpoint['ipAddress'] for endpoint in host_info['endpoints']]
    for addr in ip_addrs:
        print('***', addr)
        pprint_response('getEndpointData', host='www1.firstdirect.com', fromCache='on', s=addr)


class SSLTest(object):
    def __init__(self, host, use_cache=True):
        params = dict(fromCache='on', all='done') if use_cache else dict(startNew='on', all='done')
        self._host_info = get_response('analyze', host=host, **params)
        ip_addr = self._host_info['endpoints'][0]['ipAddress']
        self._endpoint_info = get_response('getEndpointData', host=host, fromCache='on' if use_cache else '', s=ip_addr)
        self.grade = self._endpoint_info['grade']
        self.drown_vulnerable = self._endpoint_info['details']['drownVulnerable']
        self.poodle_vulnerable = self._endpoint_info['details']['poodle']

if __name__ == '__main__':
#    main()
    pprint(vars(SSLTest('www1.firstdirect.com')))
