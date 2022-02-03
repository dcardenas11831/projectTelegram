import csv
import datetime
from telethon.tl.functions.channels import GetFullChannelRequest


async def get_channels_messages(client, candidates):
    # To store the dicts that contains the information of each channel
    channels = []
    # Gets the data of the channel into a dict
    for candidate in candidates:
        channel = []
        async for message in client.iter_messages(candidate):
            chat = message.chat
            print(message.id, candidate, chat.id, chat.title, message.forwards, message.views)
            # print(message)
            cm = dict(id=message.id,
                      type='Admin action'
                      if not message.text and not message.views and not message.forwards else 'Message',
                      views=message.views, forwards=message.forwards,
                      has_replies=True if message.replies else False,
                      date=message.date,
                      text=message.text.replace(',', ' ').replace(';', ' ').replace('\n', '. ')
                      if message.text is not None else str(message.action).split('(')[0],
                      has_file=True if message.file else False,
                      has_document=True if message.document else False,
                      file_type=message.document.mime_type if message.document else None,
                      has_audio=True if message.audio else False,
                      has_photo=True if message.photo else False,
                      has_gif=True if message.gif else False,
                      candidate=candidate,
                      timestamp=datetime.datetime.now())
            channel.append(cm)
        channel_sorted = sorted(channel, key=lambda m: m['id'])
        cc = dict(candidate=candidate, channel=channel_sorted)
        channels.append(cc)

    # Print in csvs
    fieldnames = channels[0]['channel'][0].keys()
    today = datetime.datetime.now()
    for cc in channels:
        with open(str(today.year) + f"{today.month:02d}" + f"{today.day:02d}" + ' ' + cc['candidate'] + '.csv', 'w',
                  encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cc['channel'])


async def get_channels_properties(client, candidates):
    channels = []
    for candidate in candidates:
        channel_entity = await client.get_entity(candidate)
        channel_full_info = await client(GetFullChannelRequest(channel=channel_entity))
        channel = dict(id=channel_entity.id, username=channel_entity.username, title=channel_entity.title,
                       participants=channel_full_info.full_chat.participants_count, created_at=channel_entity.date,
                       is_broadcast=channel_entity.broadcast, is_megagroup=channel_entity.megagroup,
                       is_gigagroup=channel_entity.gigagroup,
                       about=channel_full_info.full_chat.about.replace(',', ' ').replace(';', ' ').replace('\n', '. ')
                       if channel_full_info.full_chat.about is not None else None,
                       timestamp=datetime.datetime.now())
        # print(channel_full_info.full_chat)
        channels.append(channel)

    # Print in csv
    fieldnames = channels[0].keys()
    today = datetime.datetime.now()
    with open(str(today.year) + f"{today.month:02d}" + f"{today.day:02d}" + ' channels_info.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(channels)
