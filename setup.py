import setuptools

setuptools.setup(
    name="cofense_triage",
    version="0.1",
    description="Python interface to the Cofense Triage API V2",
    url="https://github.com/cofense/triage-sdk-python",
    author="Cofense, Inc.",
    author_email="oss@cofense.com",
    license="MIT",
    packages=setuptools.find_packages(),
    package_data={
        "cofense_triage": ["schema.json"]
    },
    install_requires=[
        "requests_oauthlib",
        "jsonapi_client",
    ],
)
