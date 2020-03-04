from setuptools import setup

# from pip.req import parse_requirements
import os

# install_reqs = parse_requirements('requirements.txt', session='hack')
package_version = "0.0.3"
# os.environ.get('CI_COMMIT_TAG') or '0.dev'

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

tests_dependencies = ["pytest", "pytest-cov", "responses", "testfixtures"]

setup(
    name="usersv8",
    version=package_version,
    description="Утилиты 1С:Разработчика",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=["requests", "lxml"],
    setup_requires=["pytest-runner"],
    tests_require=tests_dependencies,
    extras_require={"test": tests_dependencies},
    url="https://git.skbkontur.ru/ДобавитьАдрес",
    packages=["usersv8"],
    entry_points={"console_scripts": ["usersv8 = usersv8.cli:main"]},
    # maintainer='https://staff.skbkontur.ru/department/1854',
    # maintainer_email='https://staff.skbkontur.ru/department/1854',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
