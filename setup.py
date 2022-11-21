from setuptools import setup

setup(
    name = 'cornlib',
    packages = ['cornlib'],
    version = '0.0.4',
    description = 'Personal library for analyzing JIAR and Gerrot',
    long_description=open('README.md').read(),
    author = 'Corn',
    author_email = 'yang.yuming@realtek.com',
    url = 'https://github.com/roger199585/cornlib',
    download_url = 'https://test.pypi.org/project/cornlib/',
    keywords = ['JIRA', 'Gerrit', 'RTK'],
    install_requires=[
        'jira',
        'pygerrit2'
    ],
    license = 'MIT',
    python_requires='>=3.6',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)