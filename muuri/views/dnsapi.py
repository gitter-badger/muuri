from pyramid.request import Request
from pyramid.view import view_config

import logging

log = logging.getLogger(__name__)

from ..models import DnsApiModel


@view_config(route_name = 'dnsapi.home', renderer='dnsapi/home.pt')
def home(request: Request):
    m = DnsApiModel()
    apilist = m.list_all()

    log.debug(apilist)

    return {'out': ''}

@view_config(route_name = 'dnsapi.add', renderer='dnsapi/add.pt')
def add(request: Request):
    import pyramid.httpexceptions as exc

    m = DnsApiModel()
    types =  m.get_api_types()

    api_types = []

    for i in types:
        api_types.append({'id': i, 'name': types[i]['name']})

    log.debug(request.method.lower())

    if request.method.lower() is 'post':
        form_apitype = request.POST.get('apitype')
        form_address = request.POST.get('address')
        form_port = request.POST.get('port')
        form_apikey = request.POST.get('apikey')
        form_apipass = request.POST.get('apipass')
        m.add_api(apikey = form_apikey, apitype = form_apitype, host = form_address, port = form_port, password = form_apipass)

        return exc.HTTPFound(location = request.route_path('dnsapi.home'), comment = "DNS API: Add")

    return {'apitypes': api_types}