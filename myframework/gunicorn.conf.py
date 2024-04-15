import os

timeout = 90
bind = "0.0.0.0:" + str(os.environ.get('PORT', '8000'))
workers = 3