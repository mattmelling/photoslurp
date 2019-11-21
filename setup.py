from setuptools import setup


def main():
    setup(name='photoslurp',
          packages=['photoslurp'],
          entry_points={
              'console_scripts': [
                  'photoslurp = photoslurp.photoslurp:_main'
              ]})


if __name__ == '__main__':
    main()
