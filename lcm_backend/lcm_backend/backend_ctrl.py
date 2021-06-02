import json
import falcon
#from .lawscli import LawsCli
#from .testmodule import TestModule
from .LavaAws import LavaAws


class MainCtrl:

    def test_operation(self):
        my_lc=LavaAws()
        #op_res = {'operation':'create_instance','status':'fail', 'error':'Not Authenticated' }
        op_res=my_lc.list_srvr_vm()
        return op_res

    def on_get(self, req, resp):
        doc = self.test_operation()
        resp.text = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
