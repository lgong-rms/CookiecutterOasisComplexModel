from setuptools import setup
import re


'''
def readme():
    with open('README.md') as f:
        return f.read()
'''

version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open('{{cookiecutter.organization.replace(' ', '').lower()}}_{{cookiecutter.model_identifier.replace(' ', '').lower()}}/__init__.py').read(),
    re.M
).group(1)

setup(name='{{cookiecutter.organization.replace(' ', '').lower()}}_{{cookiecutter.model_identifier.replace(' ', '').lower()}}',
      version=version,
      description='{{cookiecutter.organization.replace(' ', '').lower()}}_{{cookiecutter.model_identifier.replace(' ', '').lower()}}',
      long_description='{{cookiecutter.organization.replace(' ', '')}} {{cookiecutter.model_identifier.replace(' ', '')}} Model',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.6',
      ],
      author='{{cookiecutter.project_maintainer}}',
      author_email='{{cookiecutter.project_maintainer_email}}',
      packages=['{{cookiecutter.organization.replace(' ', '').lower()}}_{{cookiecutter.model_identifier.replace(' ', '').lower()}}'],
      install_requires=[
          'oasislmf',
          'pandas>=0.24.1',
          'msgpack'
      ],
      dependency_links=[
          'oasislmf>=1.3.10',
          'msgpack'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={
          'console_scripts': [
              'complex_itemtobin=oasislmf.model_execution.complex_items_to_bin:main',
              'complex_itemtocsv=oasislmf.model_execution.complex_items_to_csv:main'
          ],
      },
      include_package_data=True,
      zip_safe=False)
