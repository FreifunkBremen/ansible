import os

from sys import path
path.append("lib")

from ansible import utils
from ansible.runner.return_data import ReturnData
from slpp import slpp as lua
import httplib2

class ActionModule(object):

    def __init__(self, runner):
        self.runner = runner

    def run(self, conn, tmp_path, module_name, module_args, inject, complex_args=None):
        ''' fetch a lua object from a HTTP resource '''

        # load up options
        options = {}
        if complex_args:
            options.update(complex_args)
        options.update(utils.parse_kv(module_args))

        url = options.get('url')
        var = options.get('var')
        h   = httplib2.Http(".cache")

        (resp, content) = h.request(url, "GET")

        result      = {}
        status      = resp.status
        contenttype = resp["content-type"]
        error       = None

        if status != 200:
            error = "Fetching %s failed with status %s" % (url, status)
        elif contenttype not in ["text/plain", "text/plain; charset=utf-8"]:
            error = "Invalid content type: %s" % contenttype
        else:
            value = lua.decode(content)
            if isinstance(value, dict):
                result["ansible_facts"] = {var: value}
            else:
                error = "Unable to parse response"

        if error != None:
            result["failed"]  = True
            result["message"] = error

        return ReturnData(conn=conn, result=result)
