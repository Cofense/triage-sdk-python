import setuptools
import pathlib


def read_readme():
    with open(pathlib.Path(__file__).parent / "README.md") as f:
        return f.read()


setuptools.setup(
    name="cofense_triage",
    version="0.1.0",
    author="Eddie Lebow",
    author_email="oss@cofense.com",
    maintainer="Cofense, Inc.",
    maintainer_email="oss@cofense.com",
    url="https://github.com/cofense/triage-sdk-python",
    description="Python interface to the Cofense Triage API V2",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    packages=setuptools.find_packages(),
    package_data={
        "cofense_triage": ["schema.json"]
    },
    install_requires=[
        "requests_oauthlib",
        "jsonapi_client",
    ],
)
