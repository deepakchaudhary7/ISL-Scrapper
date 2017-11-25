import requests
import csv

def get_url(url):
    match_no = url.split('/')[4]
    match_no = match_no.split('-')[0]
    Request_URL = "http://www.indiansuperleague.com/sifeeds/repo/football/live/india_sl/json/{0}.json".format(match_no)
    return Request_URL


def Main_scrapper(url):
    Request_URL = get_url(url)
    data        = requests.get(Request_URL)
    data        = data.json()

    with open('Data.csv', 'w') as data_file:
        fieldnames = ['S No.', 'Season', 'Match', 'Date', 'Crowd', 'Venue', 'Team', 'Opponent', 'Result', 'Home/Away', 'Formation', 'GS', 'GA', 'GD', 'Poss.', 'Shots', 'SOT', 'Shot%', 'Pass', 'Pass%', 'PC', 'Intercept', 'Cross', 'FC', 'Offsides', 'Corners', 'YC', 'RC']
        writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(0,2):
            d = {}
            d['S No.']      =   1
            d['Season']     =   data['match_detail']['series']['name'].split(',')[1].split('"')[0].lstrip().rstrip()
            d['Match']      =   data["teams"][0]["name"] + "v" + data['teams'][1]["name"]
            d['Date']       =   data['match_detail']['date']
            d['Crowd']      =   data['match_detail']['attendance']
            d['Venue']      =   data['match_detail']['venue']['name']
            d['Team']       =   data['teams'][i]['name']

            if(i==0):
                d['Opponent'] = data['teams'][1]['name']
            else:
                d['Opponent'] = data['teams'][0]['name']

            if(data['match_detail']['result']['outcome']=='D'):
                d['Result']   = "Draw"
            else:
                if(data['match_detail']['result']['winning_team_id']==data['teams']['id']):
                    d['Result'] = "Won"
                else:
                    d['Result'] = "Loss"

            if(i==0):
                d['Home/Away'] = "Home"
            else:
                d['Home/Away'] = "Away"

            d['Formation']  =   data['teams'][i]['formation']
            d['GS']         =   data['teams'][i]['score']

            if(i==0):
                d["GA"]     =   data['teams'][1]['score']
            else:
                d['GA']     =   data['teams'][0]['score']

            d['GD']         =   int(d['GS']) - int(d['GA'])
            d['Poss.']      =   data['teams'][i]['stats']['possession_percentage']
            d['Shots']      =   data['teams'][i]['stats']['events']['shots']
            d['SOT']        =   data['teams'][i]['stats']['events']['shots_on_target']
            d['Shot%']      =   float(int(d['SOT'])*100)/(int(d['Shots']))
            d['Pass']       =   data['teams'][i]['stats']['touches']['total_passes']
            d['Pass%']      =   data['teams'][i]['stats']['touches']['pass_accuracy_percentage']
            d['PC']         =   ((int(d['Pass%']) * d['Pass'])/100)
            d['Intercept']  =   data['teams'][i]['stats']['touches']['interceptions']
            d['Cross']      =   data['teams'][i]['stats']['events']['crosses']
            d['FC']         =   data['teams'][i]['stats']['events']['fouls_committed']
            d['Offsides']   =   data['teams'][i]['stats']['events']['offsides']
            d['Corners']    =   data['teams'][i]['stats']['events']['corner_kicks']
            d['YC']         =   data['teams'][i]['stats']['events']['yellow_cards']
            d['RC']         =   data['teams'][i]['stats']['events']['red_cards']

            writer.writerow(d)

    data_file.close()





Main_scrapper("http://www.indiansuperleague.com/matchcentre/19963-kerala-blasters-fc-vs-atk")
