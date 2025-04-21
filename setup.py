from setuptools import setup, find_packages

setup(
    name="wagtail-menubuilder",
    version="0.1.2",
    packages=find_packages(),  # THIS is what you're missing
    include_package_data=True,
    install_requires=[
        "wagtail>=6.0",
        "Django>=4.2",
    ],
    author="Bill Fleming",
    description="A flexible menu builder for Wagtail CMS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TechBill/wagtail-menubuilder",
    classifiers=[
        "Framework :: Django",
        "Framework :: Wagtail",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)