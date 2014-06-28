from setuptools import setup, find_packages
import backstage

setup(
    name='django_backstage',
    version=backstage.__version__,
    description='Django project and site deployment using virtualenv, uWSGI, nginx, etc.',
    author='MiddleFork',
    author_email='walker@mfgis.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "setuptools_git >= 0.3",
    ],
    entry_points = {
      'console_scripts':
            'backstage_venue = backstage.venue:new_venue'
    }
)
