from setuptools import setup, find_packages

import os

if __name__ == "__main__":

    setup(
        name="inspire11_app",
        version=os.getenv("PACKAGE_VERSION", "0.0.dev0"),
        package_dir={"": "src"},
        packages=find_packages(
            "src",
            include=["common", "raw*", "dm*"],
        ),
        description="An Inspire11 package.",
    )
