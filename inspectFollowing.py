from igramscraper.instagram import Instagram
import pickle
import os
from time import sleep
import pickle

instagram = Instagram()

# username = os.environ.get('IG_USERNAME')
# password = os.environ.get('IG_PASSWORD')
# instagram.with_credentials(username, password)
# instagram.with_credentials(username, password)
# instagram.login()
# sleep(1)
# instagram = Instagram()

medias = instagram.get_medias("iubloomington", 1)
media = medias[0]

print(media)
account = media.owner
print(account)


# f = open('iub_following.pkl', 'rb')
# iub_following = pickle.load(f)

# account = instagram.get_account('iubloomington')
# sleep(2)
comments = comments = instagram.get_media_comments_by_id(media.identifier, 10000)
# f = open('iub_comments.pkl', 'wb')
# pickle.dump(comments, f)
for comment in comments['comments']:
    print(comment.text)
    print(comment.owner)
# for user in iub_following['accounts']:
#     if 'iubloomington' in user.username:
#         print(user.username)