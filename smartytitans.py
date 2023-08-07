import requests
from datetime import datetime, timezone, timedelta
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

# add chest items
items_info["chest_forest"] = {'uid': "chest_forest", "type": "chest", "tier": 1}
items_info["chest_grotto"] = {"uid": "chest_grotto", "type": "chest", "tier": 2}
items_info["chest_swamp"] = {"uid": "chest_swamp", "type": "chest", "tier": 3}
items_info["chest_desert"] = {"uid": "chest_desert", "type": "chest", "tier": 4}
items_info["chest_pyramid"] = {"uid": "chest_pyramid", "type": "chest", "tier": 5}
items_info["chest_ruins"] = {"uid": "chest_ruins", "type": "chest", "tier": 6}
items_info["chest_castle"] = {"uid": "chest_castle", "type": "chest", "tier": 7}
items_info["chest_temple"] = {"uid": "chest_temple", "type": "chest", "tier": 8}
items_info["chest_peak"] = {"uid": "chest_peak", "type": "chest", "tier": 9}
items_info["chest_volcano"] = {"uid": "chest_volcano", "type": "chest", "tier": 10}
items_info["chest_rift"] = {"uid": "chest_rift", "type": "chest", "tier": 11}
items_info["chest_goldcity"] = {"uid": "chest_goldcity", "type": "chest", "tier": 7}
items_info["chest_goldcity2"] = {"uid": "chest_goldcity2", "type": "chest", "tier": 10}
items_info["chest_goldcity3"] = {"uid": "chest_goldcity3", "type": "chest", "tier": 11}

# get chinese name for each item
for (item_name, item_data) in items_info.items():
    # chinese_name
    chinese_name = translation["texts"][item_name + "_name"]
    item_data["chinese_name"] = chinese_name

    # chinese_type
    chinese_type = translation_type[item_data["type"]]
    chinese_type = translation["texts"][chinese_type]
    item_data["chinese_type"] = chinese_type

    # print(chinese_type, chinese_name, item_data)


def print_trade(x, Type):
    Type = Type.split("_")

    if x["quality"] == None:
        chinese_quality = translation["texts"]["common_name"]
    else:
        chinese_quality = translation["texts"][x["quality"]+"_name"]

    print(x["type"], ", ",
          x["tier"], ", ",
          chinese_quality, ", ",
          x["name"], ": ",
          "offer_" + Type[0] + ": ", x["offer"], ", ",
          "request_" + Type[1] + ": ", x["request"], ", ",
          "rate: ", x["rate"], " (",
          x["offer_t"].seconds//60, ",",
          x["request_t"].seconds//60, " mins ago)",
          sep="")


quality_to_int = {None: 0,
                  "uncommon": 1,
                  "flawless": 2,
                  "epic": 3,
                  "legendary": 4}


def get_item_value(item_info, quality):
    quality_index = quality_to_int[quality]
    item_max_value = item_info["tradeMinMaxValue"].split(";")
    item_max_value = item_max_value[1].split(",")
    item_max_value = int(item_max_value[quality_index])
    item_value = int(item_max_value/10)
    return item_value


# request items for energy
request_for_energy = []
for (item_name, item_data) in items_info.items():
    if item_data["tier"] != 10:
        continue
    # if item_data["excl"] != None:
    #     continue
    if item_data["type"] == "xu":
        continue
    if item_data["type"] == "xm":
        continue
    if item_data["type"] == "z":
        continue
    if item_data["type"] == "m":
        continue
    if item_data["type"] == "chest":
        continue

    chinese_name = item_data["chinese_name"]
    chinese_type = item_data["chinese_type"]
    # print(chinese_type, chinese_name, item_data)
    request_for_energy.append(item_data["uid"])

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

    energy_per_sale = 40
    energy_to_gold_rates = []
    gold_to_energy_rates = []
    for (key, data) in offer_request.items():
        (uid, quality) = key

        # get item info
        item_info = items_info[uid]
        item_name = item_info["chinese_name"]
        item_tier = item_info["tier"]
        item_type = item_info["chinese_type"]
        # print(item_type, item_tier, quality, item_name)

        # gold-to-energy rate
        if uid in items_info and \
                item_info["type"] != "xu" and \
                item_info["type"] != "xm" and \
                item_info["type"] != "z" and \
                item_info["type"] != "m" and \
                item_info["type"] != "chest":
            # get item value
            item_value = get_item_value(item_info, quality)

            # gold to energy rate
            if "offer" in data and data["offer"]["goldPrice"] != None and item_tier >= 8:
                offer_gold = data["offer"]["goldPrice"] - int(item_value/2)
                request_energy = item_info["discount"] + energy_per_sale
                gold_to_energy_rate = int(offer_gold/request_energy)
                gold_to_energy_rates.append({"type": item_type,
                                            "tier": item_tier,
                                             "quality": quality,
                                             "name": item_name,
                                             "offer": data["offer"]["goldPrice"],
                                             "request": request_energy,
                                             "rate": gold_to_energy_rate,
                                             "offer_t": datetime.now(timezone.utc) - parser.parse(data["offer"]["updatedAt"]),
                                             "request_t": timedelta(seconds=0)
                                             })

            # energy to gold rate
            if "offer" in data and data["offer"]["goldPrice"] != None:
                offer_energy = item_info["surcharge"] - energy_per_sale
                request_gold = item_value*2 - data["offer"]["goldPrice"]
                if offer_energy > 0 and request_gold > 0:
                    energy_to_gold_rate = int(request_gold/offer_energy)
                    energy_to_gold_rates.append({"type": item_type,
                                                "tier": item_tier,
                                                 "quality": quality,
                                                 "name": item_name,
                                                 "offer": offer_energy,
                                                 "request": data["offer"]["goldPrice"],
                                                 "rate": energy_to_gold_rate,
                                                 "offer_t": timedelta(seconds=0),
                                                 "request_t": datetime.now(timezone.utc) - parser.parse(data["offer"]["updatedAt"])
                                                 })

        if "offer" not in data or "request" not in data:
            continue

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

    gold_to_energy_rates.sort(key=lambda x: x["rate"])
    energy_to_gold_rates.sort(key=lambda x: x["rate"], reverse=True)

    print("gold_to_energy_rates:")
    for i in range(len(gold_to_energy_rates)):
        if gold_to_energy_rates[i]["rate"] < energy_to_gold_rates[0]["rate"]:
            x = gold_to_energy_rates[i]
            # print(gold_to_energy_rates[i])
            print_trade(x, "gold_energy")
            if i >= 5:
                break

    print("energy_to_gold_rates:")
    for i in range(len(energy_to_gold_rates)):
        if energy_to_gold_rates[i]["rate"] > gold_to_energy_rates[0]["rate"]:
            x = energy_to_gold_rates[i]
            # print(energy_to_gold_rates[i])
            print_trade(x, "energy_glod")
        if i >= 5:
            break
    print()

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
    print()

    # request item for energy
    for uid in request_for_energy:
        item_info = items_info[uid]
        item_type = item_info["chinese_type"]
        item_tier = item_info["tier"]
        item_name = item_info["chinese_name"]
        item_value = get_item_value(item_info, None)

        if (uid, None) in offer_request:
            data = offer_request[(uid, None)]
            if "request" in data and data["request"]["goldPrice"] != None:
                if data["request"]["goldPrice"] < int(item_value/2):
                    print(item_type, item_tier, item_name, data["request"]["goldPrice"], "<", int(item_value/2))
        else:
            print(item_type, item_tier, item_name)
    print()

    # sleep
    time.sleep(10)
