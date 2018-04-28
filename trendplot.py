import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from nltk.sentiment import vader
from scipy.stats import pearsonr 


def plot_trend(res_fname, res_name):
    fname = 'project/reviews_data/{}.html'.format(res_fname)
    df = pd.read_html(fname, header=0)[0]
    df['date'] = pd.to_datetime(df['date'])
    senti = vader.SentimentIntensityAnalyzer()
    df["sentiment"] = df["text"].apply(lambda x: senti.polarity_scores(x)["compound"])
    # print("Pearsons coeff", round(pearsonr(df["sentiment"], df["stars"])[0], 2))
    df['year'], df['month'] = df['date'].dt.year, df['date'].dt.month
    df = df[df['year'] >= 2015]
    mean_stars = df.groupby(['year', 'month'], as_index=False).mean()
    mean_stars1 = df.groupby(['year', 'month'], as_index=False)[['stars', 'sentiment']].agg({"mean_score": "mean"})
    mean_final = mean_stars[['year', 'month', 'sentiment', 'stars']]
    mean_final['period'] = mean_final['year'].astype('str').str.cat(mean_final['month'].astype('str'), sep='-')
    
    scaler = StandardScaler()
    mean_final['stars'] = scaler.fit_transform(np.expand_dims(mean_final['stars'], axis=1))
    mean_final['sentiment'] = scaler.fit_transform(np.expand_dims(mean_final['sentiment'], axis=1))
    f, ax = plt.subplots(figsize=(100, 20))

    x_col = 'period'

    sns.pointplot(ax=ax, x=x_col, y='stars', data=mean_final, color='blue')
    sns.pointplot(ax=ax, x=x_col, y='sentiment', data=mean_final, color='red')

    plt.yticks([])
    plt.ylabel('')
    plt.xlabel('')

    ax.legend(handles=ax.lines[::len(mean_final)+1], labels=["Star Rating", "Sentiment"], fontsize=70)

    ax.set_xticklabels([t.get_text().split("T")[0] for t in ax.get_xticklabels()])
    plt.tick_params(labelsize=50)

    plt.gcf().autofmt_xdate()
    
    plt.title('Trend of Star Rating and Sentiment for ' + res_name, fontsize=80)
    plt.savefig("images/" + res_fname)
    print(res_fname, pearsonr(mean_final['stars'], mean_final['sentiment'])[0])

def main():
    res_dict = {
        "mon_reviews": "Mon Ami Gabi",
        "wicked_reviews": "Wicked Spoon",
        "earl_reviews": "Earl of Sandwich",
        "gordon_reviews": "Gordon Ramsay Burger",
        "bacchanal_reivews": "Bacchanal Buffet",
        "aria_reviews": "The Buffet at ARIA",
        "eat_reviews": "Eat",
        "ellis_reviews": "Ellis Island Hotel, Casino & Brewery",        
        "fourpeaks_reviews": "Four Peaks Brewing",        
        "schwartz_reviews": "Schwartz's",        
    }
    for res_fname, res_name in res_dict.items():
        print("plotting trends for", res_fname, "...")
        plot_trend(res_fname, res_name)               
        print("#"*30)


if __name__ == "__main__":
    main()
