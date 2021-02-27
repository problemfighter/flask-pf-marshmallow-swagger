from flask import request


class PfRequestProcessor:

    def get_json(self):
        json = request.get_json()
        if json:
            return json
        return ""

