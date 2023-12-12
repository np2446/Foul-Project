from nba_api.stats.endpoints import boxscoretraditionalv2, leaguegamefinder
import csv

def get_fouls(game_id):
    # Requesting data
    boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
    data_frames = boxscore.get_data_frames()

    # The second DataFrame usually contains the team statistics
    team_stats_df = data_frames[1]

    # get away and home team abbreviations
    away_team = team_stats_df['TEAM_ABBREVIATION'][0]
    home_team = team_stats_df['TEAM_ABBREVIATION'][1]

    # get season
    season = game_id[3:5]

    # Calculating total fouls (PF) for each team
    total_fouls = team_stats_df.groupby('TEAM_ABBREVIATION')['PF'].sum()

    # return a tuple with the fouls for each team (away, home)
    away_fouls, home_fouls = total_fouls

    return season, away_team, home_team, away_fouls, home_fouls

def get_gameids():
    all_game_ids = []

    # Loop through each season from 2000 to 2019
    for year in range(2000, 2020):
        # Format the season year
        season_year = f'{year}-{str(year+1)[2:]}'

        # Create a query for regular season games for the specific season
        game_finder = leaguegamefinder.LeagueGameFinder(season_nullable=season_year, 
                                                        league_id_nullable='00', 
                                                        season_type_nullable='Regular Season')

        # Get the DataFrame from the response
        games_df = game_finder.get_data_frames()[0]

        # Extract game IDs and add them to the list
        game_ids = games_df['GAME_ID'].unique()
        all_game_ids.extend(game_ids)

    # Removing duplicates if any
    unique_game_ids = list(set(all_game_ids))
    return unique_game_ids

def get_fouls_for_games(file_name):
    # get game ids
    game_ids = get_gameids()

    # create a csv file to write to
    with open('fouls.csv', 'w') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(['game_id', 'away_team', 'home_team',  'away_fouls', 'home_fouls'])
        # for each game id
        for game_id in game_ids:
            print("Getting fouls for game: " + game_id)
            # get the fouls for each team
            season, away_team, home_team, away_fouls, home_fouls = get_fouls(game_id)
            # write the data to the csv file
            print(f"Game ID: {game_id}, Season: {season}, Away Team: {away_team}, Home Team: {home_team}, Away Fouls: {away_fouls}, Home Fouls: {home_fouls}")
            writer.writerow([game_id, season, away_team, home_team, away_fouls, home_fouls])

if __name__ == '__main__':
    get_fouls_for_games('games.csv')
    
