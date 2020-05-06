from igramscraper.instagram import Instagram
import os
from time import sleep
import pickle


instagram = Instagram()

# authentication supported
username = os.environ.get('IG_USERNAME')
password = os.environ.get('IG_PASSWORD')
instagram.with_credentials(username, password)
instagram.login()

account = instagram.get_account('aniruddhavpatil')

# Available fields
# print('Account info:')
# print('Id: ', account.identifier)
# print('Username: ', account.username)
# print('Full name: ', account.full_name)
# print('Biography: ', account.biography)
# print('External Url: ', account.external_url)
# print('Number of published posts: ', account.media_count)
# print('Number of followers: ', account.followed_by_count)
# print('Number of follows: ', account.follows_count)
# print('Is private: ', account.is_private)
# print('Is verified: ', account.is_verified)

# or simply for printing use
# print(account)

username = 'iubloomington'
account = instagram.get_account(username)
sleep(1)
following = instagram.get_following(account.identifier, 356, 100, delayed=True)
f = open('iub_following.pkl', 'wb')
pickle.dump(following, f)
print('Done')
