"""setuptools based setup module for pyinfog.
"""

from setuptools import setup, find_packages

setup(
    name='sample',

    version='0.1.2',

    description='Python Infographics',
    long_description="",

    url='https://github.com/niallmcc/pyinfog',

    author='Niall McCarroll',
    author_email='',

    license='Apache2',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: Apache',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='infographics data visualization',

    packages=find_packages(exclude=[]),

    install_requires=[],

    extras_require={
    },

    package_data={
    },

    entry_points={
    },
)