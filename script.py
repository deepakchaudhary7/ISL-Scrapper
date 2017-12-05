import requests
import csv
from bs4 import BeautifulSoup
from lxml import etree
import urllib2
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



@app.route('/ileague',methods = ['POST', 'GET'])
def i_league_Scrapper():
    if request.method == 'POST':
        return_data = request.form

        for key, value in return_data.iteritems():
            Return_URL = value.encode('utf-8')

    url = Return_URL
    url = url.split('=')[1]
    url = "https://administrator.the-aiff.com/view/fixture/"+str(url)
    
    # setting up the BeautifulSoup
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content,'html.parser')

    # setting up the etree (lxml.html)
    response = urllib2.urlopen(url) # html fetching
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)


    home_team = tree.xpath('/html/body/div[1]/div[1]/div/span')[0].text.lstrip().encode('utf-8')
    away_team = tree.xpath('/html/body/div[1]/div[3]/div/span')[0].text.lstrip().encode('utf-8')

    home_team_score = tree.xpath('/html/body/div[1]/div[2]/div[4]/div[1]')[0].text.lstrip().encode('utf-8')
    home_team_score = home_team_score.replace('\n',' ').rstrip()

    away_team_score = tree.xpath('/html/body/div[1]/div[2]/div[4]/div[3]')[0].text.lstrip().encode('utf-8')
    away_team_score = away_team_score.replace('\n',' ').rstrip()

    tournament = tree.xpath('/html/body/div[1]/div[2]/div[1]')[0].text.lstrip().encode('utf-8')
    tournament = tournament.replace('\n','').rstrip()

    date = tree.xpath('/html/body/div[1]/div[2]/div[2]')[0].text.lstrip().encode('utf-8')
    date = date.replace('\n',' ').rstrip().replace('  ','')



    k = soup.find_all('table')


    with open('/tmp/I-LEAGUE_Data.csv', 'w') as data_file:
         fieldnames = ['Tournament', 'Date & Time', 'Home Team', 'Away Team', 'Home Goals', 'Away Goals', 'Team Name', 'Player Name', 'Jersey No.', 'Start/Bench', 'Goal Time', 'Sub Time', 'Yellow(True/False)', 'Red(True/False)']
         writer = csv.DictWriter(data_file, fieldnames=fieldnames)
         writer.writeheader()
         d = {}
         look_up = [8,10,9,11]

         for i in look_up:
             rows = k[i].find_all('tr')
             for row in rows:
                temp = row.find_all('td')
                d['Tournament'] = tournament
                d['Date & Time'] = date
                d['Home Team'] = home_team
                d['Away Team'] = away_team
                d['Home Goals'] = home_team_score
                d['Away Goals'] = away_team_score

                if i==8 or i==10:
                    d['Team Name'] = home_team
                else:
                    d['Team Name'] = away_team

                if i==8 or i==9:
                    d['Start/Bench'] = 'Start'
                else:
                    d['Start/Bench'] = 'Bench'

                d['Player Name'] = temp[1].get_text().encode('utf-8')
                d['Jersey No.'] = temp[0].get_text().encode('utf-8')

                temp = temp[2].find_all('ul')


                g_t = temp[0].find_all('li', class_="goal")
                if(len(g_t)==0):
                    G_T = None
                else:
                    G_T = g_t[0].get_text()


                s_t = temp[0].find_all('li', class_='sub-out')
                if(len(s_t)==0):
                    s_t = temp[0].find_all('li', class_='sub-in')
                    if(len(s_t)==0):
                        S_T = None
                    else:
                        S_T = s_t[0].get_text()
                else:
                    S_T = s_t[0].get_text()


                z = temp[0].find_all('li', class_='yellow')
                if(len(z)==0):
                    d['Yellow(True/False)'] = "False"
                else:
                    d['Yellow(True/False)'] = "True"

                z = temp[0].find_all('li', class_='red')
                if(len(z)==0):
                    d['Red(True/False)'] = "False"
                else:
                    d['Red(True/False)'] = "True"

                d['Goal Time'] = G_T
                d['Sub Time'] = S_T

                writer.writerow(d)

    data_file.close()
    return send_file('/tmp/I-LEAGUE_Data.csv',as_attachment=True)


if __name__ == "__main__":
    app.run()
