import requests
from datetime import datetime
from datetime import timezone
from dateutil import parser

import time

# get chinese translation
response_zh = requests.get("https://smartytitans.com/assets/gameData/texts_zh_tr.json")
print(response_zh.status_code)
translation = response_zh.json()

# dictionary for type
translation_type = {"ws": "item_type_sword",
                    "wa": "item_type_axe",
                    "wd": "item_type_dagger",
                    "wm": "item_type_mace",
                    "wp": "item_type_spear",
                    "wb": "item_type_bow",
                    "wt": "item_type_staff",
                    "ww": "item_type_wand",
                    "wc": "item_type_crossbow",
                    "wg": "item_type_gun",

                    "ah": "item_type_armorheavy",
                    "am": "item_type_armormedium",
                    "al": "item_type_armorlight",
                    "hh": "item_type_helmet",
                    "hm": "item_type_roguehat",
                    "hl": "item_type_hat",
                    "gh": "item_type_gauntlets",
                    "gl": "item_type_bracers",
                    "bh": "item_type_boots",
                    "bl": "item_type_shoes",

                    "uh": "item_type_herb",
                    "up": "item_type_potion",
                    "us": "item_type_scrolls",
                    "xs": "item_type_shield",
                    "xr": "item_type_ring",
                    "xa": "item_type_amulet",
                    "xc": "item_type_cloak",
                    "xf": "item_type_familiar",
                    "fm": "item_type_meal",
                    "fd": "item_type_dessert",

                    "xu": "item_type_stone",
                    "xm": "item_type_moonstone",
                    "z": "item_type_tag",
                    "m": "component",

                    "chest": "special_item_type_chest"}

# get all item info
response_items = requests.get("https://smartytitans.com/assets/gameData/items.json")
print(response_items.status_code)
items_info = response_items.json()

# get chinese name for each item
for (item_name, item_data) in items_info.items():
    if item_name + "_name" in translation["texts"]:
        chinese_name = translation["texts"][item_name + "_name"]
        # print(item_name, item_data)

        if item_data["type"] in translation_type:
            chinese_type = translation_type[item_data["type"]]
            chinese_type = translation["texts"][chinese_type]
        else:
            chinese_type = None

        if item_name != item_data["uid"]:
            print("Error")

        item_data["chinese"] = chinese_name
    else:
        print("Error: Cannot find Chinese name for", item_name)


def print_trade(x, Type):
    Type = Type.split("_")
    print(x["type"], ", ",
          x["tier"], ", ",
          x["quality"], ", ",
          x["name"], ": ",
          "offer_" + Type[0] + ": ", x["offer"], ", ",
          "request_" + Type[1] + ": ", x["request"], ", ",
          "rate: ", x["rate"], " (",
          x["offer_t"].seconds//60, ",",
          x["request_t"].seconds//60, " mins ago)",
          sep="")


while True:
    # get all market data
    response_last = requests.get("https://smartytitans.com/api/item/last/all")
    print("status code:", response_last.status_code)
    items_last = response_last.json()

    # group market data by item
    offer_request = {}
    for item_last in items_last["data"]:
        key = (item_last["uid"], item_last["tag1"])
        if key not in offer_request:
            offer_request[key] = {}

        # set price to None, if Qty is 0
        if item_last['goldQty'] == 0:
            item_last['goldPrice'] = None
        if item_last['gemsQty'] == 0:
            item_last['gemsPrice'] = None

        # grouping
        if item_last["tType"] == "o" or item_last["tType"] == "os":
            offer_request[key]["offer"] = item_last
        elif item_last["tType"] == "r" or item_last["tType"] == "rs":
            offer_request[key]["request"] = item_last

    # find gem_to_gold_rates
    gem_to_gold_rates = []
    gold_to_gem_rates = []
    for (key, data) in offer_request.items():
        if "offer" not in data or "request" not in data:
            continue

        (uid, quality) = key

        # get chinese name
        if uid in items_info:
            item_info = items_info[uid]
            item_name = item_info["chinese"]
            item_tier = item_info["tier"]
            item_type = translation_type[item_info["type"]]

        else:
            item_name = uid
            item_tier = None
            item_type = translation_type["chest"]

        item_type = translation["texts"][item_type]

        # print(item_name, quality, data)
        # offer_gold < request_gold
        if data["offer"]["goldPrice"] != None and data["request"]["goldPrice"] != None:
            if data["offer"]["goldPrice"] < data["request"]["goldPrice"]:
                # print("offer_gold < request_gold:", item_name, quality, data)
                pass

        # offer_gems < request_gems
        if data["offer"]["gemsPrice"] != None and data["request"]["gemsPrice"] != None:
            if data["offer"]["gemsPrice"] < data["request"]["gemsPrice"]:
                # print("offer_gems < request_gems:", item_name, quality, data)
                pass

        # gold to gem rate
        if data["offer"]["goldPrice"] != None and data["request"]["gemsPrice"] != None:
            gold_to_gem_rate = int(data["offer"]["goldPrice"]/data["request"]["gemsPrice"])
            gold_to_gem_rates.append({"type": item_type,
                                      "tier": item_tier,
                                      "quality": quality,
                                      "name": item_name,
                                      "offer": data["offer"]["goldPrice"],
                                      "request": data["request"]["gemsPrice"],
                                      "rate": gold_to_gem_rate,
                                      "offer_t": datetime.now(timezone.utc) - parser.parse(data["offer"]["updatedAt"]),
                                      "request_t": datetime.now(timezone.utc) - parser.parse(data["request"]["updatedAt"])
                                      })

        # gem to gold rate
        if data["offer"]["gemsPrice"] != None and data["request"]["goldPrice"] != None:
            gem_to_gold_rate = int(data["request"]["goldPrice"]/data["offer"]["gemsPrice"])
            gem_to_gold_rates.append({"type": item_type,
                                      "tier": item_tier,
                                      "quality": quality,
                                      "name": item_name,
                                      "offer": data["offer"]["gemsPrice"],
                                      "request": data["request"]["goldPrice"],
                                      "rate": gem_to_gold_rate,
                                      "offer_t": datetime.now(timezone.utc) - parser.parse(data["offer"]["updatedAt"]),
                                      "request_t": datetime.now(timezone.utc) - parser.parse(data["request"]["updatedAt"])
                                      })

    gold_to_gem_rates.sort(key=lambda x: x["rate"])
    gem_to_gold_rates.sort(key=lambda x: x["rate"], reverse=True)

    if gem_to_gold_rates[0]["rate"] < gold_to_gem_rates[0]["rate"]:
        print("No gem_to_gold is found.")
        print_trade(gem_to_gold_rates[0], "gem_glod")
        print_trade(gold_to_gem_rates[0], "gold_gem")
    else:
        print("gold_to_gem_rates:")
        for i in range(len(gold_to_gem_rates)):
            if gold_to_gem_rates[i]["rate"] < gem_to_gold_rates[0]["rate"]:
                x = gold_to_gem_rates[i]
                # print(gold_to_gem_rates[i])
                print_trade(x, "gold_gem")
            if i >= 5:
                break

        print("gem_to_gold_rates:")
        for i in range(len(gem_to_gold_rates)):
            if gem_to_gold_rates[i]["rate"] > gold_to_gem_rates[0]["rate"]:
                x = gem_to_gold_rates[i]
                # print(gem_to_gold_rates[i])
                print_trade(x, "gem_glod")
            if i >= 5:
                break

    # sleep
    print()
    time.sleep(10)
