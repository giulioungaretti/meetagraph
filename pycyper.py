from py2neo import Graph
import time
import tweepy


class NeoGraph():

    def __init__(self, api):
        self.graph_db = Graph()
        self.api = api
        try:
            self.graph_db.execute("""
                CREATE CONSTRAINT ON (u:User)
                ASSERT u.id_str IS UNIQUE
            """)
        except:
            pass

    def create_or_get_node(self, twitter_user, labels=[]):
        data = {'id_str': twitter_user.id_str,
                'name': twitter_user.name,
                'screen_name': twitter_user.screen_name,
                'description': twitter_user.description,
                'url': twitter_user.url,
                'followers_count': twitter_user.followers_count,
                'friends_count': twitter_user.friends_count,
                'listed_count': twitter_user.listed_count,
                'statuses_count': twitter_user.statuses_count,
                'favourites_count': twitter_user.favourites_count,
                'location': twitter_user.location,
                'time_zone': twitter_user.time_zone,
                'utc_offset': twitter_user.utc_offset,
                'lang': twitter_user.lang,
                'profile_image_url': twitter_user.profile_image_url,
                'geo_enabled': twitter_user.geo_enabled,
                'verified': twitter_user.verified,
                'notifications': twitter_user.notifications,
                }
        query_string = """
            MERGE (u:User {id_str:{id_str}})
            ON CREATE SET
    """ + (('u:' + ',u:'.join(labels) + ",") if labels else '') + """
                u.name={name},
                u.screen_name={screen_name},
                u.description={description},
                u.url={url},
                u.followers_count={followers_count},
                u.friends_count={friends_count},
                u.listed_count={listed_count},
                u.statuses_count={statuses_count},
                u.favourites_count={favourites_count},
                u.location={location},
                u.time_zone={time_zone},
                u.utc_offset={utc_offset},
                u.lang={lang},
                u.profile_image_url={profile_image_url},
                u.geo_enabled={geo_enabled},
                u.verified={verified},
                u.notifications={notifications}
    """ + (("ON MATCH SET\n  u:" + ',u:'.join(labels)) if labels else '') + """
            RETURN u
        """
        self.graph_db.cypher.execute_one(query_string, data)

    def insert_user_with_friends(self, twitter_user, user_labels=[]):
        user_labels.append("SeedNode")
        twitter_user = self.api.get_user(twitter_user)
        self.create_or_get_node(twitter_user, user_labels)
        friends = tweepy.Cursor(
            self.api.friends, user_id=twitter_user.id_str, count=20).items()
        try:
            friend = friends.next()
        except tweepy.TweepError:
            print "exceeded rate limit. waiting"
            time.sleep(60 * 16)
            friend = friends.next()

        self.create_or_get_node(friend)
        self.graph_db.cypher.execute_one("""
            MATCH (user:User {id_str:{user_id_str}}), (friend:User {id_str:{friend_id_str}})
            CREATE UNIQUE (user)-[:FOLLOWS]->(friend)
        """, parameters={"user_id_str": twitter_user.id_str,
                         "friend_id_str": friend.id_str})
