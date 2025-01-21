from setuptools import setup, find_packages
import os

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read() if os.path.exists('README.md') else ''

setup(
    name='wagtail-menubuilder',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'wagtail>=6.0',
        'Django>=4.2',
    ],
    python_requires='>=3.8',
    author='Bill Fleming',
    description='A flexible menu builder for Wagtail CMS',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/TechBill/wagtail-menubuilder',
    license='MIT',
    keywords='wagtail, wagtail menu, wagtail CMS, django, menu builder',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)