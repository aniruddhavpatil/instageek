import os
import pickle

from neo4j import GraphDatabase
from scrape import get_following
from igramscraper.instagram import Instagram

instagram = Instagram()


def add_medium(tx, src, medium):
    if not medium.caption:
        medium.caption = 'No Caption'

    tx.run("MATCH (a:Account {identifier: $src_identifier}) "
           "MERGE (m:Medium {"
           "identifier: $medium_identifier,"
           "caption: $medium_caption,"
           "type: $medium_type"
           "}) "
           "MERGE (a)-[:POSTED]->(m)",
           src_identifier=src.identifier,
           medium_identifier=medium.identifier,
           medium_caption=medium.caption,
           medium_type=medium.type
           )


def add_comment(tx, comment):
    src = comment.owner
    tx.run("MATCH (m:Medium {identifier: $medium_identifier})"
           "MERGE (a:Account {"
           "name: $src_username, "
           "identifier: $src_identifier,"
           "is_private: $src_is_private,"
           "is_verified: $src_is_verified,"
           "is_joined_recently: $src_is_joined_recently"
           "}) "
           "MERGE (c:Comment {"
           "identifier: $comment_identifier,"
           "text: $comment_text"
           "})"
           "MERGE (a)-[:COMMENTED]->(c)"
           "MERGE (c)-[:COMMENTED_ON_MEDIA]->(m)",
           comment_text=comment.text,
           medium_identifier=comment.medium_identifier,
           comment_identifier=comment.identifier,
           src_username=src.username,
           src_identifier=src.identifier,
           src_is_private=src.is_private,
           src_is_verified=src.is_verified,
           src_is_joined_recently=src.is_joined_recently
           )
    print("Added comment", comment.identifier, "by", src.username, "on medium", comment.medium_identifier)


def add_following(tx, src, dst):
    tx.run("MERGE (a:Account {"
           "name: $src_username, "
           "identifier: $src_identifier,"
           "is_private: $src_is_private,"
           "is_verified: $src_is_verified,"
           "is_joined_recently: $src_is_joined_recently"
           "}) "
           "MERGE (b:Account {"
           "name: $dst_username, "
           "identifier: $dst_identifier,"
           "is_private: $dst_is_private,"
           "is_verified: $dst_is_verified,"
           "is_joined_recently: $dst_is_joined_recently"
           "}) "
           "MERGE (a)-[:FOLLOWS]->(b)",
           src_username=src.username,
           src_identifier=src.identifier,
           src_is_private=src.is_private,
           src_is_verified=src.is_verified,
           src_is_joined_recently=src.is_joined_recently,
           dst_username=dst.username,
           dst_identifier=dst.identifier,
           dst_is_private=dst.is_private,
           dst_is_verified=dst.is_verified,
           dst_is_joined_recently=dst.is_joined_recently)

def delete_everything(tx):
    tx.run("MATCH (n)"
           "DETACH DELETE n")

def populate_db_following(session):
    filename = 'iubloomington' + '_account.pkl'
    if os.path.exists(filename):
        f = open(filename, 'rb')
        src = pickle.load(f)
    else:
        username = os.environ.get('IG_USERNAME')
        password = os.environ.get('IG_PASSWORD')
        instagram.with_credentials(username, password)
        instagram.login()
        src = instagram.get_account('iubloomington')
        f = open(filename, 'wb')
        pickle.dump(src, f)

    following = get_following('iubloomington')
    for d, dst in enumerate(following['accounts']):
        filename = dst.username + '_following.pkl'
        if os.path.exists(filename):
            # session.write_transaction(add_following, src, dst)
            f = open(filename, 'rb')
            dst_following = pickle.load(f)
            for dd, dst_dst in enumerate(dst_following['accounts']):
                session.write_transaction(add_following, dst, dst_dst)

def populate_db_media(session):
    filename = 'iubloomington' + '_media.pkl'
    f = open(filename, 'rb')
    iub_media = pickle.load(f)
    filename = 'iubloomington' + '_account.pkl'
    f = open(filename, 'rb')
    src = pickle.load(f)
    for m, medium in enumerate(iub_media):
        session.write_transaction(add_medium, src, medium)

def populate_db_comments(session):
    filename = 'iubloomington' + '_comments.pkl'
    f = open(filename, 'rb')
    iub_comments = pickle.load(f)
    for c,comment in enumerate(iub_comments):
        session.write_transaction(add_comment, comment)


def reset_db(session):
    session.write_transaction(delete_everything)

if __name__ == "__main__":
    driver = GraphDatabase.driver("bolt://127.0.0.1:7687/Graph/data", auth=("neo4j", "password"), encrypted = False)
    with driver.session() as session:
        # Use below to clear db programatically
        # reset_db(session)
        print("Populating following.")
        populate_db_following(session)
        print("Populating following complete.")
        print("Populating media.")
        populate_db_media(session)
        print("Populating media complete.")
        print("Populating comments.")
        populate_db_comments(session)
        print("Populating comments complete.")

    driver.close()


