import os

from setuptools import setup, find_packages

install_requires = [
    'python-decouple',
    'python-dotenv',
    'requests',
    'boto3',
    'click',

    'pytest>=5.4.1',  # for mce_lib_aws.pytest.plugin
]

tests_requires = [
    'pytest>=5.4.1',
    'bandit',
    'flake8',
    'coverage',
    'pytest-cov',
    'pytest-pep8',
    'pytest-flake8',
    'black',
    'freezegun',
    'moto[server]',
]

dev_requires = [
    'pylint',
    'ipython',
    'autopep8',
    'twine',
    'wheel'
]

doc_requires = [
    'Sphinx>=3.0',
    'sphinx_rtd_theme',
    'sphinx-click',
    'sphinx-autodoc-typehints'
]

ci_requires = [
    'coveralls',
    'codecov',
]

extras_requires = {
    'tests': tests_requires,
    'dev': dev_requires,
    'doc': doc_requires,
    'ci': ci_requires,
    'gevent': [
        'gevent',
        'gevent-openssl',
    ]
}

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mce-lib-aws',
    version="0.1.0",
    description='MCE - SDK for AWS',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/multi-cloud-explorer/mce-lib-aws.git',
    license='GPLv3+',
    packages=find_packages(exclude=("tests",)),
    include_package_data=False, 
    tests_require=tests_requires,
    install_requires=install_requires,
    extras_require=extras_requires,
    test_suite='tests',
    zip_safe=False,
    author='Stephane RAULT',
    author_email="stephane.rault@radicalspam.org",
    python_requires='>=3.7',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'mce-aws = mce_lib_aws.cli:main',
        ],
    }
)
