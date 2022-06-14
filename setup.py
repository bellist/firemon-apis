from setuptools import setup, find_packages  # noqa: H301

NAME = "security-manager-apis"
VERSION = "0.2.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
REQUIRES = ["requests>=2.20.1"]

with open("README.md","r") as fh:
    long_description = fh.read()


setup(
    name=NAME,
    version=VERSION,
    description="Security Manager API",
    author_email="",
    url="",
    keywords=["Security Manager APIs"],
    install_requires=REQUIRES,
    python_requires ='>=3.6',
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    package_data={'':['*']},
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description=long_description
    
)