#rs1
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, KNNBasic, accuracy
from surprise.model_selection import train_test_split

# Rating matrix
ratings = pd.DataFrame([
    [5,3,0,1,0],
    [4,0,0,1,0],
    [1,1,0,5,4],
    [0,0,5,4,5],
    [0,0,5,4,0]
], columns=['A','B','C','D','E'], index=['U1','U2','U3','U4','U5'])

# Similarities
def cosine(df): return pd.DataFrame(cosine_similarity(df), index=df.index, columns=df.index)
def pearson(df): return df.T.corr()
def jaccard(df):
    b=(df>0).astype(int).values; n=len(b); S=np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            inter=np.logical_and(b[i],b[j]).sum()
            union=np.logical_or(b[i],b[j]).sum()
            S[i,j]=inter/union if union else 0
    return pd.DataFrame(S,index=df.index,columns=df.index)

print(cosine(ratings))
print(pearson(ratings))
print(jaccard(ratings))

# MovieLens User-Based and Item-Based CF
from surprise import Dataset, KNNBasic, accuracy
from surprise.model_selection import train_test_split

# Load MovieLens 100k
data = Dataset.load_builtin('ml-100k')

# Train-test split
train, test = train_test_split(data, test_size=0.2, random_state=42)

# ------------------------------
# User-Based Collaborative Filtering
# ------------------------------
user_cf = KNNBasic(sim_options={'name': 'cosine', 'user_based': True})
user_cf.fit(train)
print(user_cf.predict(5,100))
print("User-Based RMSE:")
accuracy.rmse(user_cf.test(test))

# ------------------------------
# Item-Based Collaborative Filtering
# ------------------------------
item_cf = KNNBasic(sim_options={'name': 'cosine', 'user_based': False})
item_cf.fit(train)

print("Item-Based RMSE:")
accuracy.rmse(item_cf.test(test))

#rs2
import numpy as np
import pandas as pd
from numpy.linalg import svd
# Small matrix
R = np.array([[2,3,2],
              [3,2,-2],
              [1,4,9]], float)
# SVD
U, s, Vt = svd(R)
# Reconstruction
R_hat = U @ np.diag(s) @ Vt
print("Reconstructed:\n", R_hat)
# Low-rank approx
k=2
R_k = U[:,:k] @ np.diag(s[:k]) @ Vt[:k,:]
print("Rank-2 Approx:\n", R_k)

# Matrix with missing values
M = np.array([[5, np.nan, 3],
              [4, 2, np.nan],
              [np.nan, 1, 4]], float)
# Fill missing with column mean
M_filled = np.where(np.isnan(M), np.nanmean(M,axis=0), M)
# SVD completion (one iteration)
U,s,Vt = svd(M_filled)
M_completed = U[:,:2] @ np.diag(s[:2]) @ Vt[:2,:]
print("Completed:\n", M_completed)
# PCA + NMF simple pipeline
from sklearn.decomposition import PCA, NMF

pca = PCA(n_components=2).fit_transform(M_filled)
M_pca = PCA(n_components=2).fit(M_filled).inverse_transform(pca)
nmf = NMF(n_components=2, init='random')
W = nmf.fit_transform(M_filled)
H = nmf.components_
M_nmf = W @ H
print("PCA:\n", M_pca)
print("NMF:\n", M_nmf)

# rs3
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
rows = []
for i in range(15000):
    u = np.random.randint(0, 1000)
    it = np.random.randint(0, 500)
    r = np.clip(np.random.normal(3, 1), 1, 5)
    rows.append([u, it, r])
inter = pd.DataFrame(rows, columns=['user_id', 'item_id', 'rating'])
matrix = inter.pivot_table(index='user_id', columns='item_id', values='rating', fill_value=0)
scaler = StandardScaler()
X = scaler.fit_transform(matrix)
kmeans = KMeans(n_clusters=6, random_state=42)
kmeans.fit(X)
labels = kmeans.labels_

X2 = PCA(n_components=2).fit_transform(X)
plt.scatter(X2[:, 0], X2[:, 1], c=labels, s=10)
plt.title("User Clusters via K-Means")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()
def predict_user_cluster(user_id):
    user_vector = matrix.iloc[user_id].values.reshape(1, -1)
    user_vector_scaled = scaler.transform(user_vector)
    cluster = kmeans.predict(user_vector_scaled)[0]
    return cluster
