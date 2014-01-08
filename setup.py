from setuptools import setup, find_packages

setup(
    name='django_backstage',
    version='0.0.59',
    description='Django project and site deployment using uWSGI, nginx, etc.',
    author='MiddleFork',
    author_email='walker@mfgis.com',
    packages=find_packages(),
    install_requires=[
        "setuptools_git >= 0.3",
    ],
    entry_points = {
      'console_scripts':
            'backstage_project = backstage.project:new_project'
    }
)
