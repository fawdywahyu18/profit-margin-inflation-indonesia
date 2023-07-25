# Setup for estimations-all "unveiling the supply side inflation in Indonesia: Profits or Wages?"

from setuptools import setup

setup(
    name='estimations-all',
    version='0.1.0',
    py_modules=['estimations-all'],
    install_requires=[
        'et-xmlfile==1.1.0',
        'numpy==1.23.5',
        'openpyxl==3.0.10',
        'pandas==1.5.2',
        'python-dateutil==2.8.2',
        'pytz==2023.3',
        'six==1.16.0',
    ],
    entry_points='''
        [console_scripts]
        estimations-all=estimations-all:estimations-all
    ''',
)