user_id = 10
pred_cluster = predict_user_cluster(user_id)
print(f"\nUser {user_id} belongs to Cluster {pred_cluster}")
def recommend_for_cluster(cluster_id, top_n=5):
    cluster_users = matrix.index[np.where(labels == cluster_id)[0]]
    cluster_data = matrix.loc[cluster_users]
    item_popularity = cluster_data.mean(axis=0).sort_values(ascending=False)
    print(f"\nTop {top_n} items recommended for Cluster {cluster_id}:")
    print(item_popularity.head(top_n))
recommend_for_cluster(pred_cluster, top_n=5)

# RS4 – Content-Based Recommendation System
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample movies dataset
movies = pd.DataFrame({
    'movieId': range(1, 11),
    'title': [
        'Toy Story (1995)', 'Jumanji (1995)', 'Heat (1995)', 'GoldenEye (1995)',
        'Casino (1995)', 'Sense and Sensibility (1995)', 'Four Weddings (1994)',
        'Speed (1994)', 'Pulp Fiction (1994)', 'Shawshank Redemption (1994)' ],
    'genres': [
        'Adventure|Animation|Children|Comedy',
        'Adventure|Children|Fantasy',
        'Action|Crime|Thriller',
        'Action|Adventure|Thriller',
        'Crime|Drama',
        'Drama|Romance',
        'Comedy|Romance',
        'Action|Thriller',
        'Crime|Drama|Thriller',
        'Drama']})

# Step 1: Preprocess Movie Content
movies['genres_clean'] = movies['genres'].str.replace('|', ' ')
movies['content'] = movies['title'] + ' ' + movies['genres_clean']

# Step 2: TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['content'])

# Step 3: Cosine Similarity Matrix
cos_sim = cosine_similarity(tfidf_matrix)

