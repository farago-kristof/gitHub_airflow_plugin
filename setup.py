from setuptools import setup, find_packages

with open('src/requirements.txt') as f:
    reqs = f.read().splitlines()

setup(
    name='gh_airflow_plugin',
    version='1.0.0',
    description='A simple GH plugin for Airflow',
    url="https://github.com/farago-kristof/gitHub_airflow_plugin",
    python_requires='>=3.12',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=reqs
)