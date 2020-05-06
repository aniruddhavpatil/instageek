import os
from igramscraper.instagram import Instagram
from time import sleep
import pickle

instagram = Instagram()

def main():
    pass

def get_following(username, limit=500):
    filename = username + '_following.pkl'
    if os.path.exists(filename):
        f = open(filename, 'rb')
        following = pickle.load(f)
        return following

    else:
        # instagram = Instagram()
        account = instagram.get_account(username)
        sleep(1)
        try:
            following = instagram.get_following(account.identifier, limit, 100, delayed=True)
            f = open(filename, 'wb')
            pickle.dump(following, f)
            sleep(5)
            return following
        except:
            return None


def get_followers(username, limit=500):
    filename = username + '_followers.pkl'
    if os.path.exists(filename):
        f = open(filename, 'rb')
        followers = pickle.load(f)

    else:
        # instagram = Instagram()
        account = instagram.get_account(username)
        sleep(1)
        try:
            followers = instagram.get_followers(account.identifier, limit, 100, delayed=True)
            f = open(filename, 'wb')
            pickle.dump(followers, f)
        except:
            pass

    return followers

def get_media(username, limit=200):
    filename = username + '_media.pkl'
    if os.path.exists(filename):
        f = open(filename, 'rb')
        media = pickle.load(f)
    else:
        # instagram = Instagram()
        media = instagram.get_medias(username, limit)
        f = open(filename, 'wb')
        pickle.dump(media, f)
    return media


def get_comments(media, comment_limit=100):
    filename = username + '_comments.pkl'
    if os.path.exists(filename):
        f = open(filename, 'rb')
        comments = pickle.load(f)
    else:
        comments = []
        for m,medium in enumerate(media):
            print("Medium number:", m)
            if m > 0 and m % 100 == 0:
                ckpt_filename = username + '_comments_ckpt' + str(m) + '.pkl'
                f = open(ckpt_filename, 'wb')
                pickle.dump(comments, f)
                print("Saved", ckpt_filename)
                sleep(2)
            medium_comments = instagram.get_media_comments_by_id(medium.identifier, comment_limit)
            for comment in medium_comments['comments']:
                comment.medium_identifier = medium.identifier
                comments.append(comment)
        f = open(filename, 'wb')
        pickle.dump(comments, f)

    return comments

if __name__ == "__main__":

    username = os.environ.get('IG_USERNAME')
    password = os.environ.get('IG_PASSWORD')
    instagram.with_credentials(username, password)
    instagram.login()
    username = 'iubloomington'
    print("Scraping following.")
    following = get_following(username, 356)
    for u,user in enumerate(following['accounts']):
        print(u, user.username)
        _ = get_following(user.username, 100)
    print("Scraping following complete.")
    print("Scraping media.")
    media = get_media(username,2311)
    print("Scraping media complete.")
    print("Scraping comments.")
    comments = get_comments(media, 1000)
    print("Scraping comments complete.")
    print("Scraping complete.")