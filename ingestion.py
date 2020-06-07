import os
import requests
from mediastore import MediaStore


class Ingestor():
    work_root = None
    driver = None
    datastore = None

    def __init__(self):
        self.datastore = MediaStore()
        self.work_root = os.path.dirname(os.path.abspath(__file__))

    def get_tag_data_json(self, tag_file=None):
        tag_file_path = os.path.join(self.work_root, 'data/', tag_file)

        with open(tag_file_path, 'r') as input_tags:
            tags = input_tags.readlines()
            for tag in tags:
                tag = tag.strip()
                print(f"INFO: Getting information for tag: {tag}")
                url = f"https://www.instagram.com/explore/tags/{tag}?__a=1"
                data = requests.get(url).json()

                number_of_photos_tagged = 0
                try:
                    number_of_photos_tagged = data["graphql"]["hashtag"][
                        "edge_hashtag_to_media"]["count"]
                except Exception:
                    print(f"WARNING: No tagged number for: {tag}")
                    pass

                print(
                    f"INFO: Number of photos tagged as {tag}: {number_of_photos_tagged}"  # noqa
                )

                tag_popular_posts = [None] * 9
                try:
                    for counter in range(0, 9):
                        code = data["graphql"]["hashtag"][
                            "edge_hashtag_to_top_posts"]["edges"][counter][
                                "node"]["shortcode"]
                        tag_popular_post = f"https://instagram.com/p/{code}"
                        tag_popular_posts[counter] = tag_popular_post
                        print(f"INFO: Popular photo: {tag_popular_post}")
                except Exception:
                    pass

                if all(v is None for v in tag_popular_posts):
                    print(f"WARNING: No popular photos for: {tag}")
                else:
                    try:
                        self.datastore.store_tag_popularity(
                            tag=tag,
                            tag_popular_posts=tag_popular_posts,
                            tag_posts=number_of_photos_tagged)
                    except Exception as e:
                        print(
                            f"ERROR: Couldn't save popular posts for tag: {tag}"
                        )
                        print(f"ERROR: {e.__str__()}")
