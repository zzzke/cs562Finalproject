import csv
import textblob
from wordcloud import WordCloud
import os
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import re
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

statecounter = {
'Alabama' : 0,
'Alaska' : 0,
'Arizona' : 0,
'Arkansas' : 0,
'California' : 0,
'Colorado' : 0,
'Connecticut' : 0,
'Delaware' : 0,
'Florida' : 0,
'Georgia' : 0,
'Hawaii' : 0,
'Idaho' : 0,
'Illinois' : 0,
'Indiana' : 0,
'Iowa' : 0,
'Kansas' : 0,
'Kentucky' : 0,
'Louisiana' : 0,
'Maine' : 0,
'Maryland' : 0,
'Massachusetts' : 0,
'Michigan' : 0,
'Minnesota' : 0,
'Mississippi' : 0,
'Missouri' : 0,
'Montana' : 0,
'Nebraska' : 0,
'Nevada' : 0,
'New Hampshire' : 0,
'New Jersey' : 0,
'New Mexico' : 0,
'New York' : 0,
'North Carolina' : 0,
'North Dakota' : 0,
'Ohio' : 0,
'Oklahoma' : 0,
'Oregon' : 0,
'Pennsylvania' : 0,
'Rhode Island' : 0,
'South Carolina' : 0,
'South Dakota' : 0,
'Tennessee': 0,
'Texas' : 0,
'Utah' : 0,
'Vermont' : 0,
'Virginia' : 0,
'Washington' : 0,
'West Virginia' : 0,
'Wisconsin' : 0,
'Wyoming' : 0
}

states = [
'Alabama',
'Alaska',
'Arizona',
'Arkansas',
'California',
'Colorado',
'Connecticut',
'Delaware',
'Florida',
'Georgia',
'Hawaii',
'Idaho',
'Illinois',
'Indiana',
'Iowa',
'Kansas',
'Kentucky',
'Louisiana',
'Maine',
'Maryland',
'Massachusetts',
'Michigan',
'Minnesota',
'Mississippi',
'Missouri',
'Montana',
'Nebraska',
'Nevada',
'New Hampshire',
'New Jersey',
'New Mexico',
'New York',
'North Carolina',
'North Dakota',
'Ohio',
'Oklahoma',
'Oregon',
'Pennsylvania',
'Rhode Island',
'South Carolina',
'South Dakota',
'Tennessee',
'Texas',
'Utah',
'Vermont',
'Virginia',
'Washington',
'West Virginia',
'Wisconsin',
'Wyoming'
]

statewordfreq = []
statehashtag = []
statesentiment = []

def remove_stopword(intext):
    stop_words = {'a','able','about','across','after','all','almost','also','am','among','an','and','any','are',
                  'as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does',
                  'either','else','ever','every','for','from','get','got','had','has','have','he','her','hers',
                  'him','his','how','however','i','if','in','into','is','it','its','just','least','let','like',
                  'likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often',
                  'on','only','or','other','our','own','rather','said','say','says','she','should','since','so',
                  'some','than','that','the','their','them','then','there','these','they','this','tis','to','too',
                  'twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why',
                  'will','with','would','yet','you','your'}
    text = word_tokenize(intext)
    tweettext = []
    hashtag = []
    tagflag = False
    for w in text:
        if w.lower().strip("\n") not in stop_words and w.isalpha():
            if tagflag == True:
                hashtag.append(w)
                tagflag = False
            elif w.lower().strip("\n") != "https" and w.lower().strip("\n") != "syria" and w.lower().strip("\n") != "airstrike":
                tweettext.append(w)
        if w.lower().strip("\n") not in stop_words and w[0] == '#':
            tagflag = True
    return tweettext, hashtag

def stemmer(tweettext):
    sb  = SnowballStemmer("english")
    docterm = []
    for w in tweettext:
        word = sb.stem(w)
        docterm.append(word)
    return docterm

