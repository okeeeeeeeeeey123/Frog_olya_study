from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'frog_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # ПРАВИЛЬНЫЙ ПУТЬ — launch в корне пакета
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='olya',
    maintainer_email='olya@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'even_number_publisher = frog_pkg.scripts.even_number_publisher:main',
        ],
    },
)