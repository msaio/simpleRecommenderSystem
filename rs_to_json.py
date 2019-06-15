from neccessary_module import *
from popularity import *
from collaborative_filtering import *
from evaluation import *
## Loading data: CI&T Deskdrop dataset
## Get data from share_articles.csv
articles_df = pd.read_csv('shared_articles.csv')
## Only get records, "evenType" of which is "CONTERNT SHARED"
articles_df = articles_df[articles_df['eventType'] == 'CONTENT SHARED']
# print(articles_df.head(10))
################################################################################
f1 = open("content_detail.json", "w")
f1.write("[\n")
f1.close()
l = list(articles_df[["contentId", "timestamp",\
          "authorPersonId", "url", "title", "text"]]\
      .sort_values(by=["contentId"]).values)
i = 0
for contentId, timestamp, authorPersonId, url, title, text in l:
   record = {"contentId":contentId, "timestamp":timestamp,\
             "authorPersonId":authorPersonId,\
            "url":url, "title":title, "text":text}
   f = open("content_detail.json", "a")
   if(i == len(l) -1):
      f.write(json.dumps(record)+"\n")
   else:
      f.write(json.dumps(record)+","+"\n")
   f.close()
   i = i + 1
f1 = open("content_detail.json", "a")
f1.write("]")
f1.close()
#######################################
## Get Data from users_interactions.csv
interactions_df = pd.read_csv('users_interactions.csv')


## Data munging
## Associate values of eventType with strenght or weight
event_type_strength = {
   'VIEW': 1.0,
   'LIKE': 2.0, 
   'BOOKMARK': 2.5, 
   'FOLLOW': 3.0,
   'COMMENT CREATED': 4.0,  
}
## Create eventStrength and turn values of eventType into values which we associated above 
interactions_df['eventStrength'] = interactions_df['eventType'].apply(lambda x: event_type_strength[x])
# print(interactions_df.head(10))
## Number of users who interacted
users_interactions_count_df = interactions_df.groupby(['personId', 'contentId']).size().groupby('personId').size()
## Number of users who interacted 5 times at least
users_with_enough_interactions_df = users_interactions_count_df[users_interactions_count_df >= 5].reset_index()[['personId']]
## Interaction from users with at least 5 interactions
interactions_from_selected_users_df = interactions_df.\
                                    merge(users_with_enough_interactions_df, 
                                       how = 'right',
                                       left_on = 'personId',
                                       right_on = 'personId')
# print('# users: %d' % len(users_interactions_count_df))
# print('# users with at least 5 interactions: %d' % len(users_with_enough_interactions_df))
# print('# of interactions: %d' % len(interactions_df))
# print('# of interactions from users with at least 5 interactions: %d' % len(interactions_from_selected_users_df))

def get_items_interacted(person_id, interactions_df):
    # Get the user's data and merge in the movie information.
    interacted_items = interactions_df.loc[person_id]['contentId']
    return set(interacted_items if type(interacted_items) == pd.Series else [interacted_items])
def smooth_user_preference(x):
    return math.log(1+x, 2)
## An user can view an article many times + interact with different ways like (like, comment, share, recommmend,....) -> many "eventStrength"
## Get sum of "eventStrength" then use function "log" to smooth...
interactions_full_df = interactions_from_selected_users_df \
                    .groupby(['personId', 'contentId'])\
                    ['eventStrength'].sum() \
                    .apply(smooth_user_preference).reset_index()
# print('# of unique user/item interactions: %d' % len(interactions_full_df))
## print(interactions_full_df.head(10))
interactions_train_df, interactions_test_df = train_test_split(interactions_full_df,
                                   stratify=interactions_full_df['personId'], 
                                   test_size=0.20,
                                   random_state=42)
## split the df into 2 part: Train and Test with a ratio of 8 : 2 
# print('# interactions on Train set: %d' % len(interactions_train_df))
# print('# interactions on Test set: %d' % len(interactions_test_df))
## Indexing by personId
interactions_full_indexed_df = interactions_full_df.set_index('personId')
interactions_train_indexed_df = interactions_train_df.set_index('personId')
interactions_test_indexed_df = interactions_test_df.set_index('personId')
# print(interactions_full_df.loc[1])
# print(interactions_full_indexed_df.head(5))
# print(interactions_full_indexed_df.loc[-9223121837663643404])
# print("full: ", len(interactions_full_indexed_df))
# print("train: ", len(interactions_train_indexed_df))
# print("test: ", len(interactions_test_indexed_df))

