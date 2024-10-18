from setuptools import setup, find_packages

setup(
    name='mkdocs-nav-async',
    version='0.5',
    description='MkDocs plugin to extract navigation and load it asynchronously',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/0x10-z/mkdocs-nav-async",
    author='Iker Ocio (0x10)',
    install_requires=['mkdocs', 'beautifulsoup4'],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'nav_async = mkdocs_nav_async.plugin:NavAsync',
        ]
    }
)
