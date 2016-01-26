import config
import logging
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

    def update(self, element_id, **kwargs):
        """
        Update element in foreman collection

        :param element_id: element id
        :type element_id: str
        :param kwargs: element parameters to update
        :raise: ForemanException
        """
        try:
            self.collection.update(element_id, kwargs)
        except Exception as ex:
            raise ForemanException(
                "Failed to update element %s with parameters %s: %s" %
                (element_id, kwargs, ex)
            )

    def remove(self, element_id):
        """
        Remove element from foreman collection

        :param element_id: element id
        :type element_id: str
        :raise: ForemanException
        """
        try:
            self.collection.destroy(element_id)
        except Exception as ex:
            raise ForemanException(
                "Failed to remove element %s from foreman: %s" %
                (element_id, ex)
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

    def get_status(self, element_id):
        """
        Get element status

        :param element_id: element id
        :type element_id: str
        :return: element status
        :rtype: str
        """
        element_status_d = self.collection.status(element_id)
        if not element_status_d:
            self.logger.debug(
                "Failed to get element %s status" % element_id
            )
            return ""
        return element_status_d["status"]
