import falcon
from .backend_ctrl import MainCtrl

app = application = falcon.App()


main_ctrl = MainCtrl()
app.add_route('/instance',main_ctrl)
