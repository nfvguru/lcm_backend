import falcon
from .backend_ctrl import InstanceCtrl

app = application = falcon.App()


instance_ctrl = InstanceCtrl()
app.add_route('/instance',instance_ctrl)
