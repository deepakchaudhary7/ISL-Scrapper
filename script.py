import requests
import csv
from flask import Flask, make_response, send_file, render_template, request

app = Flask(__name__)



@app.route("/")
def index():
    return render_template('index.html')


@app.route('/p1',methods = ['POST', 'GET'])
def P1_scrapper():
    if request.method == 'POST':
        return_data = request.form

        for key, value in return_data.iteritems():
            Return_URL = value.encode('utf-8')

        url         = Return_URL
        match_no    = url.split('/')[4]
        match_no    = match_no.split('-')[0]
        Request_URL = "http://www.indiansuperleague.com/sifeeds/repo/football/live/india_sl/json/{0}.json".format(match_no)
        data        = requests.get(Request_URL)
        data        = data.json()

        with open('/tmp/P1_Data.csv', 'w') as data_file:
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
                    if(data['match_detail']['result']['winning_team_id']==data['teams'][i]['id']):
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
        return send_file('/tmp/P1_Data.csv',as_attachment=True)



@app.route('/p2',methods = ['POST', 'GET'])
def P2_Scrapper():
    if request.method == 'POST':
        return_data = request.form

        for key, value in return_data.iteritems():
            Return_URL = value.encode('utf-8')


        url         = Return_URL
        match_no    = url.split('/')[4]
        match_no    = match_no.split('-')[0]
        Request_URL = "http://www.indiansuperleague.com/sifeeds/repo/football/live/india_sl/json/{0}.json".format(match_no)
        data        = requests.get(Request_URL)
        data        = data.json()


        with open('/tmp/P2_Data.csv', 'w') as data_file:
            fieldnames = ['S No', 'Season', 'Match', 'Date', 'Team', 'Opponent', 'Result', 'Home/Away', 'Formation', 'Team GS', 'Team GA', 'Player Name', 'Starter/Bench', 'GS', 'Assist', 'Shots', 'SOT', 'Pass', 'INT', 'Blocks', 'Tackles', 'YC', 'RC', 'FC', 'FS', 'Crosses', 'Offside']
            writer =   csv.DictWriter(data_file,fieldnames = fieldnames)
            writer.writeheader()
            count = 1
            for i in range(0,2):
                length = len(data['teams'][i]['players'])
                k = data['teams'][i]['players']

                for j in range(0,length):
                    if(k[j]['is_started']!=True and k[j]['is_substitute']!=True):
                        continue

                    d = {}
                    d['S No']      =   count
                    count+=1
                    d['Season']     =   data['match_detail']['series']['name'].split(',')[1].split('"')[0].lstrip().rstrip()
                    d['Match']      =   data["teams"][0]["name"] + "v" + data['teams'][1]["name"]
                    d['Date']       =   data['match_detail']['date']
                    d['Team']       =   data['teams'][i]['name']

                    if(i==0):
                        d['Opponent'] = data['teams'][1]['name']
                    else:
                        d['Opponent'] = data['teams'][0]['name']

                    if(data['match_detail']['result']['outcome']=='D'):
                        d['Result']   = "Draw"
                    else:
                        if(data['match_detail']['result']['winning_team_id']==data['teams'][i]['id']):
                            d['Result'] = "Won"
                        else:
                            d['Result'] = "Loss"

                    if(i==0):
                        d['Home/Away'] = "Home"
                    else:
                        d['Home/Away'] = "Away"

                    d['Formation']  =   data['teams'][i]['formation']
                    d['Team GS']         =   data['teams'][i]['score']

                    if(i==0):
                        d["Team GA"]     =   data['teams'][1]['score']
                    else:
                        d['Team GA']     =   data['teams'][0]['score']

                    d['Player Name']    =   k[j]['name']

                    if(k[j]['is_started']):
                        d['Starter/Bench'] = 'Starter'
                    else:
                        d['Starter/Bench'] = 'Bench'
            
                    d['GS'] =   k[j]['events']['goals']
                    d['Assist'] =   k[j]['events']['assists']
                    d['Shots']  =   k[j]['events']['shots']
                    d['SOT']    =   k[j]['events']['shots_on_target']
                    d['Pass']   =   k[j]['touches']['total_passes']
                    d['INT']    =   k[j]['touches']['interceptions']
                    d['Blocks'] =   k[j]['touches']['blocks']
                    d['Tackles']    =   k[j]['touches']['tackles']
                    d['YC'] =   k[j]['events']['yellow_cards']
                    d['RC'] =   k[j]['events']['red_cards']
                    d['FC'] =   k[j]['events']['fouls_committed']
                    d['FS'] =   k[j]['events']['fouls_suffered']
                    d['Crosses']    =   k[j]['events']['crosses']
                    d['Offside']   =   k[j]['events']['offsides']

                    writer.writerow(d)

        data_file.close()
        return send_file('/tmp/P2_Data.csv',as_attachment=True)

if __name__ == "__main__":
    app.run()
