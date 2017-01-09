import logging

log = logging.getLogger(__name__)

from pyramid.view import view_config

from ..models import DnsApiModel
from . import SecureView


class DnsApiViews(SecureView):
    __parent__ = None

    @view_config(route_name='dnsapi.home', renderer='dnsapi/home.pt')
    def home(self):
        m = DnsApiModel()
        apilist = m.list_all()

        l = []

        for i in apilist:
            l.append({
                'id': i.id,
                'link': self.request.route_path('dnsapi.zones', id=i.id),
            })

        return {
            'out': '',
            'apilist': l,
        }

    @view_config(route_name='dnsapi.add', renderer='dnsapi/add-api.pt')
    def add(self):
        """
        Add new DNS API
        """
        import pyramid.httpexceptions as exc

        m = DnsApiModel()
        types = m.get_api_types()

        api_types = []

        for i in types:
            api_types.append({'id': i, 'name': types[i]['name']})

        if self.request.method.lower() == 'post':
            form_apitype = self.request.POST.get('apitype')
            form_address = self.request.POST.get('address')
            form_port = self.request.POST.get('port')
            form_apikey = self.request.POST.get('apikey')
            form_apipass = self.request.POST.get('apipass')

            m.add_api(apikey=form_apikey, apitype=int(form_apitype), host=form_address, port=int(form_port),
                      password=form_apipass)

            return exc.HTTPFound(location=self.request.route_path('dnsapi.home'), comment="DNS API: Add")

        return {
            'back_link': self.request.route_path('dnsapi.home'),
            'apitypes': api_types
        }

    @view_config(route_name='dnsapi.zones', renderer='dnsapi/zones.pt')
    def zones(self):
        """
        List of zones
        """
        api_id = int(self.request.matchdict['id'])

        m = DnsApiModel()
        api = m.get_api(api_id)

        from muuri.lib.dns import PowerDNSRestAPI

        a = PowerDNSRestAPI(api.apikey, api.host, api.port, api.password)

        zones = []
        for i in a.list_zones():
            zones.append({
                'name': i['name'],
                'link': self.request.route_path('dnsapi.zone', id=api_id, zone=i['name']),
            })

        return {
            'back_link': self.request.route_path('dnsapi.home'),
            'add_link': self.request.route_path('dnsapi.zone-add', id=api_id),
            'zonelist': zones,
        }

    @view_config(route_name='dnsapi.zone-add', renderer='dnsapi/add-zone.pt')
    def add_zone(self):
        """
        Add new zone to DNS server
        :return:
        """
        api_id = int(self.request.matchdict['id'])

        m = DnsApiModel()
        api = m.get_api(api_id)

        from muuri.lib.dns import PowerDNSRestAPI

        a = PowerDNSRestAPI(api.apikey, api.host, api.port, api.password)

        if self.request.method.lower() == 'post':
            form_name = self.request.POST.get('name')
            nameservers = []
            nameservers.append("ns1.{0}".format(form_name))
            nameservers.append("ns2.{0}".format(form_name))

            a.add_zone(form_name, nameservers)
            import pyramid.httpexceptions as exc
            return exc.HTTPFound(location=self.request.route_path('dnsapi.zones', id=api_id),
                                 comment="DNS API: Added zone")

        return {
            'back_link': self.request.route_path('dnsapi.zones', id=api_id),
        }

    @view_config(route_name='dnsapi.zone', renderer='dnsapi/zone.pt')
    def zone(self):
        api_id = int(self.request.matchdict['id'])

        records = [
            {"id": "SOA", "value": "SOA"},
            {"id": "A", "value": "A"},
            {"id": "CNAME", "value": "CNAME"},
            {"id": "AAAA", "value": "AAAA"},
            {"id": "NS", "value": "NS"},
            {"id": "PTR", "value": "PTR"},
            {"id": "TXT", "value": "TXT"},
            {"id": "SOA", "value": "SOA"},
        ]

        return {
            'back_link': self.request.route_path('dnsapi.zones', id=api_id),
            'recordtypes': records,
        }
