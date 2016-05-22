"""Glusto CLI wrapper"""
import argparse

from glusto.core import Glusto as g


def handle_configs(config_list):
    """Load default and user-specified configuration files"""

    # load default config
    g.glustolog.info("Loading default configuration files.")
    g.load_config_defaults()

    # load user specified configs
    if (config_list):
        g.glustolog.info("Loading user specified configuration files.")
        config_files = config_list.split()
        config = g.load_configs(config_files)
        g.update_config(config)

    # XXX: remove me
    g.show_config(g.config)


def main():
    """Entry point console script for setuptools.

    Provides a command-line interface to Glusto.

    Currently does nothing useful, but plan to wrap Glusto functionality in a
    CLI interface that can be injected into shell scripts, etc.

    Example:
        # glusto run hostname.example.com "uname -a"
    """
    g.glustolog.info("Starting glusto via main()")
    print "Starting glusto via main()"

    parser = argparse.ArgumentParser(description="Glusto CLI wrapper")
    parser.add_argument("-c", "--config",
                        help="Config file(s) to read.",
                        action="store", dest="config_list")
    args = parser.parse_args()

    # read config files and update g.config attributes
    handle_configs(args.config_list)

    # handle actionable config items
    # logging
    log_name = g.config.get('log_name', 'glustomain')
    log_filename = g.config.get('log_filename', '/tmp/glustomain.log')
    log_level = g.config.get('log_level', 'INFO')

    if log_filename:
        g.log = g.create_log(name=log_name, filename=log_filename,
                             level=log_level)
        g.log.info("Logfile %s created as %s "
                   "with log level %s", log_name, log_filename, log_level)

    g.glustolog.info("Ending glusto via main()")
    print "Ending glusto via main()"

if __name__ == '__main__':
    main()
