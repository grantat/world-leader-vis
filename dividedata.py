import json
import os
from datetime import datetime
import csv
import time


def save_json(new_json, filename):
    """ Helper to save json files in /chunks/ """
    with open("data/chunks/" + filename, 'w') as out:
        json.dump(new_json, out, sort_keys=True)


def match_json():
    """ Find JSON pairs from original json """
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
                    profile_pic = ""
                    for tweet in tweets:
                        if tweet["id"] == int(tweet_id):
                            profile_pic = tweet["user"][
                                "profile_image_url_https"]
                            break
                    created_at = datetime.strptime(
                        tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
                    formatted_time = created_at.strftime("%Y-%m-%dT%H:%M:%S")
                    timestamp = time.mktime(created_at.timetuple())
                    new_json.setdefault(int(timestamp), [])
                    new_json[int(timestamp)].append(
                        {"username": username,
                         "profile_pic": profile_pic,
                         "created_at": formatted_time,
                         "text": sentiment_dict[tweet_id]["text"],
                         "sentiment": sentiment_dict[tweet_id]["sentiment"]})
    # print(json.dumps(new_json, sort_keys=True, indent=4))
    save_json(new_json, "merged_data.json")


def before_oct_3(date):
    """ Helper check date before oct_3 """
    if date < "2017-10-03":
        return True
    return False


def print_dates():
    """
    Merged together tweets tweeted at the exact same time and add them
    to a dictionary based on month
    """
    with open("data/chunks/merged_data.json") as f:
        merged_data = json.load(f)
        total = 0
        merge_on_month = {}
        for timestamp in merged_data:
            total += len(merged_data[timestamp])
            new_date = datetime.fromtimestamp(int(timestamp)).strftime(
                '%Y-%m')
            merge_on_month.setdefault(new_date, [])
            for tweet in merged_data[timestamp]:
                merge_on_month[new_date].append(tweet)

            # print(
            #     datetime.fromtimestamp(int(timestamp)).strftime(
            #         '%Y-%m-%dT%H:%M:%S'), len(merged_data[timestamp])
            # )

        month_chunks(merge_on_month)


def month_chunks(merge_on_month):
    """
    This function splits tweets groups tweets based on the month they
    were created.
    Save chunks to json files in /chunks/
    """
    for month in sorted(merge_on_month):
        # months = {}
        if not before_oct_3(month):
            continue

        # print(merge_on_month[month])
        file_str = "data/chunks/{}.json".format(
            month)

        with open(file_str, 'w') as out:
            json.dump(merge_on_month[month], out)


def build_heatmap_data():
    """ Build appropriate data format for a heatmap into a csv """
    for filename in os.listdir("data/chunks/"):
        if not filename.startswith("m") and filename.endswith(".json"):

            month = filename[:-5]

            with open("data/chunks/" + filename) as f, \
                    open("data/heatmap/{}.csv".format(month), 'w') as out:
                writer = csv.writer(out)
                writer.writerow(["day", "hour", "value"])
                data = json.load(f)
                map_vals = {}
                for tweet in data:
                    temp_date = datetime.strptime(
                        tweet["created_at"], "%Y-%m-%dT%H:%M:%S")
                    map_vals.setdefault(temp_date.isoweekday(), {})
                    map_vals[temp_date.isoweekday()].setdefault(
                        temp_date.hour, 0)
                    map_vals[temp_date.isoweekday()][temp_date.hour] += 1
                    # print(temp_date.isoweekday(), temp_date.hour)
                print(json.dumps(map_vals, indent=4))
                print(filename)
                for weekday in map_vals:
                    for hour in map_vals[weekday]:
                        writer.writerow(
                            [weekday, hour, map_vals[weekday][hour]])


def date_range_sets(merge_on_day):
    """
    ******DEPRECATED******
    Write files of for ranges of data.
    This function splits tweets into date ranges that have atleast 100
    tweets or are the remaining tweets left in the list.
    """
    temp = []
    total = 165553
    lowerbound = ""
    upperbound = ""
    for day in sorted(merge_on_day):
        if not before_oct_3(day):
            continue

        # merge based on number of entries
        lowerbound = day
        temp += merge_on_day[day]
        temp_count = len(temp)
        if len(upperbound) == 0:
            upperbound = day
        if temp_count > 100 or (total - temp_count) == 0:
            total -= temp_count
            file_str = "data/chunks/{}to{}.json".format(
                upperbound, lowerbound)

            if upperbound == lowerbound:
                file_str = "data/chunks/{}.json".format(upperbound)

            with open(file_str, 'w') as out:
                json.dump(temp, out)
            # reset lower and upperbounds
            upperbound = ""
            lowerbound = ""
            temp = []


def barchart_metrics():
    """
    Divide data by year, then chunk?
    """
    with open("data/date-ranges.json", 'w') as out:
        date_ranges = {}
        for filename in os.listdir("data/chunks/"):
            if not filename.startswith("m") and not filename.startswith("DS"):
                with open("data/chunks/" + filename) as f:
                    print(filename)
                    year = ""
                    date = filename.split(".")[0]
                    year = datetime.strptime(
                        date, "%Y-%m").year

                    date_ranges.setdefault(year, [])
                    chunk = json.load(f)
                    temp = {}

                    chunk_size = len(chunk)
                    chunk_title = filename.replace("to", " - ")
                    temp["count"] = chunk_size
                    temp["title"] = chunk_title[:-5]
                    temp["filename"] = filename
                    date_ranges[year].append(temp)
        json.dump(date_ranges, out)


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
    match_json()
    print_dates()
    # barchart_metrics()
    # build_heatmap_data()
