import json
import falcon
from pprint import pprint
#from .lawscli import LawsCli
#from .testmodule import TestModule
from .LavaAws import LavaAws
from .LavaAzure import LavaAzure


class InstanceCtrl:

    def do_operation(self, op, qs):

        resp={}
        if op == 'aws':
            my_lc=LavaAws()
            myfilters=[]
            myvalues=['lava_srvr']
            if 'values' in qs:
                for value in qs['values']:
                    myvalues.append(value)
            F1={'Name':'tag:Name','Values':myvalues}
            myfilters.append(F1)
            # Commeting temporarily
            # resp=my_lc.list_instances(myfilters)
            resp["instances"] = [{'ImageId': 'ami-65383lava',
                                  'InstanceId': 'i-0aa518a7e5d43lava',
                                  'InstanceType': 't1.micro',
                                  'Tags': [{'Key':'Name', 'Value': 'amazonVM1'}],
                                  'State': {'Code': '80', 'Name':'running'}}]
            resp["error_code"]=0
        elif op == 'gcp':
            resp["instances"] = [{'ImageId': 'gcp-11223232',
                                  'InstanceId': 'gcp-0aa518a7e5d43',
                                  'InstanceType': 't1.micro',
                                  'Tags': [{'Key':'Name', 'Value': 'gcpVM1'}],
                                  'State': {'Code': '80', 'Name':'stopped'}}]
            resp["error_code"]=0
        elif op == 'azure':
            my_lc=LavaAzure()
            myfilters=['lava']
            if 'values' in qs:
                for value in qs['values']:
                    myfilters.append(value)
            resp=my_lc.list_instances(myfilters)
            resp["error_code"]=0
        else:
            resp["instances"] = [{'ImageId': 'azure-11223232',
                                  'InstanceId': 'azure-0aa518a7e5d43',
                                  'InstanceType': 't1.micro',
                                  'Tags': [{'Key':'Name', 'Value': 'azureVM1'}],
                                  'State': {'Code': '80', 'Name':'stopped'}}]
            resp["error_code"]=0
        return resp


    def find_operation(self, req):
        #op_res = {'operation':'create_instance','status':'fail', 'error':'Not Authenticated' }
        qs = falcon.uri.parse_query_string(req.query_string)
        opres={}
        # print(req.query_string)
        if "op" in qs:
            myop = qs["op"]
            opres =self.do_operation(myop,qs)
        else:
            opres["error_code"]=100
        return opres

    def on_get(self, req, resp):
        doc = self.find_operation(req)
        resp.text = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
