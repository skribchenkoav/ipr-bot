import requests
from datetime import datetime
from datetime import timedelta
from config import config


def get_standings(league_id):
    uri = f'http://api.football-data.org/v4/competitions/{league_id}/standings'
    headers = {'X-Auth-Token': config.API_AUTH_TOKEN}
    r = requests.get(uri, headers=headers)
    data = r.json()
    rows = 'Турнирная таблица:\n'
    for entry in data["standings"][0]["table"]:
        position = entry["position"]
        team = entry["team"]["name"]
        points = entry["points"]
        rows += f"{position} - {team} - {points} очков\n"
    return rows


def get_fixtures(league_id):
    today = datetime.now()
    week_later = today + timedelta(days=7)
    today_str = today.strftime('%Y-%m-%d')
    week_later_str = week_later.strftime('%Y-%m-%d')
    uri = f"http://api.football-data.org/v4/matches?competitions={league_id}&dateFrom={today_str}&dateTo={week_later_str}"
    headers = {'X-Auth-Token': config.API_AUTH_TOKEN}
    r = requests.get(uri, headers=headers)
    data = r.json()
    rows = 'Список матчей на ближайшую неделю:\n'
    for match in data["matches"]:
        home_team = match["homeTeam"]["name"]
        away_team = match["awayTeam"]["name"]
        match_date = datetime.fromisoformat(match["utcDate"]).strftime('%d.%m.%Y %H:%M')
        rows += f"{match_date} {home_team} - {away_team}\n"
    return rows


def get_league_teams(league_id):
    uri = f'http://api.football-data.org/v4/competitions/{league_id}/standings'
    headers = {'X-Auth-Token': config.API_AUTH_TOKEN}
    r = requests.get(uri, headers=headers)
    data = r.json()
    rows = ''
    for entry in data["standings"][0]["table"]:
        team_id = entry["team"]["id"]
        name = entry["team"]["name"]
        short_name = entry["team"]["shortName"]
        tla = entry["team"]["tla"]
        rows += f'{team_id}: {name}, {short_name} ({tla})\n'
    return rows


def get_team(team_id):
    uri = f'http://api.football-data.org/v4/teams/{team_id}'
    headers = {'X-Auth-Token': config.API_AUTH_TOKEN}
    r = requests.get(uri, headers=headers)
    data = r.json()

    positions_dict = {"Goalkeeper": "Вратарь", "Defence": "Защитник", "Midfield": "Полузащитник",
                      "Offence": "Нападающий", "Forward": "Форвард"}

    rows = ''
    rows += f'Название: {data["name"]}\n\n'
    rows += f'Год основания: {data["founded"]}\n\n'
    rows += f'Тренер: {data["coach"]["name"]}\n\n'
    rows += 'Состав:\n'

    for player in data["squad"]:
        rows += f'{player["name"]} - {positions_dict[player["position"]]}\n'

    return rows
