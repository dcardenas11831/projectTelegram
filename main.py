import telegram_client
from telethon import TelegramClient


def run_telegram():
    api_id = 14335782
    api_hash = '4d7e1d9fbc10c926343d7aa516d53f72'
    client = TelegramClient('anon', api_id, api_hash)
    # List of candidates, id número también sirve
    candidates = ['gustavopetrooficial', 'JERobledo', 'sergiofajardo', 'JuanManuelGalan', 'oscarivanzuluaga']

    # Session initializer
    with client:
        client.loop.run_until_complete(telegram_client.get_channels_properties(client, candidates))
        client.loop.run_until_complete(telegram_client.get_channels_messages(client, candidates))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_telegram()
