from setuptools import find_packages, setup

setup(
    name='Scribes',
    version='1.0.0',
    description='Use Faust to manage memory pool and asynchronous task management in the scribe software',
    author='Connor Smith',
    packages=find_packages(exclude=['tests','tests.*']),
    python_requires='~=3.6',
    entry_points={
        'console_scripts': [
            'Scribes = Scribes.__main__:main',
            'Scribes-faust = faustapp.app:main',
        ],
    },
) 