## Users and Items to Json
# print interactions_full_df["personId"].unique()[:10]
# print interactions_full_df["contentId"].unique()[:10]
################################################################################
f = open("personId.json", "w")
record = {"personId" : list(interactions_full_df["personId"].unique())}
f.write(json.dumps(record))
f.close()
#######################################
# f = open("contentId.json", "w")
# record = {"contentId" : list(interactions_full_df["contentId"].sort_values().unique())}
# f.write(json.dumps(record))
# f.close()


# *****************************************************************************************
## Popularity
## Computes the most popular items
item_popularity_df = interactions_full_df.groupby('contentId')['eventStrength'].sum().sort_values(ascending=False).reset_index()
# popularity_model = PopularityRecommender(item_popularity_df, articles_df)
# print(item_popularity_df["contentId"].values)
## Because item_popularity_df got 2 columns type int64 and float64,
## it will be automaticly convert values into scientific notation
## while turn df into list.
## So we got to turn one colums into dtype object
## -> strange behavior
item_popularity_df["contentId"] = item_popularity_df["contentId"].astype(object)
list_of_popularity_items = list(item_popularity_df.values)
# print list_of_popularity_items[:10]
# print("-----Top 10 popularity items-----")
################################################################################
## Turn Popularity Items into Json
f1 = open("popularity_items.json", "w")
f1.write("[\n")
f1.close()
i = 0 
# for content_id, event_stength in list_of_popularity_items[:10]:
for content_id, event_stength in list_of_popularity_items:
   record = {"contentId" : content_id , "eventStrength" : event_stength}
   # print("contentId: ", content_id, "eventStrength: ", event_stength)
   f = open("popularity_items.json", "a")
   if(i == len(list_of_popularity_items)-1):
   # if(i == 10 -1):
      f.write(json.dumps(record)+"\n")
   else:
      f.write(json.dumps(record)+","+"\n")
   f.close()
   i = i + 1

f1 = open("popularity_items.json", "a")
f1.write("]")
f1.close()
#######################################
# *****************************************************************************************
## CF matrix factorize
## Creating a sparse pivot table with users in rows and items in columns
users_items_pivot_matrix_df = interactions_train_df.pivot(index='personId', 
                                                          columns='contentId', 
                                                          values='eventStrength').fillna(0)
# print(users_items_pivot_matrix_df.head(10))

users_items_pivot_matrix = users_items_pivot_matrix_df.values
# print(users_items_pivot_matrix[:10])

users_ids = list(users_items_pivot_matrix_df.index)
# print(users_ids[:10])

## The number of factors to factor the user-item matrix.
NUMBER_OF_FACTORS_MF = 15
## Performs matrix factorization of the original user item matrix
U, sigma, Vt = svds(users_items_pivot_matrix, k = NUMBER_OF_FACTORS_MF)
# print(U.shape)
# print(Vt.shape)
sigma = np.diag(sigma)
# print(sigma.shape)
## After the factorization, we try to to reconstruct the original matrix by multiplying its factors. The resulting matrix is not sparse any more. It was generated predictions for items the user have not yet interaction, which we will exploit for recommendations.
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) 
# print(all_user_predicted_ratings)
## Converting the reconstructed matrix back to a Pandas dataframe
cf_preds_df = pd.DataFrame(all_user_predicted_ratings, columns = users_items_pivot_matrix_df.columns, index=users_ids).transpose()
# print(cf_preds_df.head(10))
# print(len(cf_preds_df.columns))
################################################################################
cf_recommender_model = CFRecommender(cf_preds_df, articles_df)
## Turn CF results into json
l = list(interactions_full_indexed_df.index.unique().values)
f1 = open("cf_recommend_result.json", "w")
f1.write("[\n")
f1.close()

i = 0 
# for person_id in l[:10]:
for person_id in l:   
   recommend_df = cf_recommender_model.recommend_items(person_id)
   record = {"personId":person_id, "recommendItems":list(recommend_df["contentId"].values)}
   f = open("cf_recommend_result.json", "a")
   if(i == len(l)-1):
   # if(i == 10 -1):
      f.write(json.dumps(record)+"\n")
   else:
      f.write(json.dumps(record)+","+"\n")
   f.close()
   i = i + 1

f1 = open("cf_recommend_result.json", "a")
f1.write("]")
f1.close()
#######################################

# *****************************************************************************************
