import singer
import tap_framework
import tap_slack.client

LOGGER = singer.get_logger()


class SlackRunner(tap_framework.Runner):
    pass


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(
        required_config_keys=['token', 'start_date'])

    slackclient = tap_slack.client.SlackClient(args.config)

    if args.discover:
        pass
    else:
        slackclient.get_conversations()


if __name__ == '__main__':
    main()
