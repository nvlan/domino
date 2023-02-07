import boto3
import flask
import time
#from boto3.session import Session
from botocore.config import Config as botoConfig
import logging
from domino.config import BaseConfig

# credentials should be: {'AWS_KEY': 'XXXX', 'AWS_SECRET': 'XXXX', 'REGION': 'us-east-1'}
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s- %(levelname)s - %(message)s')
import json

class Route53():

    def __init__(self, current_app, data=None):
        self.data = data
        config = botoConfig(retries=dict(max_attempts=30))
        region = current_app.config['REGION']
        self.r53 = boto3.client('route53', region_name=region, config=config)
        self.blacklist_domains = current_app.config['BLACKLIST_DOMAINS']
        if data is not None:
            self.id_zone = data['id_zone']
            try:
                if data['action'] == 'CREATE' or data['action'] == 'DELETE':
                    self.subdomain = data['subdomain']
                    self.zone = data['zone']
                    self.cdn = current_app.config['CDN'][data['zone']]
            except:
                pass

    #metodo que devuelve todos los domains actuales de AWS, restando los blacklisted
    def get_all_zones(self):
        success = True
        extraArgs = {}
        zones = {}
        all_zones = {}
        while True:
            try:
                response = self.r53.list_hosted_zones(**extraArgs)
            except:
                success = False
                break
            else:
                for i in range(len(response['HostedZones'])):
                    if response['HostedZones'][i]['Name'][:-1] not in self.blacklist_domains:
                        zones[response['HostedZones'][i]['Name'][:-1]] = response['HostedZones'][i]['Id'][12:]
                if response['IsTruncated']:
                    extraArgs['Marker'] = response['NextMarker']
                else:
                    break
        return zones, success

    #metodo que devuelve todos los registros en una zona. Espera recibir el pais.
    def get_records(self):
        success = True
        records = []
        extraArgs = {}
        all_records = {}
        while True:
            try:
                response = self.r53.list_resource_record_sets(HostedZoneId=self.id_zone,**extraArgs)
            except:
                success = False
                response = { 'Error' : 'The zone does not exist' }
                return response, success
            else:
                for record in response['ResourceRecordSets']:
                    if record['Type'] == 'A' or record['Type'] == 'CNAME':
                        records.append(record)
                if response['IsTruncated']:
                    extraArgs['StartRecordName'] = response['NextRecordName']
                    extraArgs['StartRecordType'] = response['NextRecordType']
                else:
                    break
        all_records.setdefault('Resource records', records)
        return all_records, success

    #metodo que crea los registros en una zona. Espera recibir el pais y el subdominio a crear
    def action_records(self):
        success = True
        status = 'PENDING'
        try:
            response = self.r53.change_resource_record_sets(
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': self.data['action'],
                            'ResourceRecordSet': {
                                'Name': self.subdomain + '.' + self.zone,
                                'ResourceRecords': [
                                    {
                                        'Value': self.cdn,
                                    },
                                ],
                                'TTL': 300,
                                'Type': 'CNAME',
                            },
                        },
                    ],
                    'Comment': 'Record created by Domino',
                },
                HostedZoneId= self.id_zone,
            )
        except:
            success = False
            if self.data['action'] == 'CREATE':
                response2 = { 'Error' : 'The subdomain is in use' }
            else:
                response2 = { 'Error' : 'the record you want to delete does not exist' }
        else:
            if self.data['action'] == 'CREATE':
                response2 = { 'Success' : 'The record ' + self.subdomain + '.' + self.zone + ' has been created' }
                try:
                    if self.data['update']:
                        response2 = { 'Success' : 'The record ' + self.subdomain + '.' + self.zone + ' has been updated' }
                except:
                    pass
            else:
                response2 = { 'Success' : 'The record ' + self.subdomain + '.' + self.zone + ' has been deleted' }
        return response2, success
