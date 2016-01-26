# Collection constants
COLLECTION = "collection"
COLLECTION_OS = "operatingsystems"
COLLECTION_HOST = "hosts"
COLLECTION_ARCH = "architectures"
COLLECTION_MEDIA = "media"
COLLECTION_DOMAIN = "domains"
COLLECTION_PTABLE = "ptables"
COLLECTION_LOCATION = "locations"
COLLECTION_HOSTGROUP = "hostgroups"
COLLECTION_ENVIRONMENT = "environments"
COLLECTION_ORGANIZATION = "organizations"

# Element id constants
ELEMENT_ID = "element_id"
OS_ID = "operatingsystem_id"
HOST_ID = "host_id"
ARCH_ID = "architecture_id"
MEDIA_ID = "medium_id"
DOMAIN_ID = "domain_id"
PTABLE_ID = "ptable_id"
LOCATION_ID = "location_id"
HOSTGROUP_ID = "hostgroup_id"
ENVIRONMENT_ID = "environment_id"
ORGANIZATION_ID = "organization_id"

# Search attribute constants
SEARCH_ATTR = "search_attr"
SEARCH_ATTR_NAME = "name"
SEARCH_ATTR_TITLE = "title"
SEARCH_ATTR_DESCRIPTION = "description"

COLLECTION_D = {
    COLLECTION_OS: {
        ELEMENT_ID: OS_ID,
        SEARCH_ATTR: SEARCH_ATTR_DESCRIPTION,
    },
    COLLECTION_HOST: {
        ELEMENT_ID: HOST_ID,
        SEARCH_ATTR: SEARCH_ATTR_NAME,
    },
    COLLECTION_ARCH: {
        ELEMENT_ID: ARCH_ID,
        SEARCH_ATTR: SEARCH_ATTR_NAME,
    },
    COLLECTION_MEDIA: {
        ELEMENT_ID: MEDIA_ID,
        SEARCH_ATTR: SEARCH_ATTR_NAME,
    },
    COLLECTION_DOMAIN: {
        ELEMENT_ID: DOMAIN_ID,
        SEARCH_ATTR: SEARCH_ATTR_NAME
    },
    COLLECTION_PTABLE: {
        ELEMENT_ID: PTABLE_ID,
        SEARCH_ATTR: SEARCH_ATTR_NAME,
    },
    COLLECTION_LOCATION: {
        ELEMENT_ID: LOCATION_ID,
        SEARCH_ATTR: SEARCH_ATTR_TITLE
    },
    COLLECTION_HOSTGROUP: {
        ELEMENT_ID: HOSTGROUP_ID,
        SEARCH_ATTR: SEARCH_ATTR_TITLE,
    },
    COLLECTION_ORGANIZATION: {
        ELEMENT_ID: ORGANIZATION_ID,
        SEARCH_ATTR: SEARCH_ATTR_TITLE
    },
    COLLECTION_ENVIRONMENT: {
        ELEMENT_ID: ENVIRONMENT_ID,
        SEARCH_ATTR: SEARCH_ATTR_NAME,
    },
}

# Host status constants
HOST_STATUS_NO_CHANGES = "No changes"
HOST_STATUS_OUT_OF_SYNC = "Out of sync"
HOST_STATUS_PENDING_INSTALLATION = "Pending Installation"
