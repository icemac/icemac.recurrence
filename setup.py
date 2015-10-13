# -*- coding: utf-8 -*-
import os.path
import setuptools


def read(*path_elements):
    """Read file."""
    return file(os.path.join(*path_elements)).read()


version = '1.0.0'
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
    download_url='http://pypi.python.org/pypi/icemac.recurrence',
    url='https://bitbucket.org/icemac/icemac.recurrence',
    license='ZPL 2.1',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['icemac'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'gocept.month >= 1.3.2',
        'grokcore.component',
        'setuptools',
        'zope.cachedescriptors',
        'zope.component',
        'zope.globalrequest',
        'zope.i18nmessageid',
        'zope.interface',
    ],
    extras_require=dict(
        test=[
            'gocept.month [test]',
            'plone.testing',
            'pytest',
            'pytz',
            'zope.publisher',
        ]),
)
