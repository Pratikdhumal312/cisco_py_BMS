from setuptools import setup, find_packages

setup(
    name="bms",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "requests",
        "beautifulsoup4",
        "python-dotenv",
        "aiohttp",
        "asyncio",
        "selenium",
        "structlog"
    ],
)