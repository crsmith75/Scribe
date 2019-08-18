from setuptools import setup, find_packages

requires = [
    "colorlog>=3.1.4",
    "robinhood-aiokafka>=1.0.3",
    "requests>=2.22.0",
    "simple-settings>=0.16.0",
    "python-schema-registry-client[faust]>=1.0.0",
]

setup(
    name='Scribes_Faust',
    version='1.0.0',
    description='Scribe Project',
    long_description='''
    Kafka, Faust, Djangp, Vue webapp to track tweets)
    ''',
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Connor Smith',
    author_email='',
    url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=[],
    setup_requires=[],
    dependency_links=[],
    entry_points={
        'console_scripts': [
            'daemon = daemon.app:main',
        ],
    },
)
