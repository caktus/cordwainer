import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


with open('README.rst') as file:
    long_description = file.read()


# http://tox.readthedocs.org/en/latest/example/basic.html#integration-with-setuptools-distribute-test-commands
class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)


setup(
    name='cordwainer',
    version='0.0.2',
    packages=find_packages(),
    url='https://github.com/caktus/cordwainer',
    license='APL2',
    author='Dan Poirier',
    author_email='dpoirier@caktusgroup.com',
    description='A better CSV module',
    install_requires=[
        'six>=1.7',
    ],
    tests_require=[
        'tox>=1.7',
        # Other test requirements are installed in each venv,
        #  per `tox.ini` file.
    ],
    cmdclass={'test': Tox},
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
    ],
)
