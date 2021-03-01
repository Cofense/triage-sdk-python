from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session, OAuth2
import jsonapi_client

from cofense_triage.filter_params import FilterParams
from cofense_triage import TRIAGE_SCHEMA


class TriageApiClient:
    def __init__(self, *, host, api_version, client_id, client_secret):
        if not api_version == 2:
            raise "unsupported API version"

        self.host = host
        self.api_version = api_version
        self.client_id = client_id
        self.client_secret = client_secret

        self.oauth_session, self.oauth_auth = self._build_auth_object()
        self.jsonapi_session = self._build_jsonapi_session()

    def _build_auth_object(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth_session = OAuth2Session(client=client)
        token = oauth_session.fetch_token(
            token_url=f"{self.host}/oauth/token",
            client_id=self.client_id,
            client_secret=self.client_secret,
        )

        return (
            oauth_session,
            OAuth2(client_id=self.client_id, client=client, token=token),
        )

    def _build_jsonapi_session(self):
        # TODO we have to deal with token expiration ourselves. jsonapi_session should be able to take an OAuth2Session.
        return jsonapi_client.Session(
            f"{self.host}/api/public/v{self.api_version}",
            request_kwargs={"auth": self.oauth_auth},
            schema=TRIAGE_SCHEMA,
            use_relationship_iterator=True,
        )

    def get_documents(self, resource_type, filter_params=None):
        if filter_params:
            return self.jsonapi_session.iterate(
                resource_type, FilterParams(filter_params)
            )

        return self.jsonapi_session.iterate(resource_type)

    def create_documents(self, resource_type, resources):
        for resource in resources:
            # Triage properties contain underscores, so use `fields` instead of expanding kwargs
            new_resource = self.jsonapi_session.create(resource_type, fields=resource)

            # The resource must be manually added to the session. Perhaps a bug in jsonapi_client.
            self.jsonapi_session.add_resources(new_resource)

        return self.jsonapi_session.commit()
