import crypt
import config
import logging
from rrmngmnt import Host, RootUser
from foreman.client import Foreman


class ForemanException(Exception):
    pass


class ForemanCollection(object):
    """
    Foreman collection class
    """
    def __init__(
        self, foreman_url, foreman_user, foreman_password,
        api_version=2, collection_name=None, search_attr=None
    ):
        """
        Initialize Foreman collection class

        :param foreman_url: foreman url
        :type foreman_url: str
        :param foreman_user: foreman user
        :type foreman_user: str
        :param foreman_password: foreman password
        :type foreman_password: str
        :param api_version: foreman api version
        :type api_version: int
        :param collection_name: foreman collection name
        :type collection_name: str
        :param search_attr: search element under collection by given attribute
        :type search_attr: str
        """
        super(ForemanCollection, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.foreman_api = Foreman(
            url=foreman_url,
            auth=(foreman_user, foreman_password),
            api_version=api_version
        )
        self.collection = None
        self.search_attr = None
        self.collection_name = None
        self.set_collection(collection_name, search_attr=search_attr)

    def set_collection(self, collection_name, search_attr=None):
        """
        Set foreman collection

        :param collection_name: foreman collection name
        :type collection_name: str
        :param search_attr: search element under collection by given attribute
        :type search_attr: str
        """
        self.collection_name = collection_name
        self.collection = getattr(self.foreman_api, self.collection_name, None)
        if self.collection and not search_attr:
            self.search_attr = config.COLLECTION_D[
                self.collection_name
            ][config.SEARCH_ATTR]

    def get_element_id(self, element_name):
        """
        Get element id from foreman collection

        :param element_name: element name
        :type element_name: str
        :return: element id
        :rtype: str
        """
        self.logger.info(
            "Looking for %s under foreman collection %s",
            element_name, self.collection_name
        )
        response = self.collection.index(
            search="%s = \"%s\"" % (self.search_attr, element_name)
        )
        try:
            return response["results"][0]["id"]
        except (IndexError, KeyError):
            self.logger.info(
                "Element '%s' is not declared under foreman collection %s",
                element_name, self.collection_name
            )
            return ""

    def add(self, **kwargs):
        """
        Add new element to foreman collection
        Example:
            host_collection = ForemanCollection(
                COLLECTION_HOST, ...
            )
            add_dictionary = {
                "name": host_fqdn
                "ip": host_ip,
                "mac": host_mac,
                OS_ID: foreman operating system id,
                ....
            }
            host_collection.add(**add_dictionary)

        :param kwargs: element parameters
        :raise: ForemanException

        """
        try:
            self.collection.create(kwargs)
        except Exception as ex:
            raise ForemanException(
                "Failed to add element with parameters %s: %s" % (kwargs, ex)
            )

    def update(self, element_name, **kwargs):
        """
        Update element in foreman collection

        :param element_name: element name
        :type element_name: str
        :param kwargs: element parameters to update
        :raise: ForemanException
        """
        element_id = self.get_element_id(element_name=element_name)
        try:
            self.collection.update(element_id, kwargs)
        except Exception as ex:
            raise ForemanException(
                "Failed to update element %s with parameters %s: %s" %
                (element_name, kwargs, ex)
            )

    def remove(self, element_name):
        """
        Remove element from foreman collection

        :param element_name: element name
        :type element_name: str
        :raise: ForemanException
        """
        element_id = self.get_element_id(element_name=element_name)
        try:
            self.collection.destroy(element_id)
        except Exception as ex:
            raise ForemanException(
                "Failed to remove element %s from foreman: %s" %
                (element_name, ex)
            )

    def is_exist(self, element_name):
        """
        Check if element exist under foreman collection

        :param element_name: element name
        :type element_name: str
        :return: True, if element exist, otherwise False
        :rtype: bool
        """
        return bool(self.get_element_id(element_name=element_name))

    def get_status(self, element_name):
        """
        Get element status

        :param element_name: element name
        :type element_name: str
        :return: element status
        :rtype: str
        """
        element_id = self.get_element_id(element_name=element_name)
        element_status_d = self.collection.status(element_id)
        if not element_status_d:
            self.logger.debug(
                "Failed to get element %s status" % element_name
            )
            return ""
        return element_status_d["status"]


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
            api_version=api_version
        )
        self.host = Host(ip=host_ip)
        self.host.users.append(RootUser(password=host_root_password))
        self.host_id = self.get_element_id(self.host.fqdn)

    def add(self, **kwargs):
        """
        Add host to foreman

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
