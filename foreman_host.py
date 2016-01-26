import crypt
import config
from rrmngmnt import Host, RootUser
from foreman_collection import ForemanCollection


class ForemanHost(ForemanCollection):
    """
    Foreman host class
    """
    def __init__(
        self, host_ip, host_root_password,
        foreman_url, foreman_user, foreman_password, api_version=2
    ):
        """
        Initialize foreman host class

        :param host_ip: host ip
        :type host_ip: str
        :param host_root_password: host root password
        :type host_root_password: str
        :param foreman_url: foreman url
        :type foreman_url: str
        :param foreman_user: foreman user
        :type foreman_user: str
        :param foreman_password: foreman password
        :type foreman_password: str
        :param api_version: foreman api version
        :type api_version: int
        """
        super(ForemanHost, self).__init__(
            foreman_url=foreman_url,
            foreman_user=foreman_user,
            foreman_password=foreman_password,
            api_version=api_version,
            collection_name=config.COLLECTION_HOST
        )
        self.host = Host(ip=host_ip)
        self.host.users.append(RootUser(password=host_root_password))
        self.host_id = self.get_element_id(self.host.fqdn)

    def add(self, **kwargs):
        """
        Add host

        :param kwargs: mac = str
                       location_id = str
                       domain_id = str
                       organization_id = str
                       medium_id = str
                       architecture_id = str
                       operatingsystem_id = str
                       ptable_id = str
                       hostgroup_id = str
                       build = bool
                       managed = bool
        """
        mac_address = kwargs.pop(
            "mac", self.host.network.get_mac_by_ip(self.host.ip)
        )
        host_d = {
            "name": self.host.fqdn,
            "mac": mac_address,
            "ip": self.host.ip,
            "root_pass": crypt.crypt(
                self.host.root_user.password,
                crypt.mksalt(method=crypt.METHOD_MD5)
            )
        }
        host_d.update(kwargs)
        super(ForemanHost, self).add(**host_d)
        self.host_id = self.get_element_id(self.host.fqdn)

    def update(self, **kwargs):
        """
        Update host

        :param kwargs: host parameters to update
        """
        super(ForemanHost, self).update(element_id=self.host_id, **kwargs)

    def remove(self, **kwargs):
        """
        Remove host
        """
        super(ForemanHost, self).remove(element_id=self.host_id)
        self.host_id = None

    def is_exist(self, **kwargs):
        """
        Check if host exist

        :return: True, if host exist under foreman, otherwise False
        :rtype: bool
        """
        return bool(self.host_id)

    def get_status(self, **kwargs):
        """
        Get host status

        :return: host status
        :rtype: str
        """
        super(ForemanHost, self).get_status(self.host_id)

    def build(self):
        """
        Build host
        """
        self.update(build=True)
