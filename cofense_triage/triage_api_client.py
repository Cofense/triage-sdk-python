from authlib.integrations.requests_client import OAuth2Session, OAuth2Auth
from cofense_triage.filter_params import FilterParams
import jsonapi_client


class TriageApiClient:
    def __init__(self, *, host, api_version, client_id, client_secret):
        if not api_version == 2:
            raise "unsupported API version"

        oauth2_session = OAuth2Session(client_id, client_secret)
        token = oauth2_session.fetch_token("https://tap.phishmecloud.com/oauth/token")
        auth = OAuth2Auth(token, client=oauth2_session)
        # TODO using OAuth2Auth directly instead of the session forces us to deal with token refreshing manually, which we have not implemented

        self.jsonapi_session = jsonapi_client.Session(
            "https://tap.phishmecloud.com", request_kwargs={"auth": auth}
        )

    def get_document(self, resource_type, filter_params=None):
        path = f"api/public/v2/{resource_type}"

        if filter_params:
            return self.jsonapi_session.iterate(path, FilterParams(filter_params))
