from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def cluster(data, method, **args):
    print (args)
    """
    data : data frame with user information
    method: string
    args: parameters passed to the clustering method
        epsilon
        num_samples
    """
    data_drop = data.drop(['id', 'name', 'yelping_since'], axis=1)
    x = data_drop.values
    
    scaler = StandardScaler()
    x = scaler.fit_transform(x)
    outlier_ids = []
    outlier_cluster = 0

    ## PCA
    pca = PCA(n_components = 2)
    x_red = pca.fit_transform(x)
    print("METHOD :", method)
    if method == "kmeans":
        kmeans = KMeans(n_clusters=2, random_state=1).fit(x)
        pred = kmeans.predict(x)
        outlier_cluster = np.argmin([list(pred).count(i) for i in set(pred)])
        outliers = np.where(pred == outlier_cluster)[0]
        
    if method == "dbscan":
        dbscan = DBSCAN(eps = args['eps'], min_samples = args['min_samples'], metric = args['metric']).fit(x)
        pred = dbscan.fit_predict(x)
        outliers = np.where(pred == -1)[0]
        outlier_cluster = -1
        
    outlier_ids = data.iloc[outliers, :]['id']
    
    
    print("Variance Explained :", np.sum(pca.explained_variance_ratio_), pca.explained_variance_ratio_)
    
    ## Plotting
    color = ['r' if c == outlier_cluster else 'b' for c in pred]
    plt.scatter(x = x_red[:,0], y = x_red[:,1], c= color)
    return outlier_ids


def get_influencer_ids(fname="top_rated_res_user.csv"):
    all_users = pd.read_csv(fname, sep = ",")
    out_ids = cluster(all_users, "kmeans", min_samples = 5, eps = 60,  metric = "manhattan")
    return out_ids
    
if __name__ == "__main__":
    print(get_influencer_ids())
