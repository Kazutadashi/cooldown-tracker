import json
import urllib.request

def get_champion_names():
    """
    makes a dictionary that pairs the champion id from the riot API to the actual champion name
    eventually this function should cache the file for future use, but for now each lookup redownloads the entire list

    :return: Example: {'266': 'Aatrox', '103': 'Ahri', '84': 'Akali', '166': 'Akshan', '12': 'Alistar', '32'}
    """
    try:
        print("getting champion names...")
        with urllib.request.urlopen("http://ddragon.leagueoflegends.com/cdn/12.6.1/data/en_US/champion.json") as url:
            ddragon_data = json.loads(url.read().decode())

    except Exception as exception:
        print(exception)
        print("Could not load data dragon.")

    champion_dict = {}
    for champion_name in ddragon_data['data']:
        # print(ddragon_data['data'][champion_name])
        champion_dict[ddragon_data['data'][champion_name]['key']] = champion_name

    return champion_dict

def get_player_data(summoner_name, api_key):
    """
    gets player JSON info from the riot API to be used for the spectator API calls
    :param summoner_name: The name of the summoner to lookup
    :param api_key: the RIOT generated API key
    :return: -1 if the name is invalid or returns all player JSON data from the RIOT API
    """
    try:
        print("Fetching JSON data from server...")
        with urllib.request.urlopen("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name
                                    + "?api_key=" + api_key) as url:
            player_data = json.loads(url.read().decode())

    except Exception as exception:
        print(exception)
        print('Summoner does not exist.')
        return -1

    return player_data


def get_match_info(player_id, api_key):
    """
    uses the player ID from the riot API, and the api key to get all information related to the current match

    :param player_id: player_id located in the player's JSON datafile on the API
    :param api_key: the RIOT generated API key
    :return:
    """
    try:
        print("Getting match data...")
        with urllib.request.urlopen("https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/"
                                    + player_id + "?api_key=" + api_key) as url:
            match_data = json.loads(url.read().decode())

    except Exception as exception:
        print(exception)
        match_data = "Summoner not in game, or bad summoner name."

    return match_data


def get_champions(match_json_data):
    """
    takes in a match JSON file and returns a list of all the champions currently in the game by name
    :param match_json_data: match data taken from the riot API
    :return: a list of champions in the match by name. Example: ['Khazix', 'Trundle', 'Ziggs', 'Veigar', 'Pyke', 'Xerath', 'Jhin', 'Nautilus', 'Nocturne', 'Jax']
    """

    champion_names_dict = get_champion_names()
    champion_ids = [participant['championId'] for participant in match_json_data['participants']]

    return [champion_names_dict[str(champion_id)] for champion_id in champion_ids]


def get_cooldowns(list_of_champions):
    """
    creates a string that lists the champions name, and the CDs for each of their ability by level

    :param list_of_champions: a list of champion names
    :return: a formatted string to show off all cds for each champion
    """
    output_string = ""
    for champ in list_of_champions:
        output_string += "=====================\n"
        output_string += str(champ + " Cooldowns:\n")

        try:
            with urllib.request.urlopen(
                    "http://ddragon.leagueoflegends.com/cdn/12.6.1/data/en_US/champion/" + champ + ".json") as url:
                champion_data = json.loads(url.read().decode())

        except Exception as exception:
            print(exception)
            print('Champion does not exist.')

        output_string += ("Q: " + str(champion_data['data'][champ]['spells'][0]['cooldownBurn']) + "        ")
        output_string += ("W: " + str(champion_data['data'][champ]['spells'][1]['cooldownBurn']) + "        ")
        output_string += ("E: " + str(champion_data['data'][champ]['spells'][2]['cooldownBurn']) + "        ")
        output_string += ("R: " + str(champion_data['data'][champ]['spells'][3]['cooldownBurn']) + "\n")

    return output_string


def main(username, api_key):
    """
    Main script that incorporates all the functions above to create the main program

    :param username: summoner name to lookup
    :param api_key: riot generated api key
    :return: a formatted string with all cds.

    Example:
    =====================
    Khazix Cooldowns:
    Q: 4        W: 9        E: 20/18/16/14/12        R: 100/85/70
    """
    try:
        champions_in_current_match = (get_champions(get_match_info(get_player_data(username, api_key)['id'], api_key)))
        retrieved_cooldowns = get_cooldowns(champions_in_current_match)
        print(retrieved_cooldowns)
    except Exception as exception:
        return str(exception) + "\n Something went wrong. You may have a typo in the name, or the player is not currently" \
                                " playing on the NA server."

    print(type(retrieved_cooldowns))
    print(retrieved_cooldowns)
    return retrieved_cooldowns


# testing condition, ignore this
if __name__ == "__main__":

    main("asdf", "your_api_key_here")

