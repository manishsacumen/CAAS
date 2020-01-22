from slackclient import SlackClient


class SlackBot:
    """Slack bot client object."""

    ACTION_CHAT_POST_MESSAGE = 'chat.postMessage'
    
    def __init__(self, api_token):
        """
        Arguments:
            api_token {str} -- [description]
        """

        self.__api_token = api_token
        self.__client = SlackClient(api_token)
    
    def send_message(self, channel, text):
        """Send message to a channel.
        
        Arguments:
            channel {str} -- Channel name
            text {str} -- message to send
        """

        self.__client.api_call(self.ACTION_CHAT_POST_MESSAGE, channel=channel, text=text)
    
    def send_message_block(self, channel, block):
        """Send a formatted message block to a channel.
        
        Arguments:
            channel {str} -- channel name
            block {list} -- Blocks to send
        """

        self.__client.api_call(self.ACTION_CHAT_POST_MESSAGE, channel=channel, block=block)
