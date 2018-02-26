# -*- coding: utf-8 -*-

from setuptools import setup as st_setup
from setuptools import find_packages as st_find_packages
from sys import argv, version_info
import hydratk.lib.install.task as task
import hydratk.lib.system.config as syscfg

try:
    os_info = syscfg.get_supported_os()
except Exception as exc:
    print(str(exc))
    exit(1)

with open("README.rst", "r") as f:
    readme = f.read()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]


def version_update(cfg, *args):

    major, minor = version_info[0], version_info[1]

    if (major == 2 and minor == 6):
        cfg['modules'].append({'module': 'simplejson', 'version': '==3.8.2'})
    else:
        cfg['modules'].append({'module': 'simplejson', 'version': '>=3.8.2'})

    if (major == 3):
        cfg['libs']['lxml']['freebsd']['pkg'] = ['py36-lxml']

config = {
    'pre_tasks': [
        version_update,
        task.install_libs,
        task.install_modules
    ],

    'post_tasks': [
        task.set_config,
        task.create_dirs,
        task.copy_files,
        task.set_access_rights,
        task.set_manpage
    ],

    'modules': [
        {'module': 'hydratk', 'version': '>=0.5.0'},
        {'module': 'lxml',    'version': '>=3.3.3'},
        {'module': 'pytz',    'version': '>=2016.6.1'}
    ],

    'dirs': [
        '/tmp/test_output/html',
        '/tmp/test_output/text',
        '/tmp/jenkins'
    ],

    'files': {
        'config': {
            'etc/hydratk/conf.d/hydratk-ext-yoda.conf': '{0}/hydratk/conf.d'.format(syscfg.HTK_ETC_DIR)
        },
        'data': {
            'var/local/hydratk/yoda/yoda-tests/test1/example1.jedi': '{0}/hydratk/yoda/yoda-tests/test1'.format(syscfg.HTK_VAR_DIR),
            'var/local/hydratk/yoda/helpers/yodahelpers/__init__.py': '{0}/hydratk/yoda/helpers/yodahelpers'.format(syscfg.HTK_VAR_DIR),
            'var/local/hydratk/yoda/lib/yodalib/__init__.py': '{0}/hydratk/yoda/lib/yodalib'.format(syscfg.HTK_VAR_DIR),
            'var/local/hydratk/yoda/db_testdata/db_struct.sql': '{0}/hydratk/yoda/db_testdata'.format(syscfg.HTK_VAR_DIR),
            'var/local/hydratk/yoda/db_testdata/db_data.sql': '{0}/hydratk/yoda/db_testdata'.format(syscfg.HTK_VAR_DIR),
            'var/local/hydratk/yoda/templates/test_reports/html/default/body.html': '{0}/hydratk/yoda/templates/test_reports/html/default'.format(syscfg.HTK_VAR_DIR)
        },
        'manpage': 'doc/yoda.1'
    },

    'libs': {
        'lxml': {
            'debian': {
                'apt-get': [
                    'python-lxml',
                    'libxml2-dev',
                    'libxslt1-dev'
                ],
                'check': {
                    'python-lxml': {
                        'cmd': 'dpkg --get-selections | grep python-lxml',
                        'errmsg': 'Unable to locate package python-lxml'
                    },
                    'libxml2-dev': {
                        'cmd': 'dpkg --get-selections | grep libxml2-dev',
                        'errmsg': 'Unable to locate package libxml2-dev'
                    },
                    'libxslt1-dev': {
                        'cmd': 'dpkg --get-selections | grep libxslt1-dev',
                        'errmsg': 'Unable to locate package libxslt1-dev'
                    }
                }
            },
            'redhat': {
                'yum': [
                    'python-lxml',
                    'libxml2-devel',
                    'libxslt-devel'
                ],
                'check': {
                    'python-lxml': {
                        'cmd': 'yum list installed | grep python-lxml',
                        'errmsg': 'Unable to locate package python-lxml'
                    },
                    'libxml2-devel': {
                        'cmd': 'yum list installed | grep libxml2-devel',
                        'errmsg': 'Unable to locate package libxml2-devel'
                    },
                    'libxslt-devel': {
                        'cmd': 'yum list installed | grep libxslt-devel',
                        'errmsg': 'Unable to locate shared library libxslt-devel'
                    }
                }
            },
            'fedora': {
                'dnf': [
                    'python-lxml',
                    'libxml2-devel',
                    'libxslt-devel'
                ],
                'check': {
                    'python-lxml': {
                        'cmd': 'dnf list installed | grep python-lxml',
                        'errmsg': 'Unable to locate package python-lxml'
                    },
                    'libxml2-devel': {
                        'cmd': 'dnf list installed | grep libxml2-devel',
                        'errmsg': 'Unable to locate package libxml2-devel'
                    },
                    'libxslt-devel': {
                        'cmd': 'dnf list installed | grep libxslt-devel',
                        'errmsg': 'Unable to locate shared library libxslt-devel'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'python-lxml',
                    'libxml2-devel',
                    'libxslt-devel'
                ],
                'check': {
                    'python-lxml': {
                        'cmd': 'rpm -qa | grep python-lxml',
                        'errmsg': 'Unable to locate package python-lxml'
                    },
                    'libxml2-devel': {
                        'cmd': 'rpm -qa | grep libxml2-devel',
                        'errmsg': 'Unable to locate package libxml2-devel'
                    },
                    'libxslt-devel': {
                        'cmd': 'rpm -qa | grep libxslt-devel',
                        'errmsg': 'Unable to locate shared library libxslt-devel'
                    }
                }
            },
            'freebsd': {
                'pkg': [
                    'py27-lxml'
                ],
                'check': {
                    'py27-lxml': {
                        'cmd': 'pkg info | grep py27-lxml',
                        'errmsg': 'Unable to locate package py27-lxml'
                    },
                    'py36-lxml': {
                        'cmd': 'pkg info | grep py36-lxml',
                        'errmsg': 'Unable to locate package py36-lxml'
                    }                          
                }
            }
        }
    },

    'rights': {
        '{0}/hydratk'.format(syscfg.HTK_ETC_DIR): 'a+r',
        '{0}/hydratk'.format(syscfg.HTK_VAR_DIR): 'a+rwx',
        '/tmp/test_output': 'a+rwx'
    }
}

task.run_pre_install(argv, config)

entry_points = {
    'console_scripts': [
        'yoda = hydratk.extensions.yoda.bootstrapper:run_app'
    ]
}

st_setup(
    name='hydratk-ext-yoda',
    version='0.2.4',
    description='Test Automation Tool',
    long_description=readme,
    author='Petr Czaderna, HydraTK team',
    author_email='pc@hydratk.org, team@hydratk.org',
    url='http://extensions.hydratk.org/yoda',
    license='BSD',
    packages=st_find_packages('src'),
    package_dir={'': 'src'},
    classifiers=classifiers,
    zip_safe=False,
    entry_points=entry_points,
    keywords='hydratk,testing,test automation,engine',
    requires_python='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
    platforms='Linux,FreeBSD'
)

task.run_post_install(argv, config)