# Step 4: Recommendation Function
def recommend(movie_title, top_n=5):
    movie_title = movie_title.lower()

    matches = movies[movies['title'].str.lower().str.contains(movie_title)]
    if matches.empty:
        return "Movie not found."

    idx = matches.index[0]
    scores = list(enumerate(cos_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    rec_ids = [i for i, s in scores]
    rec_movies = movies.loc[rec_ids, ['title', 'genres']]
    rec_movies['similarity'] = [s for i, s in scores]
    return rec_movies

# Example Usage
print("Movies similar to 'Toy Story':\n")
print(recommend("Toy Story", top_n=5))

# RS5 – Collaborative Filtering Models (KNN + MF Models)
from surprise import Dataset, Reader
from surprise import KNNWithMeans, KNNBasic, KNNWithZScore, KNNBaseline
from surprise import SVD, SVDpp, NMF
from surprise.model_selection import train_test_split, cross_validate
from surprise import accuracy
import pandas as pd

# -----------------------------
# Small Ratings Dataset
# -----------------------------
ratings_df = pd.DataFrame([
    ['User1', 'MovieA', 5],
    ['User1', 'MovieB', 4],
    ['User2', 'MovieA', 3],
    ['User2', 'MovieC', 4],
    ['User3', 'MovieA', 4],
    ['User3', 'MovieC', 5],
    ['User4', 'MovieB', 5],
    ['User4', 'MovieC', 3]
], columns=['user', 'item', 'rating'])

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings_df, reader)
trainset, testset = train_test_split(data, test_size=0.25, random_state=42)
# User-based Cosine
ubc = KNNWithMeans(sim_options={'name': 'cosine', 'user_based': True})
ubc.fit(trainset)
pred_ubc = ubc.test(testset)
# Item-based Cosine
ibc = KNNWithMeans(sim_options={'name': 'cosine', 'user_based': False})
ibc.fit(trainset)
pred_ibc = ibc.test(testset)
print("\n--- Predictions for User1 on MovieC ---")
print("User-Based Cosine :", ubc.predict('User1', 'MovieC').est)
print("Item-Based Cosine :", ibc.predict('User1', 'MovieC').est)

# -----------------------------
# 2. KNN FLAVOURS (on ML-100k)
# -----------------------------
print("\n--- KNN Variants on ML-100k ---")
data_ml = Dataset.load_builtin("ml-100k")

knn_algos = {"KNNBasic": KNNBasic,
    "KNNWithMeans": KNNWithMeans,
    "KNNWithZScore": KNNWithZScore,
    "KNNBaseline": KNNBaseline}

for name, algo in knn_algos.items():
    print(f"\n{name}:")
    model = algo(sim_options={'name': 'cosine', 'user_based': True})
    cross_validate(model, data_ml, measures=['RMSE', 'MAE'], cv=3, verbose=True)

# -----------------------------
# 3. MF MODELS (SVD, SVD++, NMF, PMF)
# -----------------------------
mf_algos = {"SVD": SVD(),
    "SVD++": SVDpp(),
    "NMF": NMF(),
    "PMF": SVD(biased=False)}

results = {}
for name, model in mf_algos.items():
    scores = cross_validate(model, data_ml, measures=['RMSE', 'MAE'], cv=3, verbose=True)
    results[name] = scores['test_rmse'].mean()

best_mf = min(results, key=results.get)
print(f"\nBest MF Model = {best_mf}")

# -----------------------------
# 4. Recommendations with best MF
# -----------------------------
trainset, testset = train_test_split(data_ml, test_size=0.2)
final_model = mf_algos[best_mf]
final_model.fit(trainset)
preds = final_model.test(testset)

def get_top_n(preds, n=5):
    from collections import defaultdict
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in preds:
        top_n[uid].append((iid, est))
    for uid in top_n:
        top_n[uid] = sorted(top_n[uid], key=lambda x: x[1], reverse=True)[:n]
    return top_n

top_n = get_top_n(preds, n=5)

print("\n--- Top-5 recommendations for first 3 users ---")
for uid, recs in list(top_n.items())[:3]:
    print(f"\nUser {uid}:")
    for iid, rating in recs:
        print(f"  Movie {iid} -> {rating:.2f}")

# ============================================================
# RS6 + RS7 Combined – Simplified & Clean Version
# Includes: Random / Average / Bandwagon / Segment Attacks +
#           RDMA Detection + ROC Curves
# ============================================================
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from surprise import Dataset, Reader, KNNWithMeans
from sklearn.metrics import roc_curve, auc

np.random.seed(42)
random.seed(42)

# ------------------------------------------------------------
# 1. BASE DATASET
# ------------------------------------------------------------
ratings_data = [
    ['User1','Movie_Action1',5], ['User1','Movie_Action2',4.5],
    ['User1','Movie_Comedy1',3], ['User1','Movie_Drama1',2.5],

    ['User2','Movie_Comedy1',5], ['User2','Movie_Comedy2',4.5],
    ['User2','Movie_Action1',3], ['User2','Movie_Drama1',3.5],

    ['User3','Movie_Action1',4.5], ['User3','Movie_Action2',4],
    ['User3','Movie_Drama1',4.5], ['User3','Movie_Drama2',5],

    ['User4','Movie_Action1',3.5], ['User4','Movie_Comedy1',4],
    ['User4','Movie_Horror1',3],

    ['User5','Movie_Drama1',5], ['User5','Movie_Drama2',4.5],
    ['User5','Movie_Action1',3],

    ['User6','Movie_Horror1',5], ['User6','Movie_Horror2',4.5],
    ['User6','Movie_Action1',4], ['User6','Movie_Action2',4.5]
]

ratings_df = pd.DataFrame(ratings_data, columns=['user','item','rating'])
target_item = "Movie_Action1"


# ------------------------------------------------------------
# 2. Baseline Recommender
# ------------------------------------------------------------
def build_recommender(df):
    reader = Reader(rating_scale=(1,5))
    data = Dataset.load_from_df(df[['user','item','rating']], reader)
    trainset = data.build_full_trainset()
    algo = KNNWithMeans(k=3, sim_options={'name':'cosine', 'user_based':True})
    algo.fit(trainset)
    return algo, trainset

def recommend_top_n(algo, trainset, user, n=5):
    all_items = trainset.all_items()
    user_inner = trainset.to_inner_uid(user)
    rated = {i for i,_ in trainset.ur[user_inner]}
    unrated = [trainset.to_raw_iid(i) for i in all_items if i not in rated]
    preds = [algo.predict(user, itm) for itm in unrated]
    preds.sort(key=lambda x: x.est, reverse=True)
    return preds[:n]


baseline_algo, baseline_train = build_recommender(ratings_df)


# ------------------------------------------------------------
# 3. ATTACK MODELS
# ------------------------------------------------------------
def random_attack(df, target, n_fake=3, filler=3, push=True):
    mean = df['rating'].mean()
    std = df['rating'].std()
    fill_items = [i for i in df['item'].unique() if i != target]
    tgt_rating = 5 if push else 1
    rows=[]
    for k in range(n_fake):
        fake=f"Fake_R{k}"
        for item in random.sample(fill_items, filler):
            rows.append([fake, item, np.clip(np.random.normal(mean,std),1,5)])
        rows.append([fake, target, tgt_rating])
    return pd.DataFrame(rows, columns=['user','item','rating'])

def average_attack(df, target, n_fake=3, filler=3, push=True):
    stats = df.groupby("item")["rating"].mean()
    fill_items=[i for i in df['item'].unique() if i!=target]
    tgt_rating = 5 if push else 1
    rows=[]
    for k in range(n_fake):
        fake=f"Fake_A{k}"
        for item in random.sample(fill_items, filler):
            rating=np.clip(np.random.normal(stats[item],0.5),1,5)
            rows.append([fake,item,rating])
        rows.append([fake,target,tgt_rating])
    return pd.DataFrame(rows, columns=['user','item','rating'])

def bandwagon_attack(df, target, n_fake=3, filler=3, push=True):
    popular=df['item'].value_counts().sort_values(ascending=False).index[:3]
    tgt_rating = 5 if push else 1
    fill_items=[i for i in df['item'].unique() if i!=target]
    rows=[]
    for k in range(n_fake):
        fake=f"Fake_B{k}"
        for item in popular:
            rows.append([fake,item, random.uniform(4,5)])
        for item in random.sample(fill_items, filler):
            rows.append([fake,item, np.clip(np.random.normal(df['rating'].mean(), df['rating'].std()),1,5)])
        rows.append([fake,target,tgt_rating])
    return pd.DataFrame(rows, columns=['user','item','rating'])


# ------------------------------------------------------------
# 4. SEGMENT ATTACK (RS6)
# ------------------------------------------------------------
def segment_users(df):
    action_items=[i for i in df['item'].unique() if "Action" in i]
    seg=df[df['item'].isin(action_items)]
    return list(seg.groupby("user")['rating'].mean().loc[lambda x:x>=4].index)

segment_group = segment_users(ratings_df)

def segment_attack(df, target, n_fake=3, filler=3, push=True):
    action_items=[i for i in df['item'].unique() if "Action" in i and i!=target]
    popular=action_items[:2]
    fill_items=[i for i in df['item'].unique() if i not in popular]
    tgt=5 if push else 1
    rows=[]
    for k in range(n_fake):
        fake=f"Fake_S{k}"
        for item in popular:
            rows.append([fake,item, random.uniform(4,5)])
        for item in random.sample(fill_items, filler):
            rows.append([fake,item, np.clip(np.random.normal(df['rating'].mean(), df['rating'].std()),1,5)])
        rows.append([fake,target,tgt])
    return pd.DataFrame(rows, columns=['user','item','rating'])


# ------------------------------------------------------------
# 5. DETECTION METRICS (RS7)
# ------------------------------------------------------------
def detection_features(df, user):
    user_df=df[df['user']==user]
    if user_df.empty: return None
    item_means=df.groupby('item')['rating'].mean()
    rdma=np.mean([abs(r-item_means[i]) for i,r in zip(user_df['item'], user_df['rating'])])
    return {
        "user":user,
        "RDMA":rdma,
        "is_attacker":user.startswith("Fake_")
    }

def build_detection_df(df):
    rows=[]
    for u in df['user'].unique():
        feat=detection_features(df,u)
        if feat: rows.append(feat)
    return pd.DataFrame(rows)


# ------------------------------------------------------------
# 6. PLOT ROC CURVES
# ------------------------------------------------------------
attack_funcs = {
    "Random": random_attack,
    "Average": average_attack,
    "Bandwagon": bandwagon_attack,
    "Segment": segment_attack
}


plt.figure(figsize=(6,5))
for name,func in attack_funcs.items():
    atk = func(ratings_df, target_item, n_fake=40, filler=4, push=True)
    aug = pd.concat([ratings_df, atk], ignore_index=True)
    det = build_detection_df(aug)

    y_true = det['is_attacker'].astype(int)
    y_score= det['RDMA']
    fpr,tpr,_= roc_curve(y_true,y_score)
    AUC=auc(fpr,tpr)

    plt.plot(fpr,tpr,label=f"{name} (AUC={AUC:.3f})")

plt.plot([0,1],[0,1],'--')
plt.title("ROC Curves for Attack Detection (RDMA)")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.grid(alpha=0.3)
plt.show()

