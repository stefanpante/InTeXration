import argparse
import logging.config
from intexration import config
from intexration.helper import ApiHelper
from intexration.server import Server

# Logger
logging.config.fileConfig(config.FILE_LOGGING)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', help='Change the hostname')
    parser.add_argument('-port', help='Change the port')
    parser.add_argument('-add', help='Add API key')
    parser.add_argument('-remove', help='Remove API key')
    parser.add_argument('-list', help='List API keys', action='store_true')

    if not config.all_files_exist():
        raise RuntimeError("Some necessary files were missing. Please consult the log.")

    config_mode = False
    args = parser.parse_args()
    if args.host is not None:
        config.write('SERVER', 'host', args.host)
        logging.info("Host changed to %s", args.host)
        config_mode = True
    if args.port is not None:
        config.write('SERVER', 'port', args.port)
        config_mode = True
        logging.info("Port changed to %s", args.port)
    if args.add is not None:
        ApiHelper(config.FILE_API_KEY).add(args.add)
        logging.info("API key added.")
        config_mode = True
    if args.remove is not None:
        ApiHelper(config.FILE_API_KEY).remove(args.remove)
        logging.info("API key %s removed.", args.remove)
        config_mode = True
    if args.list:
        for line in ApiHelper(config.FILE_API_KEY).get_all():
            print(line[0])
        config_mode = True
    if config_mode:
        quit()

    server = Server(host=config.read('SERVER', 'host'),
                    port=config.read('SERVER', 'port'))
    server.start()

if __name__ == '__main__':
    main()