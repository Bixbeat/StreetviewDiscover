from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='streetviewdiscover',
    version='0.1',
    description='Simple functions for discovering current and historic Google Streetview panorama IDs in polygons of a given region',
    long_description=readme(),
    url='https://github.com/Bixbeat/streetviewdiscover',
    author='Alex Levering',
    author_email='alex.levering@wur.nl',
    license='MIT',
    packages=['svdiscover'],
    install_requires=['geopandas'],
    zip_safe=False
#     test_suite='nose.collector',
#     tests_require=['nose'],
)
