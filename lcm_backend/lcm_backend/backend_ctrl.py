import json
import falcon
from pprint import pprint
#from .lawscli import LawsCli
#from .testmodule import TestModule
from .LavaAws import LavaAws


class InstanceCtrl:

    def do_operation(self, op, qs):
        my_lc=LavaAws()
        resp={}
        if op == '1':
            myfilters=[]
            myvalues=['lava_srvr']
            if 'values' in qs:
                for value in qs['values']:
                    myvalues.append(value)
            F1={'Name':'tag:Name','Values':myvalues}
            myfilters.append(F1)
            resp=my_lc.list_instances(myfilters)
        elif op == '2':
            resp["error_code"]=200
        else:
            resp["error_code"]=300
        return resp


    def find_operation(self, req):
        #op_res = {'operation':'create_instance','status':'fail', 'error':'Not Authenticated' }
        qs = falcon.uri.parse_query_string(req.query_string)
        opres={}
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
