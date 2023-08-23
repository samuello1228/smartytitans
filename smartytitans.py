import requests
from datetime import datetime, timezone, timedelta
from dateutil import parser
import copy

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
items_info["chest_forest"] = {"uid": "chest_forest", "type": "chest", "tier": 1, "tradeMinMaxValue": "200;10000",
                              "items": ["forestroguehat", "forestshoes", "forestdagger", "forestscroll", "forestbow", "forestmace"]}
items_info["chest_grotto"] = {"uid": "chest_grotto", "type": "chest", "tier": 2, "tradeMinMaxValue": "1000;50000",
                              "items": ["grottosword", "grottogloves", "grottoring", "grottoshield", "grottoaxe", "grottoamulet"]}
items_info["chest_swamp"] = {"uid": "chest_swamp", "type": "chest", "tier": 3, "tradeMinMaxValue": "10000;500000",
                             "items": ["swampscroll", "swamphelm", "swampstaff", "swampheavyarmor", "swampboots", "swamphat"]}
items_info["chest_desert"] = {"uid": "chest_desert", "type": "chest", "tier": 4, "tradeMinMaxValue": "20000;1000000",
                              "items": ["desertspear", "desertlightarmor", "desertgauntlets", "desertmediumarmor", "desertbow", "desertgloves"]}
items_info["chest_pyramid"] = {"uid": "chest_pyramid", "type": "chest", "tier": 5, "tradeMinMaxValue": "50000;2500000",
                               "items": ["pyramidmace", "pyramidaxe", "pyramidroguehat", "pyramidheavyarmor", "pyramidpotion", "pyramidring"]}
items_info["chest_ruins"] = {"uid": "chest_ruins", "type": "chest", "tier": 6, "tradeMinMaxValue": "100000;5000000",
                             "items": ["ruinssword", "ruinsdagger", "ruinsherb", "ruinsshoes", "ruinshelm", "ruinsstaff"]}
items_info["chest_castle"] = {"uid": "chest_castle", "type": "chest", "tier": 7, "tradeMinMaxValue": "150000;7500000",
                              "items": ["castleshield", "castlestaff", "castleheavyarmor", "castleroguehat", "castleaxe", "castleshoe"]}
items_info["chest_temple"] = {"uid": "chest_temple", "type": "chest", "tier": 8, "tradeMinMaxValue": "200000;10000000",
                              "items": ["templearmor", "templering", "templesword", "templeaxe", "templespear", "templedagger"]}
items_info["chest_peak"] = {"uid": "chest_peak", "type": "chest", "tier": 9, "tradeMinMaxValue": "400000;20000000",
                            "items": ["peakscroll", "peakamulet", "peakherbs", "peakdagger", "peakhammer", "peakroguehat"]}
items_info["chest_volcano"] = {"uid": "chest_volcano", "type": "chest", "tier": 10, "tradeMinMaxValue": "800000;40000000",
                               "items": ["volcanomagehat", "volcanopotion", "volcanorobe", "volcanogloves", "volcanoboots", "volcanomedarmor"]}
items_info["chest_rift"] = {"uid": "chest_rift", "type": "chest", "tier": 11, "tradeMinMaxValue": "2000000;100000000",
                            "items": ["riftheavyarmor", "riftspear", "riftbow", "riftscroll", "riftmagehat", "riftstaff"]}
items_info["chest_goldcity"] = {"uid": "chest_goldcity", "type": "chest", "tier": 7, "tradeMinMaxValue": "50000;2500000",
                                "items": ["goldvestments", "goldamulet", "goldsword", "goldhat",
                                          "goldgauntlets", "goldstaff", "golddagger", "goldherb",
                                          "goldspear", "goldshield", "goldboots", "goldscroll",
                                          "goldring", "luxuriouselement", "luxuriousspirit"]}
items_info["chest_goldcity2"] = {"uid": "chest_goldcity2", "type": "chest", "tier": 10, "tradeMinMaxValue": "500000;25000000",
                                 "items": ["goldhammer", "goldplate", "goldherb2", "goldaxe",
                                           "goldhelmet", "goldgloves", "goldbow", "goldroguearmor",
                                           "goldgun", "goldroguehat", "lcogwand", "goldshoes",
                                           "opulentelement", "opulentspirit", "goldcrossbow", "goldgolem",
                                           "goldcloak", "goldstaff2", "goldamulet2", "goldrobe2",
                                           "goldsword2", "goldhat2", "goldgauntlets2", "golddagger2",
                                           "goldpotion", "goldmeal", "goldshield2", "golddessert",
                                           "goldspear2", "goldboots2", "goldscroll2", "goldring2"]}
items_info["chest_goldcity3"] = {"uid": "chest_goldcity3", "type": "chest", "tier": 11, "tradeMinMaxValue": "2000000;100000000",
                                 "items": ["platinummace", "platinumhelm", "platinumamulet"]}

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


