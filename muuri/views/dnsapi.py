import logging

log = logging.getLogger(__name__)

from pyramid.request import Request
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.security import Allow
from pyramid.security import ALL_PERMISSIONS

from ..models import DnsApiModel
from . import SecureView


@view_defaults(permission = 'logged-in')
class DnsApiViews(SecureView):
    __parent__ = None


    @view_config(route_name = 'dnsapi.home', renderer = 'dnsapi/home.pt')
    def home(self):
        m = DnsApiModel()
        apilist = m.list_all()

        log.debug(apilist)

        return {'out': ''}

    @view_config(route_name = 'dnsapi.add', renderer = 'dnsapi/add.pt')
    def add(self):
        import pyramid.httpexceptions as exc

        m = DnsApiModel()
        types = m.get_api_types()

        api_types = []

        for i in types:
            api_types.append({'id': i, 'name': types[i]['name']})

        if self.request.method.lower() is 'post':
            form_apitype = self.request.POST.get('apitype')
            form_address = self.request.POST.get('address')
            form_port = self.request.POST.get('port')
            form_apikey = self.request.POST.get('apikey')
            form_apipass = self.request.POST.get('apipass')
            m.add_api(apikey = form_apikey, apitype = form_apitype, host = form_address, port = form_port,
                      password = form_apipass)

            return exc.HTTPFound(location = self.request.route_path('dnsapi.home'), comment = "DNS API: Add")

        return {'apitypes': api_types}
