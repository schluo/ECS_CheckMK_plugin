#!/usr/bin/env python3
# encoding: utf-8

__author__    = "Oliver Schlueter"
__copyright__ = "Copyright 2021, Dell Technologies"
__license__   = "GPL"
__version__   = "1.0.0"
__email__     = "oliver.schlueter@dell.com"
__status__    = "Production"

""""
############################################
#
#  DELL EMC ECS plugin for check_mk
#
############################################

#import modules"""
import argparse
import sys
import os
import re
import json
import requests
import urllib3
import csv
import collections
import datetime
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###########################################
#        VARIABLE
###########################################
DEBUG = False

###########################################
#    Methods
###########################################

def escape_ansi(line):
        ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', str(line))

def get_argument():
    global hostaddress, user, password, create_config
   
    try:
        # Setup argument parser
        parser = argparse.ArgumentParser()
        parser.add_argument('-H', '--hostname',
                            type=str,
                            help='hostname or IP address',
                            required=True)
        parser.add_argument('-u', '--username',
                            type=str,
                            help='username', dest='username',
                            required=True)
        parser.add_argument('-p', '--password',
                            type=str,
                            help='user password',
                            required=True)
        parser.add_argument('-c', '--config', action='store_true', help='build new metric config file',required=False, dest='create_config')
        args = parser.parse_args()

    except KeyboardInterrupt:
        # handle keyboard interrupt #
        return 0

    hostaddress = args.hostname
    user = args.username
    password = args.password
    create_config = args.create_config


###########################################
#    CLASS
###########################################

class ecs():
    # This class permit to connect of the ECS's API

    def __init__(self):
        self.user = user
        self.password = password
        #self.cmd = arg_cmd

    def send_request_billing(self):
        # send a request and get the result as dict
        global ecs_results 
        ecs_results = []
        global ecs_token
                    
        try:
            # try to get token
            url = 'https://' + hostaddress + '/login'            
            r = requests.get(url, verify=False, auth=(self.user, self.password))
           
            # read access token from returned header
            ecs_token = r.headers['X-SDS-AUTH-TOKEN']
            #print(ecs_token)
            
        except Exception as err:
            print(timestamp + ": Not able to get token: " + str(err))
            exit(1)        
        
        try:
            # try to get namespaces using token
            url = 'https://' + hostaddress + '/object/namespaces'
            r = requests.get(url, verify=False, headers={"X-SDS-AUTH-TOKEN":ecs_token, "Accept":"application/json"})

            if DEBUG:
                print(r, r.headers)
                
            ecs_namespaces = json.loads(r.content)['namespace']
          
            for namespace in ecs_namespaces:
                current_namespace = namespace["name"]
                
                # try to get buckets using namespaces
                url = 'https://' + hostaddress + '/object/bucket?namespace=' + current_namespace
                r = requests.get(url, verify=False, headers={"X-SDS-AUTH-TOKEN":ecs_token, "Accept":"application/json"})
                ecs_buckets = json.loads(r.content)['object_bucket']
           
                for bucket in ecs_buckets:
                    current_bucket = bucket["name"]
                    
                    # try to get capacity data
                    try:
                        url = 'https://' + hostaddress + '/object/billing/buckets/' + current_namespace + '/' + current_bucket + '/info'
                        r = requests.get(url, verify=False, headers={"X-SDS-AUTH-TOKEN":ecs_token, "Accept":"application/json"})
                        bucket_billing = json.loads(r.content)
                        bucket_total_objects = bucket_billing["total_objects"]   
                        bucket_total_size = float(bucket_billing["total_size"])*1024
                        
                    # if not possible set values to zero
                    except:
                        bucket_total_objects = 0
                        bucket_total_size = 0
                        
                    bucket_data =  {"name" : current_bucket, "namespace" : current_namespace, "total_objects" : bucket_total_objects, "total_size" : bucket_total_size}
                    ecs_results.append(bucket_data)  

        except Exception as err:
            print(timestamp + ": Not able to get bucket data: " + str(err))
            exit(1)   
        
    def process_results(self):
        self.send_request_billing()

        # initiate plugin output
        try:
            checkmk_output = "Bucket Data successful loaded at " + timestamp +" | "
            check_mk_metric_conf = ""
            
            for bucket in ecs_results:
                #print(bucket["namespace"] + "/" + bucket["name"], bucket["total_objects"], bucket["total_size"])
                
                metric_full_name = bucket["namespace"] + "/" + bucket["name"] + " Capacity"
                 
                #if command line option "-c" was set then create new metric config file
                if create_config:
                    metric_unit = "bytes"
                
                    # build diagram titles from metric keys
                    check_mk_metric_conf += 'metric_info["' + metric_full_name +'"] = { ' + "\n" + \
                        '    "title" : _("' + metric_full_name.title() + '"),' + "\n" + \
                        '    "unit" : "'"bytes"'",' + "\n" + \
                        '    "color" : "' + self.random_color() + '",' + "\n" + \
                    '}' + "\n"
                        
                checkmk_output += "'" +  metric_full_name +"'=" + str(bucket["total_size"]) + ";;;; "
            
            # print result to standard output
            print(checkmk_output)

            # if command line option "-c" was set
            if create_config:
                try:                                  
                    fobj = open(metric_config_file,"w")
                    fobj.write(check_mk_metric_conf)
                    fobj.close()
                except Exception as err:
                    print(timestamp + ": Not able to write metric config file: " + str(err))
                    exit(1)

        except Exception as err:
            print(timestamp + ": Error while generating result output: " + str(err))
            exit(1)

        sys.exit(0)

 

    # method to generate a random color in hex code
    def random_color(self):
        red = format(random.randrange(10, 254),'x');
        green = format(random.randrange(10, 254),'x');
        blue = format(random.randrange(10, 254),'x');
        return "#"+ red.zfill(2) + green.zfill(2) + blue.zfill(2)


def main(argv=None):
    # get and test arguments
    get_argument()

    # store timestamp
    global timestamp, metric_filter_file, metric_config_file
    timestamp = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")

    metric_config_file = os.path.dirname(__file__).replace("/lib/nagios/plugins", "/share/check_mk/web/plugins/metrics/ecs_metric_" + hostaddress.replace(".","_")+ ".py")

    # display arguments if DEBUG enabled
    if DEBUG:
        print("hostname: "+hostaddress)
        print("user: "+user)
        print("password: "+password)
    else:
        sys.tracebacklimit = 0

    myecs = ecs()

    myecs.process_results()


if __name__ == '__main__':
    main()
    sys.exit(3)
