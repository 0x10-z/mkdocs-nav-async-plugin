from setuptools import setup, find_packages

setup(
    name='mkdocs-nav-async-plugin',
    version='0.1',
    description='MkDocs plugin to extract navigation and load it asynchronously',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/0x10-z/mkdocs-nav-async-plugin",
    author='0x10',
    install_requires=['mkdocs', 'beautifulsoup4'],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'nav_async = plugin:NavAsyncPlugin',
        ]
    }
)
