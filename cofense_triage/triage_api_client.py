from authlib.integrations.requests_client import OAuth2Session, OAuth2Auth
import jsonapi_client

from cofense_triage.filter_params import FilterParams
from cofense_triage import TRIAGE_SCHEMA


class TriageApiClient:
    def __init__(self, *, host, api_version, client_id, client_secret):
        if not api_version == 2:
            raise "unsupported API version"

        oauth2_session = OAuth2Session(client_id, client_secret)
        token = oauth2_session.fetch_token(f"{host}/oauth/token")
        auth = OAuth2Auth(token, client=oauth2_session)
        # TODO using OAuth2Auth directly instead of the session forces us to deal with token refreshing manually, which we have not implemented

        host_string = f"{host}/api/public/v{api_version}"
        self.jsonapi_session = jsonapi_client.Session(
            host_string,
            request_kwargs={"auth": auth},
            schema=TRIAGE_SCHEMA,
        )

    def get_document(self, resource_type, filter_params=None):
        if filter_params:
            return self.jsonapi_session.iterate(
                resource_type, FilterParams(filter_params)
            )

        return self.jsonapi_session.iterate(resource_type)

    def create_document(self, resource_type, **attrs):
        return self.jsonapi_session.create_and_commit(
            resource_type,
            fields=attrs,  # Triage properties contain underscores, so pass a dict as fields param
        )
