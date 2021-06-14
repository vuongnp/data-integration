import pandas as pd

def countByYear(general):
    general = pd.DataFrame(general)
    general['year'] = pd.to_datetime(general['year'], format='%Y')
    df=general.groupby(pd.Grouper(key='year',freq='20Y')).title.count()
    labels=[]
    data=[]
    for i, count in df[:-1].items():
        labels.append(str(i).split('-')[0])
        data.append(count)
    return (labels,data)

def countByGenre(general):
    general = pd.DataFrame(general)
    genres = {}
    for x in list(general.genres.loc[:]):
        if x is not None:
            for gen in x:
                if gen in genres:
                    genres[gen]=genres[gen]+1
                else:
                    genres[gen]=1
    labels=['Drama','Comedy','Action','Adventure','Horror','Thriller','Documentary','Crime','Romance','Mystery','Fantasy','Suspense','Sci-Fi','Animation','Family']
    data=[]
    for gen in labels:
        data.append(int(genres[gen]))
    return (labels,data)
def avgRating(general):
    general = pd.DataFrame(general)
    labels=['Drama','Comedy','Action','Adventure','Horror','Thriller','Documentary','Crime','Romance','Mystery','Fantasy','Sci-Fi','Animation','Family']
    rating={'Drama':0,'Comedy':0,'Action':0,'Adventure':0,'Horror':0,'Thriller':0,'Documentary':0,'Crime':0,'Romance':0,'Mystery':0,'Fantasy':0,'Sci-Fi':0,'Animation':0,'Family':0}
    count={'Drama':0,'Comedy':0,'Action':0,'Adventure':0,'Horror':0,'Thriller':0,'Documentary':0,'Crime':0,'Romance':0,'Mystery':0,'Fantasy':0,'Sci-Fi':0,'Animation':0,'Family':0}
    for i,row in general.iterrows():
        for gen in labels:
            if general.genres.iloc[i] is not None:
                if gen in list(general.genres.iloc[i]):
                    if general.rating.iloc[i] is not None and pd.notnull(general.rating.iloc[i]):
                        rating[gen] = rating[gen]+int(general.rating.iloc[i])
                        count[gen] = count[gen]+1
    avg=[]
    label=[]
    couting=[]
    for key in labels:
        label.append(key)
        avg.append(rating[key]/count[key])
        couting.append(count[key])
    
    return (label,count,avg)
def getCountLinks(general):
    counts=[]
    count1 = 0
    count2 = 0
    count3=0
    count4=0
    count5=0
    count6=0
    count7=0
    count8=0
    for ind in general.index:
        if len(general['urls'].loc[ind])==1:
            count1+=1
        elif len(general['urls'].loc[ind])==2:
            count2+=1
        elif len(general['urls'].loc[ind])==3:
            count3+=1
        elif len(general['urls'].loc[ind])==4:
            count4+=1
        elif len(general['urls'].loc[ind])==5:
            count5+=1
        elif len(general['urls'].loc[ind])==6:
            count6+=1
        elif len(general['urls'].loc[ind])==7:
            count7+=1
        elif len(general['urls'].loc[ind])==8:
            count8+=1
    counts=[count1]+[count2]+[count3]+[count4]+[count5]+[count6]+[count7]+[count8]
    labels = ['1 sources','2 sources','3 sources','4 sources','5 sources','6 sources', '7 sources', '8 sources']
    return (labels,counts)

def results(general):
    labels=['Drama', 'Comedy', 'Action','Crime', 'Adventure', 'Thriller', 'Romance','Horror', 'Mystery', 'Fantasy', 'Sci-Fi', 'Animation', 'Family', 'Documentary']
    count=[7212, 5061, 2961, 2517, 2181, 2057,1945, 1637, 1367, 1033, 982, 834, 805, 142]
    avg=[6.254575707154742, 5.994467496542185, 5.856805133400878, 6.033929390187987, 5.281612706169823, 5.627126883811376, 7.211267605633803, 6.185935637663886, 5.989717223650386, 6.01609363569861, 5.833494675701839, 5.689409368635438, 6.571942446043166, 5.885714285714286]
    sources=['1 sources','2 sources','3 sources','4 sources','5 sources','6 sources', '7 sources', '8 sources']
    countSources=[31933, 4006, 1188, 282, 14, 0, 0, 0]
    return (labels,count,labels,avg,sources,countSources)

