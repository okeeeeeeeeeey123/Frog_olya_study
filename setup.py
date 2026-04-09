from setuptools import find_packages, setup

package_name = 'frog_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='olya',
    maintainer_email='olya@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'first_node = frog_pkg.scripts.first_node:main',   # ← добавляем эту строку
            'PR1_time_node = frog_pkg.scripts.PR1_time_node:main',   # ← добавляем эту строку
            'talker = frog_pkg.talker:main',   # ← добавляем эту строку
            'listener = frog_pkg.listener:main',   # ← добавляем эту строку
            'even_number_publisher = frog_pkg.scripts.even_number_publisher:main',   # ← добавляем эту строку
            'overflow_listener = frog_pkg.scripts.overflow_listener:main',
        ],
    },
)
