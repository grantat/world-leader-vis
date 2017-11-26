import json
import os
from datetime import datetime
import time


def save_json(new_json, filename):
    with open("data/chunks/" + filename, 'w') as out:
        json.dump(new_json, out, sort_keys=True)


def match_json():
    new_json = {}
    for filename in os.listdir("data/sentiment/"):
        username = filename[:-11]
        back_json_file = filename[:-5] + "s.json"
        print(filename)
        print(username)
        if filename.endswith(".json"):
            with open("data/sentiment/" + filename) as f, \
                    open("data/backup_json/" + back_json_file) as f2:
                sentiment_dict = json.load(f)
                tweets = json.load(f2)
                # search backup_json for tweet
                for tweet_id, i in sentiment_dict.items():
                    for tweet in tweets:
                        if tweet["id"] == int(tweet_id):
                            break
                    created_at = datetime.strptime(
                        tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
                    formatted_time = created_at.strftime("%Y-%m-%dT%H:%M:%S")
                    timestamp = time.mktime(created_at.timetuple())
                    new_json.setdefault(int(timestamp), [])
                    new_json[int(timestamp)].append(
                        {"username": username,
                         "id": int(tweet_id),
                         "created_at": formatted_time,
                         "text": sentiment_dict[tweet_id]["text"],
                         "sentiment": sentiment_dict[tweet_id]["sentiment"]})
    # print(json.dumps(new_json, sort_keys=True, indent=4))
    save_json(new_json, "merged_data.json")


def print_dates():
    with open("data/chunks/merged_data.json") as f:
        merged_data = json.load(f)
        for timestamp in merged_data:
            print(
                datetime.fromtimestamp(int(timestamp)).strftime(
                    '%Y-%m-%d %H:%M:%S')
            )
        print(len(merged_data))


def print_duplicates(timestamps):
    """
    Unfortunately there are duplicates in almost every users tweet set.
    This prints duplicate entries.
    """
    seen = set()
    not_uniq = []
    for x in timestamps:
        if x in seen:
            not_uniq.append(x)
        else:
            seen.add(x)
    print(not_uniq)


if __name__ == "__main__":
    # match_json()
    print_dates()
