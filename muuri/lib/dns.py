class DnsApi():
    def __init__(self, apikey: str, host: str, port: int, password: str):
        raise NotImplementedError("Not implemented.")

    def add_zone(self, zone: str):
        raise NotImplementedError("Not implemented.")

    def list_zones(self):
        raise NotImplementedError("Not implemented.")

    def delete_zone(self, zone: str):
        raise NotImplementedError("Not implemented.")

    def add_record(self, zone: str, record):
        raise NotImplementedError("Not implemented.")


class PowerDNSRestAPI(DnsApi):
    _c = None

    def __init__(self, apikey: str, host: str, port: int, password: str):
        from pypdnsrest.client import PowerDnsRestApiClient
        self._c = PowerDnsRestApiClient(apikey, "http", host, port)


    def add_zone(self, zone: str, nameservers:list):
        return self._c.add_zone(zone, nameservers)

    def list_zones(self):
        zones = self._c.get_zones()
        return zones

    def delete_zone(self, zone: str):
        raise NotImplementedError("Not implemented.")

    def add_record(self, zone, record):
        raise NotImplementedError("Not implemented.")
