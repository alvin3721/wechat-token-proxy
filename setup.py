from setuptools import setup

setup(
    name='wtp',
    version='0.1.0',
    author='duckgogo',
    author_email='zeng.jianxin@foxmail.com',
    description='WeChat access_token proxy.',
    py_modules=['proxy'],
    packages=['.'],
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'flask',
        'requests'
    ]
)
