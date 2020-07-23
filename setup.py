from setuptools import setup

setup(name='simple_smart_scale',
      version='0.1',
      description='minimal package for a scale project',
      url='https://github.com/madgen-content/simple_smart_scale',
      author='madgen_content',
      author_email='n/a',
      license='MIT',
      packages=['simple_smart_scale'],
      install_requires=[
            'pandas',
            'pysimplegui'
      ],
      zip_safe=False)