# installation: pip install blog-to-json
from setuptools import setup, find_packages

# read requirements.txt for requires, filter comments and newlines.
sanitize = lambda x: not x.startswith("#") and not x.startswith("\n")
with open("requirements.txt", "r") as f:
    requires = filter(sanitize, f.readlines())

setup(
    name="blog-to-json",
    version="0.1.0",
    description="Convert Various blogs dumps to JSON",
    keywords="Convert Wordpress Disqus XML dumps to JSON ",
    long_description=open("README.rst").read(),
    author="Russell Ballestrini",
    author_email="russell@ballestrini.net",
    url="https://github.com/russellballestrini/blog-to-json",
    license="Public Domain",
    packages=find_packages(),
    install_requires=requires,
    tests_require=["nose", "mock", "funcsigs", "pytest"],
    setup_requires=["pytest-runner"],
    entry_points={
        "console_scripts": [
            "blog-to-json = blog_to_json.__main__:main",
            "wordpress-xml-to-json = blog_to_json.__main__:main_wordpress",
            "disqus-xml-to-json = blog_to_json.__main__:main_disqus",
            "graphcomment-xml-to-json = blog_to_json.__main__:main_graphcomment",
        ]
    },
    classifiers=[
        "Intended Audience :: Developers, Operators, System Administrators",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)

"""
setup()
  keyword args: http://peak.telecommunity.com/DevCenter/setuptools
configure pypi username and password in ~/.pypirc::
 [pypi]
 username:
 password:
build and upload to pypi with this::
 python setup.py sdist bdist_egg register upload
"""
