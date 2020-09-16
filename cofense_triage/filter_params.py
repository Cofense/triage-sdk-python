import jsonapi_client


class FilterParams(jsonapi_client.Filter):
    def __init__(self, params):
        """
        jsonapi_client.Filter takes conditions as kwargs, which only allows for attributes and
        values. We also want to support operations, so we'll replace the kwargs with a list of dicts
        having three keys: attribute, value, op.

        examples:
            Filter({"attribute": "name", "value": "Example"})
            Filter({"attribute": "name", "value": "Ex", "op": "start"})
            Filter({"attribute": "created_at", "value": "2000-01-01", "op": "gt"})
        """
        self._params = params

    def appended_query(self):
        return self.format_filter_query(self._params)

    def format_filter_query(self, params):
        def build_key(param):
            if "op" in param:
                return f"{param['attribute']}_{param['op']}"

            return param["attribute"]

        return "&".join(
            f"filter[{build_key(param)}]={param['value']}" for param in params
        )
