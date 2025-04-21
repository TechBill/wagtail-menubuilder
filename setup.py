with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

from setuptools import setup, find_packages

setup(
    name="wagtail-menubuilder",
    version="0.2.0",
    packages=find_packages(include=["wagtail_menubuilder", "wagtail_menubuilder.*"]),
    include_package_data=True,
    install_requires=[
        "wagtail>=6.0",
        "Django>=4.2",
    ],
    author="Bill Fleming",
    description="A flexible menu builder for Wagtail CMS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TechBill/wagtail-menubuilder",
    license="MIT",
    classifiers=[
        "Framework :: Django",
        "Framework :: Wagtail",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
    project_urls={
        "Documentation": "https://github.com/TechBill/wagtail-menubuilder",
        "Source": "https://github.com/TechBill/wagtail-menubuilder",
        "Tracker": "https://github.com/TechBill/wagtail-menubuilder/issues",
    },
)