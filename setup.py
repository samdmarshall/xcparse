from setuptools import setup

setup(
    name='xcparse',
    version='0.1',
    description='Xcode Build System Library',
    url='https://github.com/samdmarshall/xcparse',
    author='Sam Marshall',
    author_email='me@samdmarshall.com',
    license='BSD 3-Clause',
    package_data = {'xcparse': ['defaults.xcconfig']},
    packages=[
        'xcparse/xcparse', 
        'xcparse/xcparse/Helpers', 
        'xcparse/xcparse/Xcode', 
        'xcparse/xcparse/Xcode/PBX', 
        'xcparse/xcparse/Xcode/XCSchemeActions', 
        'xcparse/xcparse/Xcode/BuildSystem', 
        'xcparse/xcparse/Xcode/BuildSystem/XCSpec', 
        'xcparse/xcparse/Xcode/BuildSystem/LangSpec',
        'xcparse/xcparse/Xcode/BuildSystem/Environment'
    ],
    zip_safe=False
)