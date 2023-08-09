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

# player info
energy_per_sale = 40
surcharge_tier = 12


def print_trade(x, key1, key2):
    print(x["type"], ", ",
          x["tier"], ", ",
          x["quality"], ", ",
          x["name"], ": ",
          key1 + ": ", x[key1], ", ",
          key2 + ": ", x[key2], ", ",
          "rate: ", x["rate"], " (",
          x[key1 + "_t"].seconds//60, ",",
          x[key2 + "_t"].seconds//60, " mins ago)",
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


def offer_energy_rate(x, y):
    return (y["currency_change"]*x["energy_change"] - x["currency_change"]*y["energy_change"])/(x["energy_change"] - y["energy_change"])


def compare_gold_energy(x, y, gold_change, energy_change):
    if x[gold_change] > y[gold_change] and x[energy_change] > y[energy_change] or \
       x[gold_change] > y[gold_change] and x[energy_change] == y[energy_change] or \
       x[gold_change] == y[gold_change] and x[energy_change] > y[energy_change]:
        return 1
    elif x[gold_change] < y[gold_change] and x[energy_change] < y[energy_change] or \
            x[gold_change] < y[gold_change] and x[energy_change] == y[energy_change] or \
            x[gold_change] == y[gold_change] and x[energy_change] < y[energy_change]:
        return -1
    else:
        return 0


def insert(List, y):
    for x in List:
        if compare_gold_energy(x, y, "currency_change", "energy_change") > 0:
            return False
    return True


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

        # set chinese_quality
        if item_last["tag1"] == None:
            offer_request[key]["chinese_quality"] = translation["texts"]["common_name"]
        else:
            offer_request[key]["chinese_quality"] = translation["texts"][item_last["tag1"] + "_name"]

        # grouping
        if item_last["tType"] == "o" or item_last["tType"] == "os":
            offer_request[key]["offer"] = item_last
        elif item_last["tType"] == "r" or item_last["tType"] == "rs":
            offer_request[key]["request"] = item_last

    # find gem_to_gold_rates
    gem_to_gold_rates = []
    gold_to_gem_rates = []

    offer_energy_list = []
    gold_to_gem_rate_estimated = 4000000
    for (key, data) in offer_request.items():
        (uid, quality) = key

        # get item info
        if uid not in items_info:
            # print("uid \"", uid, "\" is not found in the file \"items.json\".", sep="")
            continue

        item_info = items_info[uid]
        item_type = item_info["chinese_type"]
        item_tier = item_info["tier"]
        chinese_quality = data["chinese_quality"]
        item_name = item_info["chinese_name"]
        # print(item_type, item_tier, chinese_quality, item_name)

        # offer-energy pair
        if item_info["type"] != "xu" and \
           item_info["type"] != "xm" and \
           item_info["type"] != "z" and \
           item_info["type"] != "m" and \
           item_info["type"] != "chest":
            # get item value
            item_value = get_item_value(item_info, quality)

            # offer-energy pair
            if "offer" in data:
                # calculate offer and offer_value
                if data["offer"]["gemsPrice"] == None:
                    # only gold offer
                    offer = data["offer"]["goldPrice"]
                    offer_value = data["offer"]["goldPrice"]
                elif data["offer"]["goldPrice"] == None:
                    # only gems offer
                    offer = data["offer"]["gemsPrice"]
                    offer_value = data["offer"]["gemsPrice"] * gold_to_gem_rate_estimated
                else:
                    # both gold and gems offer
                    offer_gems_value = data["offer"]["gemsPrice"] * gold_to_gem_rate_estimated
                    if data["offer"]["goldPrice"] <= offer_gems_value:
                        offer = data["offer"]["goldPrice"]
                        offer_value = data["offer"]["goldPrice"]
                    else:
                        offer = data["offer"]["gemsPrice"]
                        offer_value = offer_gems_value

                # discount
                currency_change = int(item_value/2) - offer_value
                energy_change = item_info["discount"] + energy_per_sale
                offer_energy_list.append({"selling_type": "discount",
                                          "type": item_type,
                                          "tier": item_tier,
                                          "quality": chinese_quality,
                                          "name": item_name,
                                          "currency_change": currency_change,
                                          "energy_change": energy_change,
                                          "offer": offer,
                                          "offer_t": datetime.now(timezone.utc) - parser.parse(data["offer"]["updatedAt"]),
                                          })

                # surcharge
                if item_tier <= surcharge_tier:
                    currency_change = item_value*2 - offer_value
                    energy_change = -item_info["surcharge"] + energy_per_sale
                    offer_energy_list.append({"selling_type": "surcharge",
                                              "type": item_type,
                                              "tier": item_tier,
                                              "quality": chinese_quality,
                                              "name": item_name,
                                              "currency_change": currency_change,
                                              "energy_change": energy_change,
                                              "offer": offer,
                                              "offer_t": datetime.now(timezone.utc) - parser.parse(data["offer"]["updatedAt"]),
                                              })

        if "offer" not in data or "request" not in data:
            continue

        # offer_gold < request_gold
        if data["offer"]["goldPrice"] != None and data["request"]["goldPrice"] != None:
            if data["offer"]["goldPrice"] < data["request"]["goldPrice"]:
                # print("offer_gold < request_gold:", item_name, chinese_quality, data)
                pass

        # offer_gems < request_gems
        if data["offer"]["gemsPrice"] != None and data["request"]["gemsPrice"] != None:
            if data["offer"]["gemsPrice"] < data["request"]["gemsPrice"]:
                # print("offer_gems < request_gems:", item_name, chinese_quality, data)
                pass

        # gold to gem rate
        if data["offer"]["goldPrice"] != None and data["request"]["gemsPrice"] != None:
            gold_to_gem_rate = int(data["offer"]["goldPrice"]/data["request"]["gemsPrice"])
            gold_to_gem_rates.append({"type": item_type,
                                      "tier": item_tier,
                                      "quality": chinese_quality,
                                      "name": item_name,
                                      "offer_gold": data["offer"]["goldPrice"],
                                      "request_gems": data["request"]["gemsPrice"],
                                      "rate": gold_to_gem_rate,
                                      "offer_gold_t": datetime.now(timezone.utc) - parser.parse(data["offer"]["updatedAt"]),
                                      "request_gems_t": datetime.now(timezone.utc) - parser.parse(data["request"]["updatedAt"])
                                      })

        # gem to gold rate
        if data["offer"]["gemsPrice"] != None and data["request"]["goldPrice"] != None:
            gem_to_gold_rate = int(data["request"]["goldPrice"]/data["offer"]["gemsPrice"])
            gem_to_gold_rates.append({"type": item_type,
                                      "tier": item_tier,
                                      "quality": chinese_quality,
                                      "name": item_name,
                                      "offer_gems": data["offer"]["gemsPrice"],
                                      "request_gold": data["request"]["goldPrice"],
                                      "rate": gem_to_gold_rate,
                                      "offer_gems_t": datetime.now(timezone.utc) - parser.parse(data["offer"]["updatedAt"]),
                                      "request_gold_t": datetime.now(timezone.utc) - parser.parse(data["request"]["updatedAt"])
                                      })

    # offer-energy pair
    # divide offer_energy_list into two lists
    energy_loss_list = []
    energy_gain_list = []
    energy_loss_boundary = []
    energy_gain_boundary = []
    for x in offer_energy_list:
        # energy_gain
        if x["energy_change"] > 0:
            x["energy_change_t"] = timedelta(seconds=0)
            x["energy_rate"] = int(-x["currency_change"]/x["energy_change"])
            energy_gain_list.append(x)

            if insert(energy_gain_boundary, x):
                energy_gain_boundary.append(x)

        # energy_loss
        if x["energy_change"] < 0 and x["currency_change"] > 0:
            x["energy_change_t"] = timedelta(seconds=0)
            x["energy_rate"] = int(-x["currency_change"]/x["energy_change"])
            energy_loss_list.append(x)

            if insert(energy_loss_boundary, x):
                energy_loss_boundary.append(x)

    offer_energy_pair = []
    for energy_gain in energy_gain_boundary:
        for energy_loss in energy_loss_boundary:
            rate = offer_energy_rate(energy_gain, energy_loss)
            offer_energy_pair.append({"energy_gain": energy_gain,
                                      "energy_loss": energy_loss,
                                      "rate": rate,
                                      })
    offer_energy_pair.sort(key=lambda x: x["rate"], reverse=True)

    print("offer-to-energy:")
    offer_to_energy_rate = offer_energy_pair[0]["energy_gain"]["energy_rate"]
    energy_to_offer_rate = offer_energy_pair[0]["energy_loss"]["energy_rate"]
    print("offer_to_energy_rate:", offer_to_energy_rate)
    print("energy_to_offer_rate:", energy_to_offer_rate)
    for i in range(len(offer_energy_pair)):
        if i >= 1:
            break

        x = offer_energy_pair[i]
        print("rate: ", int(x["rate"]), ": ",
              x["energy_gain"]["type"], ", ",
              x["energy_gain"]["tier"], ", ",
              x["energy_gain"]["quality"], ", ",
              x["energy_gain"]["name"], ", ",
              x["energy_gain"]["offer"], ", ",
              x["energy_gain"]["energy_rate"], "; ",

              x["energy_loss"]["type"], ", ",
              x["energy_loss"]["tier"], ", ",
              x["energy_loss"]["quality"], ", ",
              x["energy_loss"]["name"], ", ",
              x["energy_loss"]["offer"], ", ",
              x["energy_loss"]["energy_rate"], " (",

              x["energy_gain"]["offer_t"].seconds//60, ",",
              x["energy_loss"]["offer_t"].seconds//60, " mins ago)",
              sep="")

    print("offer_to_energy:")
    for energy_gain in energy_gain_list:
        energy_gain["rate"] = int(offer_energy_rate(energy_gain, offer_energy_pair[0]["energy_loss"]))
    energy_gain_list.sort(key=lambda x: x["rate"], reverse=True)

    for i in range(len(energy_gain_list)):
        x = energy_gain_list[i]
        print_trade(x, "offer", "energy_change")
        if i >= 5:
            break

    print("energy_to_offer:")
    for energy_loss in energy_loss_list:
        energy_loss["rate"] = int(offer_energy_rate(offer_energy_pair[0]["energy_gain"], energy_loss))
    energy_loss_list.sort(key=lambda x: x["rate"], reverse=True)

    for i in range(len(energy_loss_list)):
        x = energy_loss_list[i]
        print_trade(x, "offer", "energy_change")
        if i >= 10:
            break
    print()

    # gold-to-gem rates
    gold_to_gem_rates.sort(key=lambda x: x["rate"])
    gem_to_gold_rates.sort(key=lambda x: x["rate"], reverse=True)

    if gem_to_gold_rates[0]["rate"] < gold_to_gem_rates[0]["rate"]:
        print("No gem_to_gold is found.")
        print_trade(gem_to_gold_rates[0], "offer_gems", "request_gold")
        print_trade(gold_to_gem_rates[0], "offer_gold", "request_gems")
    else:
        print("gold_to_gem_rates:")
        for i in range(len(gold_to_gem_rates)):
            if gold_to_gem_rates[i]["rate"] < gem_to_gold_rates[0]["rate"]:
                x = gold_to_gem_rates[i]
                # print(gold_to_gem_rates[i])
                print_trade(x, "offer_gold", "request_gems")
            if i >= 5:
                break

        print("gem_to_gold_rates:")
        for i in range(len(gem_to_gold_rates)):
            if gem_to_gold_rates[i]["rate"] > gold_to_gem_rates[0]["rate"]:
                x = gem_to_gold_rates[i]
                # print(gem_to_gold_rates[i])
                print_trade(x, "offer_gems", "request_gold")
            if i >= 5:
                break
    print()

    # request item for energy
    print("request items for energy:")
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
