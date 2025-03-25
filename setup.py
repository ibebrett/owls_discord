from setuptools import setup


setup(
    name="owls_discord",
    version="1.0",
    description="An experiment in building a discord bot",
    author="SCSU CS Club",
    packages=["owls_discord"],
    entry_points={
        "console_scripts": [
            "owls_discord_server=owls_discord.server:main",
            "owls_discord_server_setup_db=owls_discord.db:setup_db",
        ]
    },
)
