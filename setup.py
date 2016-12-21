from setuptools import setup, find_packages

setup(name='hloopy',
      version='0.0.0',
      description=u"Python tools for analyzing hysteresis loops",
      classifiers=[],
      keywords='matplotlib, scipy, numpy',
      author=u"Julian Irwin",
      author_email='julian.irwin@gmail.com',
      url='https://github.com/julianirwin/hloopy',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['mock'],
      setup_requires=['nose>=1.0', 
                      'numpy>=1.0', 
                      'scipy>=0.18', 
                      'pandas>=0.18.1',
                      'matplotlib>=1.5.3'],
      extras_require={
          'test': ['nose'],
      },
      test_suite = 'nose.collector',
      # entry_points = {
      #     'console_scripts': ['bpl4_quickplot=batchplotlib4.bpl4_quickplot:main'],
      #     }
      )
