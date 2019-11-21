from setuptools import setup


def main():
    setup(name='photoslurp',
          entry_points={
              'console_scripts': [
                  'photoslurp = photoslurp:_main'
              ]})


if __name__ == '__main__':
    main()
