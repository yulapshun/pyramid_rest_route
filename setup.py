from setuptools import setup

from os import path

README = path.abspath(path.join(path.dirname(__file__), 'README.md'))

setup(
      name='pyramid_rest_route',
      version='0.1',
      packages=['pyramid_rest_route'],
      description='Simple helper for creating rest route and view',
      long_description=open(README).read(),
      author='Rick Mak',
      author_email='rick.mak@gmail.com',
      url='https://github.com/rickmak/pyramid_rest_route',
      license='MIT',
      requires=[]
)
