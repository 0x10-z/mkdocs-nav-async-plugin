# Steps to upload a package to PyPI

1. **Create the structure of your package**:
   Make sure your project has the following basic structure:

   ```bash
   mkdocs-nav-async/
   ├── plugin.py
   ├── setup.py
   ├── README.md
   └── LICENSE
   ```

2. **Configure the `setup.py` file**:
   The `setup.py` file is essential to define your package. Here's a basic example:

   ```python
   from setuptools import setup, find_packages

   setup(
       name='mkdocs-nav-async-plugin',
       version='0.1',
       description='MkDocs plugin to extract navigation and load it asynchronously',
       long_description=open('README.md').read(),
       long_description_content_type='text/markdown',
       url="https://github.com/0x10-z/your-repo",
       author='0x10',
       install_requires=['mkdocs', 'beautifulsoup4'],
       packages=find_packages(),
       entry_points={
           'mkdocs.plugins': [
               'nav_async = plugin:NavAsyncPlugin',
           ]
       }
   )
   ```

3. **Register an account on PyPI**:
   If you don't already have a PyPI account, register here: [PyPI](https://pypi.org/account/register/)

4. **Install `twine`**:
   To upload your package, you'll need to use `twine`, a tool that allows you to securely upload packages to PyPI.

   Install `twine`:

   ```bash
   pip install twine
   ```

5. **Generate the necessary files for PyPI**:
   First, generate the distributable package (source distribution and wheel):

   ```bash
   python setup.py sdist bdist_wheel
   ```

   This will generate a `dist/` directory that contains `.tar.gz` and `.whl` files, which are the files you'll upload to PyPI.

6. **Upload to TestPyPI**:

   If you want to test the upload process before doing it on the official repository, you can use [TestPyPI](https://test.pypi.org/), which is PyPI's testing environment. The process is the same, but you'll be uploading to a test repository:

   ```bash
   twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ```

   Then you can install the test package with:

   ```bash
   pip install --index-url https://test.pypi.org/simple/ mkdocs-nav-async
   ```

7. **Upload the package to PyPI**:
   Use `twine` to upload the package to the official PyPI repository:

   ```bash
   twine upload dist/*
   ```

   It will prompt you for your PyPI credentials, and once uploaded, your package will be available for anyone to install using `pip`.

   ```bash
   pip install mkdocs-nav-async
   ```

## Can I delete the package after uploading?

Yes, **you can delete** a package from PyPI, but **only if you do it within the first 24 hours** after uploading it. After this period, you cannot delete the entire package, but **you can delete specific versions**.

### To delete the package

1. Go to the [PyPI website](https://pypi.org/).
2. Log in.
3. Navigate to your package in the **"Manage Project"** section.
4. You'll see an option to **"Delete entire project"** (if it's within 24 hours) or **"Delete version"** to remove specific versions.
