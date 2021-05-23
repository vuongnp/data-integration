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

