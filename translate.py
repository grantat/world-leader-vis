import csv
import os
import ast
import json
import time
from googletrans import Translator
import google.cloud as cloud


def translate_csvs():
    """
    Using googletrans library. Hits rate limit or captcha
    after 20 requests in a row.
    """
    for filename in os.listdir("data/"):
        username = filename[:-4]
        if os.path.isfile("data/translations/" + username + ".json"):
            continue

        if filename.endswith(".csv"):
            with open("data/" + filename, 'r') as f:
                print("File:", filename)
                reader = csv.reader(f)
                next(reader)

                data = []
                for row in reader:
                    temp = {}
                    temp["id"] = row[0]
                    temp["datetime"] = row[1]
                    bytes_string = ast.literal_eval(row[2])
                    sentence = bytes_string.decode('utf-8').rstrip()
                    temp["orig"] = sentence
                    # sleep for 1 seconds between requests
                    time.sleep(1)

                    # keep running until it finally translates
                    translated_flag = True
                    translation = ""
                    while(translated_flag):
                        try:
                            translation = translate(sentence)
                            translated_flag = False
                        except json.decoder.JSONDecodeError:
                            print("Hit rate limit. Sleeping for 2 minutes")
                            time.sleep(60 * 2)

                    print(translation)
                    temp["translation"] = translation.text
                    data.append(temp)
                dump_data_if_not_exists(
                    "data/translations/", username + ".json", data)
                # stop after each file
                exit()
        else:
            continue


def translate(sentence):
    """
    googletrans autodetect language option.
    Process one at a time to avoid limit rates/captchas
    """
    translator = Translator()
    translation = translator.translate(sentence, dest='en')
    # translations = translator.translate(sentence_list, dest='en')
    return translation


def makedir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def dump_data_if_not_exists(directory, filename, data):
    """
    Save translated Json with original text, translation, language
    """
    if not os.path.isfile(directory + filename):
        with open(directory + filename, 'w') as out:
            json.dump(data, out)


def find_overall_lang():
    for filename in os.listdir("data/backup_json/"):
        print(filename)
        # username = filename[:-5]
        lang_counts = {}
        if filename.endswith(".json"):
            with open("data/backup_json/" + filename, 'r') as f:
                tweet_list = json.load(f)
                for i in tweet_list:
                    lang = i["lang"]
                    lang_counts.setdefault(lang, 0)
                    lang_counts[lang] += 1
                    if lang == "und":
                        print(i["text"])
        print(lang_counts)
        # exit()


def build_html():
    for filename in os.listdir("data/backup_json/"):
        print(filename)
        username = filename[:-5]
        if filename.endswith(".json"):
            with open("data/backup_json/" + filename, 'r') as f, \
                    open("data/html/" + username + ".html", 'w') as out:
                tweet_list = json.load(f)
                html = ("<head><meta http-equiv='Content-Type' "
                        "content='text/html; charset=UTF-8'/></head>")
                for i in tweet_list:
                    html += "<div class='tweets-text' id='{}'>{}</div>".format(
                        i["id"], i["text"])
                out.write(html)


if __name__ == "__main__":
    directory = "data/translations/"
    makedir_if_not_exists(directory)
    # find_overall_lang()
    # build_html()
    # translate_csvs()
