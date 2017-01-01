class DnsApi():
    def __init__(self):
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
    def add_zone(self, zone: str):
        raise NotImplementedError("Not implemented.")

    def list_zones(self):
        raise NotImplementedError("Not implemented.")

    def delete_zone(self, zone: str):
        raise NotImplementedError("Not implemented.")

    def add_record(self, zone, record):
        raise NotImplementedError("Not implemented.")
