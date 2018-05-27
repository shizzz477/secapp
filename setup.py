from setuptools import setup

setup(
    name='secapp',
    version='1.0',
    packages=['app'],
    url='https://github.com/shizzz477/secapp',
    license='GNU Public License',
    author='Marc Gurreri',
    author_email='marcgurreri@gmail.com',
    description='Sample Secure Application',
    install_requires=[
        "request",
        "Flask",
        "Flask-WTF",
        "bcrypt",
        "Flask-login",
        "wtforms",
        "python-owasp-zap-v2.4"
    ]
)
