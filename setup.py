from distutils.core import setup


with open("README.md", "r") as f:
    readme = f.readlines()
    
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",   
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",    
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython",    
    "Programming Language :: Python :: Implementation :: PyPy",    
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]

packages=[
          'hydratk.extensions.yoda', 
         ]
         
data_files=[
            ('/etc/hydratk/conf.d', ['config/hydratk-ext-yoda.conf']),
            ('/var/local/hydratk/yoda/yoda-tests/test1',['var/local/hydratk/yoda/yoda-tests/test1/example1.yoda']),
            ('/var/local/hydratk/yoda/yoda-helpers',['var/local/hydratk/yoda/yoda-helpers/__init__.py']),
            ('/var/local/hydratk/yoda/yoda-lib',['var/local/hydratk/yoda/yoda-lib/__init__.py'])
           ]         
                
setup(name='Yoda Tester',
      version='0.1.1a',
      description='Test Automation Tool',
      long_description=readme,
      author='Petr Czaderna',
      author_email='pc@hydratk.org',
      url='http://extensions.hydratk.org/yoda',
      license='BSD',
      packages=packages,
      package_dir={'' : 'src'},
      classifiers=classifiers,
      data_files=data_files      
     )