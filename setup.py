import os
from setuptools import setup, find_packages


version = "0.1"

install_requires = [
    'cached-property',
    'chameleon',
    'cromlech.jwt',
    'horseman',
    'wrapt',
]

test_requires = [
    'WebTest',
]


setup(
    name='arkivi',
    version=version,
    author='Adeline Nex',
    author_email='contact@arkivi.fr',
    url='http://www.arkivi.fr',
    download_url='',
    description='Arkivi WebSite',
    long_description=(open("README.txt").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.txt")).read()),
    license='ZPL',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python:: 3 :: Only',
        ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
        },
    )