def print_trade(x, key1, key2, key3):
    print(x["trade_data"]["item_info"]["chinese_type"], ", ",
          x["trade_data"]["item_info"]["tier"], ", ",
          x["trade_data"]["chinese_quality"], ", ",
          x["trade_data"]["item_info"]["chinese_name"], ": ",
          key1 + ": ", x[key1], ", ",
          key2 + ": ", x[key2], ", ",
          key3 + ": ", x[key3], " (",
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


def erase_duplicated_item(List):
    i = 0
    while True:
        if i >= len(List):
            break

        isFound = False
        for j in range(i):
            if List[j]["trade_data"]["item_info"]["uid"] == List[i]["trade_data"]["item_info"]["uid"] and \
               List[j]["trade_data"]["quality"] == List[i]["trade_data"]["quality"]:
                isFound = True
                break

        if isFound:
            del List[i]
            # print(List)
        else:
            i += 1


while True:
    # get all market data
    response_last = requests.get("https://smartytitans.com/api/item/last/all")
    print("status code:", response_last.status_code)
    items_last = response_last.json()

    # group market data by item
    offer_request = {}
    for item_last in items_last["data"]:
        if item_last["uid"] not in items_info:
            continue

        key = (item_last["uid"], item_last["tag1"])
        if key not in offer_request:
            offer_request[key] = {}

        # set price to None, if Qty is 0
        if item_last["goldQty"] == 0:
            item_last["goldPrice"] = None
        if item_last["gemsQty"] == 0:
            item_last["gemsPrice"] = None

        # set item_info
        offer_request[key]["item_info"] = items_info[item_last["uid"]]

        # set quality
        offer_request[key]["quality"] = item_last["tag1"]

        # set chinese_quality
        if item_last["tag1"] == None:
            offer_request[key]["chinese_quality"] = translation["texts"]["common_name"]
        else:
            offer_request[key]["chinese_quality"] = translation["texts"][item_last["tag1"] + "_name"]

        # set item_value
        offer_request[key]["item_value"] = get_item_value(items_info[item_last["uid"]], item_last["tag1"])

        # grouping
        if item_last["tType"] == "o" or item_last["tType"] == "os":
            offer_request[key]["offer"] = item_last
        elif item_last["tType"] == "r" or item_last["tType"] == "rs":
            offer_request[key]["request"] = item_last

    # find gold-to-gem rates
    gem_to_gold_rates = []
    gold_to_gem_rates = []
    for (key, data) in offer_request.items():
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
            gold_to_gem_rates.append({"trade_data": data,
                                      "offer_gold": data["offer"]["goldPrice"],
                                      "request_gems": data["request"]["gemsPrice"],
                                      "rate": int(data["offer"]["goldPrice"]/data["request"]["gemsPrice"]),
                                      "offer_gold_t": datetime.now(timezone.utc) - parser.parse(data["offer"]["updatedAt"]),
                                      "request_gems_t": datetime.now(timezone.utc) - parser.parse(data["request"]["updatedAt"])
                                      })

        # gem to gold rate
        if data["offer"]["gemsPrice"] != None and data["request"]["goldPrice"] != None:
            gem_to_gold_rates.append({"trade_data": data,
                                      "offer_gems": data["offer"]["gemsPrice"],
                                      "request_gold": data["request"]["goldPrice"],
                                      "rate": int(data["request"]["goldPrice"]/data["offer"]["gemsPrice"]),
                                      "offer_gems_t": datetime.now(timezone.utc) - parser.parse(data["offer"]["updatedAt"]),
                                      "request_gold_t": datetime.now(timezone.utc) - parser.parse(data["request"]["updatedAt"])
                                      })

    gold_to_gem_rates.sort(key=lambda x: x["rate"])
    gem_to_gold_rates.sort(key=lambda x: x["rate"], reverse=True)

    # offer-energy pair
    offer_energy_list = []
    gold_to_gem_rate_estimated = 4000000
    for (key, data) in offer_request.items():
        if "offer" not in data:
            continue

        if data["item_info"]["type"] != "xu" and \
           data["item_info"]["type"] != "xm" and \
           data["item_info"]["type"] != "z" and \
           data["item_info"]["type"] != "m" and \
           data["item_info"]["type"] != "chest":
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

            # normal sell
            offer_energy_list.append({"trade_data": data,
                                      "selling_type": "normal sell",
                                      "currency_change": data["item_value"] - offer_value,
                                      "energy_change": energy_per_sale,
                                      "offer": offer
                                      })

            # discount
            offer_energy_list.append({"trade_data": data,
                                      "selling_type": "discount",
                                      "currency_change": int(data["item_value"]/2) - offer_value,
                                      "energy_change": data["item_info"]["discount"] + energy_per_sale,
                                      "offer": offer
                                      })

            # surcharge
            if data["item_info"]["tier"] <= surcharge_tier:
                offer_energy_list.append({"trade_data": data,
                                          "selling_type": "surcharge",
                                          "currency_change": data["item_value"]*2 - offer_value,
                                          "energy_change": -data["item_info"]["surcharge"] + energy_per_sale,
                                          "offer": offer
                                          })

    # divide offer_energy_list into two lists
    energy_loss_list = []
    energy_gain_list = []
    energy_loss_boundary = []
    energy_gain_boundary = []
    for x in offer_energy_list:
        if x["energy_change"] == 0:
            continue

        x["offer_t"] = datetime.now(timezone.utc) - parser.parse(x["trade_data"]["offer"]["updatedAt"])
        x["selling_type_t"] = timedelta(seconds=0)
        x["energy_rate"] = int(-x["currency_change"]/x["energy_change"])

        # energy_gain
        if x["energy_change"] > 0:
            energy_gain_list.append(x)
            if insert(energy_gain_boundary, x):
                energy_gain_boundary.append(x)

        # energy_loss
        if x["energy_change"] < 0 and x["currency_change"] > 0:
            energy_loss_list.append(x)
            if insert(energy_loss_boundary, x):
                energy_loss_boundary.append(x)

    # try all possible pairs of energy_gain and energy_loss
    # find maximum rate
    offer_energy_pair = []
    for energy_gain in energy_gain_boundary:
        for energy_loss in energy_loss_boundary:
            rate = offer_energy_rate(energy_gain, energy_loss)
            offer_energy_pair.append({"energy_gain": energy_gain,
                                      "energy_loss": energy_loss,
                                      "rate": rate,
                                      })
    offer_energy_pair.sort(key=lambda x: x["rate"], reverse=True)
    offer_to_energy_rate = offer_energy_pair[0]["energy_gain"]["energy_rate"]
    energy_to_offer_rate = offer_energy_pair[0]["energy_loss"]["energy_rate"]

    # calculate rates for all energy_gain
    for energy_gain in energy_gain_list:
        energy_gain["rate"] = int(offer_energy_rate(energy_gain, offer_energy_pair[0]["energy_loss"]))
    energy_gain_list.sort(key=lambda x: x["rate"], reverse=True)

    # calculate rates for all energy_loss
    for energy_loss in energy_loss_list:
        energy_loss["rate"] = int(offer_energy_rate(offer_energy_pair[0]["energy_gain"], energy_loss))
    energy_loss_list.sort(key=lambda x: x["rate"], reverse=True)

    # remove some unused entries
    energy_gain_list = [x for x in energy_gain_list if x["energy_rate"] < energy_to_offer_rate]
    erase_duplicated_item(energy_gain_list)
    energy_loss_list = [x for x in energy_loss_list if x["energy_rate"] > offer_to_energy_rate]
    erase_duplicated_item(energy_loss_list)

    # print gem_to_gold
    if gem_to_gold_rates[0]["rate"] < gold_to_gem_rates[0]["rate"]:
        print("No gem_to_gold is found.")
        print_trade(gem_to_gold_rates[0], "offer_gems", "request_gold", "rate")
        print_trade(gold_to_gem_rates[0], "offer_gold", "request_gems", "rate")
    else:
        print("gold_to_gem_rates:")
        for i in range(len(gold_to_gem_rates)):
            if gold_to_gem_rates[i]["rate"] < gem_to_gold_rates[0]["rate"]:
                x = gold_to_gem_rates[i]
                print_trade(x, "offer_gold", "request_gems", "rate")
            if i >= 5:
                break

        print("gem_to_gold_rates:")
        for i in range(len(gem_to_gold_rates)):
            if gem_to_gold_rates[i]["rate"] > gold_to_gem_rates[0]["rate"]:
                x = gem_to_gold_rates[i]
                print_trade(x, "offer_gems", "request_gold", "rate")
            if i >= 5:
                break
    print()

    # print offer-energy
    print("offer-to-energy:")
    print("offer_to_energy_rate:", offer_to_energy_rate)
    print("energy_to_offer_rate:", energy_to_offer_rate)
    for i in range(len(offer_energy_pair)):
        if i >= 1:
            break

        x = offer_energy_pair[i]
        print("rate: ", int(x["rate"]), ": ",
              x["energy_gain"]["trade_data"]["item_info"]["chinese_type"], ", ",
              x["energy_gain"]["trade_data"]["item_info"]["tier"], ", ",
              x["energy_gain"]["trade_data"]["chinese_quality"], ", ",
              x["energy_gain"]["trade_data"]["item_info"]["chinese_name"], ", ",
              x["energy_gain"]["offer"], ", ",
              x["energy_gain"]["energy_rate"], "; ",

              x["energy_loss"]["trade_data"]["item_info"]["chinese_type"], ", ",
              x["energy_loss"]["trade_data"]["item_info"]["tier"], ", ",
              x["energy_loss"]["trade_data"]["chinese_quality"], ", ",
              x["energy_loss"]["trade_data"]["item_info"]["chinese_name"], ", ",
              x["energy_loss"]["offer"], ", ",
              x["energy_loss"]["energy_rate"], " (",

              x["energy_gain"]["offer_t"].seconds//60, ",",
              x["energy_loss"]["offer_t"].seconds//60, " mins ago)",
              sep="")

    print("offer_to_energy:")
    for i in range(len(energy_gain_list)):
        x = energy_gain_list[i]
        print_trade(x, "offer", "selling_type", "energy_rate")
        if i >= 5:
            break

    print("energy_to_offer:")
    for i in range(len(energy_loss_list)):
        x = energy_loss_list[i]
        print_trade(x, "offer", "selling_type", "energy_rate")
        if i >= 10:
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
