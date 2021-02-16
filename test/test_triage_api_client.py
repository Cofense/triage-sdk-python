from cofense_triage.triage_api_client import TriageApiClient


class TestTriageApiClient:
    def test__build_auth_object(self, mocker, requests_mock):
        requests_mock.post(
            "https://some-triage-host/oauth/token",
            text="""
                {
                    "access_token": "great-access-token",
                    "token_type": "bearer",
                    "expires_in": 3600,
                    "refresh_token": "great-refresh-token"
                }
            """,
        )
        mock_auth = mocker.patch("cofense_triage.triage_api_client.OAuth2")

        TriageApiClient(
            host="https://some-triage-host",
            api_version=2,
            client_id="great_client_id",
            client_secret="great_client_secret",
        )

        mock_auth_args = mock_auth.call_args[1]
        assert mock_auth_args["client_id"] == "great_client_id"
        assert mock_auth_args["token"]["access_token"] == "great-access-token"

    def test__build_jsonapi_session(self, mocker):
        mock_jsonapi_session = mocker.patch("jsonapi_client.Session")
        mock_auth_object = mocker.patch(
            "cofense_triage.triage_api_client.TriageApiClient._build_auth_object"
        )

        TriageApiClient(
            host="https://some-triage-host",
            api_version=2,
            client_id="great_client_id",
            client_secret="great_client_secret",
        )

        mock_jsonapi_session.assert_called_once_with(
            "https://some-triage-host/api/public/v2",
            request_kwargs={"auth": mock_auth_object()},
            schema=mocker.ANY,
        )
