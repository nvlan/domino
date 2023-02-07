import os
## pending header x_application_id

class BaseConfig(object):
    PREFIX_APP_URL = '/api/domino'
    LOG_FORMAT = '%(asctime)s- %(levelname)s - %(message)s'
    LOG_FILE = '/opt/logs/domino.log'
    #Specify which AWS region to use! Format should be eg. us-east-1
    REGION = ''
    STATIC_ROOT = '/opt/code/domino/app/statics'
    #Use the CDN dict to map which CNAME record to write for each domain
    #to create
    CDN = {}
    #List to blacklist specific domains
    BLACKLIST_DOMAINS = []
    SUBDOMAINS = []

settings = globals()['BaseConfig']
