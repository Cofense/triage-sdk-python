from cofense_triage.triage_api_client import TriageApiClient


class TestTriageApiClient:
    def test_init(self, mocker, requests_mock):
        mock_session = mocker.patch("jsonapi_client.Session")
        mock_auth = mocker.patch("cofense_triage.triage_api_client.OAuth2Auth")

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

        TriageApiClient(
            host="https://some-triage-host",
            api_version=2,
            client_id="great_client_id",
            client_secret="great_client_secret",
        )

        mock_auth_args = mock_auth.call_args[0][0]
        assert mock_auth_args["access_token"] == "great-access-token"

        mock_session.assert_called_once_with(
            "https://some-triage-host", request_kwargs={"auth": mock_auth()}
        )
