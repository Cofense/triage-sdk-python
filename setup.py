import setuptools

setuptools.setup(
    name="cofense_triage",
    version="0.1",
    description="",
    url="",
    author="",
    author_email="",
    license="",
    packages=setuptools.find_packages(),
    package_data={
        "cofense_triage": ["schema.json"]
    },
    install_requires=[
        "requests_oauthlib",
        "jsonapi_client",
    ],
)