def countwordfreq(csvpath):
    if not os.path.exists(csvpath):
        print("tweet.csv doesn't exist")
        return
    for key in statecounter.keys():
        filename1 = key + "_stem.txt"
        filename2 = key + "_hashtag.txt"
        if os.path.exists(filename1):
            os.remove(filename1)
        if os.path.exists(filename2):
            os.remove(filename2)
    for key in statecounter.keys():
        filename1 = key + "_stem.txt"
        filename2 = key + "_hashtag.txt"
        file1 = open(filename1, "a")
        file2 = open(filename2, "a")
        csvFile = open(csvpath, encoding='utf-8', mode="r")
        reader = csv.reader(csvFile)
        for row in reader:
            if row[4] == key:
                tweet, hashtag = remove_stopword(row[1])
                term = stemmer(tweet)
                for w in term:
                    file1.write(w)
                    file1.write('\n')
                for h in hashtag:
                    file2.write("#"+h)
                    file2.write('\n')
        file1.close()
        file2.close()
        csvFile.close()
    for key in statecounter.keys():
        filename1 = key + "_stem.txt"
        filename2 = key + "_hashtag.txt"
        file1 = open(filename1, "r")
        file2 = open(filename2, "r")
        worddict = {}
        termlst = []
        tagdict = {}
        taglst = []
        for line1 in file1.readlines():
            line1 = line1.strip('\n')
            termlst.append(line1)
        for word in termlst:
            if word in worddict.keys():
                worddict[word] += 1
            else:
                worddict[word] = 1
        statewordfreq.append(worddict)
        for line2 in file2.readlines():
            line2 = line2.strip('\n')
            termlst.append(line2)
        for tag in taglst:
            if tag in tagdict.keys():
                tagdict[tag] += 1
            else:
                tagdict[tag] = 1
        statehashtag.append(tagdict)
        file1.close()
        file2.close()
    usmap = np.array(Image.open("usmap.jpg"))
    for i in range(len(statewordfreq)):
        if not statewordfreq[i]:
            continue
        wordcloud1 = WordCloud(width=900, height=500, max_words=1628, relative_scaling=1, mask = usmap,
                              normalize_plurals=False).generate_from_frequencies(statewordfreq[i])
        plt.imshow(wordcloud1, interpolation='bilinear')
        plt.title(states[i])
        plt.axis("off")
        if os.path.exists(states[i]+"wc.jpg"):
            os.remove(states[i]+"wc.jpg")
        plt.savefig(states[i]+"wc.jpg")

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def sentiment(csvpath):
    if not os.path.exists(csvpath):
        print("tweet.csv doesn't exist")
        return
    for key in statecounter.keys():
        sen = {'pos': 0, 'neg': 0, 'neu': 0}
        csvFile = open(csvpath, encoding='utf-8', mode="r")
        reader = csv.reader(csvFile)
        for row in reader:
            if row[4] == key:
                analysis = textblob.TextBlob(clean_tweet(row[1]))
                if analysis.sentiment.polarity > 0:
                    sen['pos'] += 1
                elif analysis.sentiment.polarity == 0:
                    sen['neu'] += 1
                else:
                    sen['neg'] += 1
        print(sen)
        statesentiment.append(sen)
        csvFile.close()

def statistic():
    total = 0
    totalpos = 0
    totalneg = 0
    totalneu = 0
    statepercent = []
    for i in range(len(statesentiment)):
        staterate = {'pos': 0, 'neu': 0, 'neg': 0, 'total': 0}
        statetotal = statesentiment[i]['pos'] + statesentiment[i]['neu'] + statesentiment[i]['neg']
        if statetotal == 0:
            statepercent.append(staterate)
            continue
        total += statetotal
        totalpos += statesentiment[i]['pos']
        totalneu += statesentiment[i]['neu']
        totalneg += statesentiment[i]['neg']
        staterate['total'] = statetotal
        staterate['pos'] = statesentiment[i]['pos'] / statetotal
        staterate['neu'] = statesentiment[i]['neu'] / statetotal
        staterate['neg'] = statesentiment[i]['neg'] / statetotal
        statepercent.append(staterate)
    return total, totalpos / total, totalneu / total, totalneg / total, statepercent

def countstateactive(csvpath):
    if not os.path.exists(csvpath):
        print("tweet.csv doesn't exist")
        return
    csvFile = open(csvpath, encoding='utf-8', mode="r")
    reader = csv.reader(csvFile)
    for row in reader:
        if row[4] in statecounter:
            statecounter[row[4]] += 1
    print(statecounter)
    csvFile.close()

def visualization(statepercent):
    map = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64, urcrnrlat=49,
                projection='lcc', lat_1=33, lat_2=45, lon_0=-95)
    map.readshapefile('st99_d00', name='states', drawbounds=True)
    state_names = []
    for shape_dict in map.states_info:
        state_names.append(shape_dict['NAME'])
    ax = plt.gca()
    for i in range(len(states)):
        seg = map.states[state_names.index(states[i])]
        if statepercent[i]['pos'] > statepercent[i]['neg']:
            poly = Polygon(seg, facecolor='blue', edgecolor='blue')
        elif statepercent[i]['pos'] < statepercent[i]['neg']:
            poly = Polygon(seg, facecolor='red', edgecolor='red')
        elif statepercent[i]['total'] == 0:
            continue
        else:
            poly = Polygon(seg, facecolor='grey', edgecolor='grey')
        ax.add_patch(poly)
    plt.title("attitudes of each states towards airstrike")
    plt.show()

def piechart(total, tpos, tneu, tneg):
    plt.figure(figsize=(6, 9))
    labels = ['positive', 'negative', 'neural']
    sizes = [(total * tpos), (total * tneu), (total * tneg)]
    colors = ['blue', 'red', 'grey']
    explode = (0, 0, 0)
    patches, text1, text2 = plt.pie(sizes,
                                    explode=explode,
                                    labels=labels,
                                    colors=colors,
                                    autopct='%3.2f%%',
                                    shadow=False,
                                    startangle=90,
                                    pctdistance=0.6)
    plt.axis('equal')
    plt.show()

def main():
    csvpath = 'tweet.csv'
    countstateactive(csvpath)
    countwordfreq(csvpath)
    sentiment(csvpath)
    total, tpos, tneu, tneg, statepercent = statistic()
    visualization(statepercent)
    piechart(total, tpos, tneu, tneg)

if __name__ == "__main__":
    main()
