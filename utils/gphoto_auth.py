#!/usr/bin/env python

from gphotospy import authorize
from gphotospy.album import Album
from gphotospy.media import Media

CLIENT_SECRET_FILE = "gphotos.secret.json"

service = authorize.init(CLIENT_SECRET_FILE)

album_manager = Album(service)
media_manager = Media(service)

ALBUM_ID_WIDEBOY = (
    "AFbCb1EzvgohdOwFFxOoK67fCMyh6QlglIBjXkqNs2B4w-_mQcl9S_0fZXyJvcwQcE8nrKCUUP2A"
)

print("Getting a list of albums...")
album_iterator = album_manager.list()

for _ in range(3):
    try:
        # Print only album's title (if present, otherwise None)
        print(next(album_iterator).get("title"))
    except (StopIteration, TypeError) as e:
        # Handle exception if there are no albums left
        print("No (more) albums.")
        break

print("Getting WideBoy Album")
album = album_manager.get(ALBUM_ID_WIDEBOY)
# print(album)

search_iterator = media_manager.search_album(ALBUM_ID_WIDEBOY)
try:
    for _ in range(2):
        image = next(search_iterator)
        print(image.get("baseUrl"))
except (StopIteration, TypeError) as e:
    print("No (more) media in album {}.".format(album_title))
