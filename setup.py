from setuptools import setup

setup(
    name = 'cornlib',
    packages = ['cornlib'],
    version = '0.0.1',
    description = 'Personal library for analyzing JIAR and Gerrot',
    long_description=open('README.md').read(),
    author = 'Corn',
    author_email = 'yang.yuming@realtek.com',
    url = 'https://github.com/roger199585/cornlib',
    download_url = '',
    keywords = ['JIRA', 'Gerrit', 'RTK'],
    license = 'MIT',
    python_requires='>=3.6',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)