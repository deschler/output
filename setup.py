#!/usr/bin/env python
from distutils.core import setup

# Dynamically calculate the version based on output.VERSION.
version = __import__('output').get_version()


setup(
    name='output',
    version=version,
    description='Fancy output for your Python shell scripts.',
    long_description=open('README.rst').read(),
    author='Dirk Eschler',
    author_email='eschler@gmail.com',
    url='https://github.com/deschler/output',
    packages=['output'],
    download_url='https://github.com/downloads/deschler/output/output-%s.tar.gz' % version,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)'
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Shells',

    ],
    license='GPLv2'
)
