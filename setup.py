from setuptools import setup

setup(
    name='visual_regression_tracker_sdk',
    version='3.0.2',
    description='Open source, self hosted solution for visual testing '
                'and managing results of visual testing.',
    long_description=open('README.md').read(),
    author='',
    license='APACHE',
    url='https://github.com/Visual-Regression-Tracker/'
        'Visual-Regression-Tracker',
    packages=['visual_regression_tracker_sdk'],
    requires=['requests']
)
