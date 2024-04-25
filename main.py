import requests
import json
import time
import math
import random
from authkey import auth


def getPlayerDataFromTournament(championship_id: str):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + str(auth),
    }

    end = False
    offset = 0
    players_elo_json = {}
    while not end:
        r = requests.get(
            "https://open.faceit.com/data/v4/championships/"
            + championship_id
            + "/subscriptions?offset="
            + str(offset)
            + "&limit=10",
            headers=headers,
        )

        if r.status_code != 200:
            time.sleep(2)
            continue

        r = r.json()
        

        if r["items"] == []:
            print("Done")
            break

        for player in r["items"]:
            #if player["status"] == "checkedIn":
            r = requests.get(
                "https://open.faceit.com/data/v4/players/" + str(player["leader"]),
                headers=headers,
            ).json()
            players_elo_json[r["nickname"]] = r["games"]["cs2"]["faceit_elo"]
        offset += 10
        print(str(offset) + " done")

    return players_elo_json


def writePlayerDataToJsonFile(filename, json_data):
    sorted_players_by_elo = json.dumps(
        {k: v for k, v in sorted(json_data.items(), key=lambda item: item[1])}
    )
    sorted_players_by_elo_json = json.loads(sorted_players_by_elo)
    with open(filename, "w") as out_file:
        json.dump(sorted_players_by_elo_json, out_file, indent=4)


def readPlayerDataFromJsonFile(filename):
    with open(filename, "r") as in_file:
        return json.load(in_file)


def getAverageEloFromPlayers(players_json):
    avg = 0
    for player in players_json:
        avg += int(players_json[player])
    avg = avg / len(players_json)
    return avg


def createBalancedTeams(players_json):
    amount_teams = math.floor(len(players_json) / 5)
    average_elo = getAverageEloFromPlayers(players_json)

    all_players = []
    for player in players_json:
        all_players.append((player, players_json[player]))

    team_list = []

    random_players = random.sample(range(len(all_players)), amount_teams)
    pl_to_remove = []
    for random_player in random_players:
        team_list.append([all_players[random_player]])
        pl_to_remove.append(all_players[random_player])

    all_players = [x for x in all_players if x not in pl_to_remove]

    team_counter = 0
    best_teams = [0] * amount_teams
    for team in team_list:
        team_captain = team[0]
        elo_diff = 2000
        counter = 0
        end = False
        while not end:
            team_elo = 0
            avg_team_elo = 0
            counter += 1
            random_players_idx = random.sample(range(len(all_players)), 4)
            for i in range(4):
                team.append(all_players[random_players_idx[i]])
            if len(team) != 5:
                continue
            for player in team:
                team_elo += player[1]
            avg_team_elo = team_elo / 5
            if abs(average_elo - avg_team_elo) < elo_diff:
                best_teams[team_counter] = team
                team = [team_captain]
                elo_diff = abs(average_elo - avg_team_elo)
            else:
                team = [team_captain]
            if counter > 200:
                all_players = [x for x in all_players if x not in best_teams[team_counter]]
                end = True
        team_counter += 1
        if team_counter > amount_teams:
            print("BROKE")
            break
    return best_teams, all_players


def printCreatedTeams(best_teams, players_json):
    average_elo = getAverageEloFromPlayers(players_json)
    print("Average Elo over all players: " + str(average_elo))
    print()
    counter = 1
    for team in best_teams:
        elo = 0
        print("Team " + str(counter) + ":")
        for player in team:
            print(player[0] + " - " + str(player[1]))
            elo += player[1]
        avg_elo_per_team = elo / 5
        print("Average Team Elo: " + str(avg_elo_per_team))
        print()
        counter += 1

def createListForTS(best_teams):
    open("tsshit.txt", "w").close()
    teamchannel_counter = 467
    for team in best_teams:
        for player in team:
            with open("tsshit.txt", "a") as f:
                f.write("if(username == '" + str(player[0]) + "'){let client = backend.getClientByUID(uid); client.moveTo(" + str(teamchannel_counter) + ")}\n")
        teamchannel_counter += 1

if __name__ == "__main__":
    ###Uncomment, wenn neues Turnier erstellt
    #writePlayerDataToJsonFile("players.json", getPlayerDataFromTournament("a5542a1b-cdd1-4d23-8351-0f4dc186f027"))
    
    players_json = readPlayerDataFromJsonFile("players.json")
    best_teams, benched_players = createBalancedTeams(players_json)
    printCreatedTeams(best_teams, players_json)
    print("Benched players: " + str(benched_players))
    createListForTS(best_teams)
