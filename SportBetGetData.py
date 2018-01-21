import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests, json, shutil, os

'''
Master
Sport Bet
'''
def main():
    shutil.rmtree("SportsBetImages")
    os.mkdir("SportsBetImages")
    r = requests.get("https://app.scrapinghub.com/api/jobs/list.json?apikey=ba45f9cc9a924bafb620bf53ca39338e&project=270249&spider=sportsbet_spider&state=finished&count=1")
    jsonData = json.loads(r.text)
    jobId = jsonData['jobs'][0]['id']
    print jobId
    r = requests.get("https://storage.scrapinghub.com/items/"+jobId+"?apikey=ba45f9cc9a924bafb620bf53ca39338e&format=json")
    
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    
    # Find a workbook by name
    # Make sure you use the right name here.
    sheet = client.open("PuntDaily.com Promos")
    sheet = sheet.worksheet('sportsbet')
    sheet.clear()
    
    row = ["Link","Terms","Image Name","Image Link"]
    sheet.insert_row(row,1)
    
    jsonData = json.loads(r.text)
    for i in range(0,len(jsonData)):
        link = jsonData[i]['Link']
        terms = jsonData[i]['Terms']
        imageName = jsonData[i]['image_name'][0]
        imageURLs = jsonData[i]['image_urls'][0]
        downloadImages(imageName,imageURLs)
        row = [link,terms,imageName,imageURLs]
        sheet.insert_row(row,i+2)

def downloadImages(imageName, imageURLs):
    try:
        response = requests.get(imageURLs,stream = True)
        print imageURLs
    except:
        print "no response"
        #f = open(os.path.join(str(ctr_fold),str(ctr_url)))
    with open(os.path.join("SportsBetImages",str(imageName)), 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

if __name__ == "__main__":
    main()