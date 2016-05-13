from glusto.core import Glusto as g


def main():
    """Entry point console script for setuptools.

    Provides a command-line interface to Glusto.

    Currently does nothing useful, but plan to wrap Glusto functionality in a
    CLI interface that can be injected into shell scripts, etc.

    Example:
        # glusto run hostname.example.com "uname -a"
    """
    g.log.info("Starting glusto via main()")
    print "Starting glusto via main()"

    g.log.info("Ending glusto via main()")
    print "Ending glusto via main()"

if __name__ == '__main__':
    main()
