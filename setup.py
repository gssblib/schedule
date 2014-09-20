import os
from setuptools import setup, find_packages

setup(
    name='schedule',
    version='0.1.0',
    author='German Saturday School Boston',
    author_email='librarygssb@gmail.com',
    description='Post library schedule into Google Calendar',
    keywords = "console tools",
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent'],
    url='http://github.com/gssblib/schedule',
    license='BSD',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    install_requires=[
        'gdata',
        'setuptools',
        ],
    entry_points = dict(console_scripts=[
        'post-schedule = schedule.schedule:post_schedule',
        ]),
    include_package_data = True,
    zip_safe = False,
    )
