from setuptools import setup
from settings import __project_name__, __version__

setup(
    name=__project_name__,
    version=__version__,
    description='Network layout optimizator.',
    author='Victor Magalhaes',
    author_email='victormagalhaes01@gmail.com',
    include_package_data=True,
    install_requires=[
        'numpy>=1.13.0',
        'geojson>=2.4.0',
        'vincenty>=0.1.4',
        'click>=6.7',
    ],
    entry_points = '''
    [console_scripts]
        netopt = NetworkOptmization:cli
    ''',
)