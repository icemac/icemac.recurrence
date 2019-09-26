# -*- coding: utf-8 -*-
import os.path
import setuptools


def read(*path_elements):
    """Read file."""
    with open(os.path.join(*path_elements)) as f:
        return f.read()


version = '1.7'
long_description = '\n\n'.join([
    read('README.rst'),
    read('CHANGES.rst'),
])

setuptools.setup(
    name='icemac.recurrence',
    version=version,
    description="Compute recurrences of events",
    long_description=long_description,
    keywords='calendar event recurring recurrence datetime',
    author='Michael Howitz',
    author_email='icemac@gmx.net',
    url='https://github.com/icemac/icemac.recurrence',
    download_url='https://pypi.org/project/icemac.recurrence',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['icemac'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'gocept.month >= 2',
        'grokcore.component >= 2.6',
        'setuptools',
        'zope.cachedescriptors',
        'zope.component',
        'zope.globalrequest',
        'zope.i18nmessageid',
        'zope.interface',
    ],
    extras_require=dict(
        test=[
            'zope.configuration',
        ]),
)
