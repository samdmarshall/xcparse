from setuptools import setup

setup(
    name='xcparse',
    version='0.1',
    description='Xcode Build System Library',
    url='https://github.com/samdmarshall/xcparse',
    author='Sam Marshall',
    author_email='me@samdmarshall.com',
    license='BSD 3-Clause',
    package_data = {'xcparse/Xcode/XCConfig': ['defaults.xcconfig', 'runtime.xcconfig']},
    packages=[
        'xcparse', 
        'xcparse/Helpers',
        'xcparse/Xcode',
        'xcparse/Xcode/PBX',
        'xcparse/Xcode/XCSchemeActions',
        'xcparse/Xcode/XCConfig'
        'xcparse/Xcode/BuildSystem',
        'xcparse/Xcode/BuildSystem/XCSpec',
        'xcparse/Xcode/BuildSystem/LangSpec',
        'xcparse/Xcode/BuildSystem/Environment'
    ],
    zip_safe=False
)