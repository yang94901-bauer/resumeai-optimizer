# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project

import sys

# add your project directory to the sys.path
project_home = '/home/yang94901/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
import os
os.environ["KIMI_API_KEY"]="sk-dTLMiEPMe3zLJhS6TSFBunfcUI9yJJ6pyyrkgccsRIMviwL5"
os.environ["GUMROAD_PRODUCT_ID"]="GQ72Bapk2zdvwGrdzKnNQQ=="
os.environ["GUMROAD_API_KEY"]="i-pId0S7Q13nmrAY4pS5FIns3P-XQm8Z5tGLUass8JE"
from app import app as application  # noqa
