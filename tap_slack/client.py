import time
import requests
import singer
import slack

from tap_framework.client import BaseClient


LOGGER = singer.get_logger()


class SlackClient(BaseClient):

    def __init__(self, config):
        super().__init__(config)

    def get_webclient(self):

        client = slack.WebClient(token=self.config.get("token"))
        return client

    def get_conversations(self):

        client = self.get_webclient()

        response = client.conversations_list()

        done = False
        pages = 0
        while done is False:
            if response.get('has_more') is False:
                done = True
            else:
                next_cursor = response.get('response_metadata').get('next_cursor')
                try:
                    response = client.conversations_list(cursor=next_cursor)
                except Exception:
                    if response.get('ok'):
                        pages += 1
                        print(pages)
                    elif response.get('ok') is False and response["headers"]["Retry-After"]:
                        delay = int(response["headers"]["Retry-After"])
                        print("Rate limited. Retrying in " + str(delay) + " seconds")
                        time.sleep(delay)
                        pages += 1
                        print(pages)
