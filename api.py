import os
import googleapiclient.discovery

# Some initializations. Api key and video id to modify.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyCzLzeKOj6Ovz7sT06DYG1Lc9v_uXgKmFE"
youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey = DEVELOPER_KEY)
video_id = "TI4PXFUOPR8"
#https://www.youtube.com/watch?v=TI4PXFUOPR8

# Get the texts only from the comments infos
def load_comments(match, comments_list):
    for item in match["items"]:
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
        comments_list.append(text)
        #print("Comment by {}: {}".format(author, text))
        # Get the replies
        '''if 'replies' in item.keys():
            for reply in item['replies']['comments']:
                rauthor = reply['snippet']['authorDisplayName']
                rtext = reply["snippet"]["textDisplay"]
                print("\n\tReply by {}: {}".format(rauthor, rtext), "\n")'''

# Request with the API to get all comments infos. Max results can be modified.
def get_comment_thread(youtube, video_id, next_page_token):
    results = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        videoId=video_id,
        textFormat="plainText",
        pageToken=next_page_token
    ).execute()
    return results

# Initialize the list who will store all the comments.
comments_list = []

# First call to the API. Max results can be modified.
results = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        videoId=video_id,
        textFormat="plainText",
    ).execute()
next_page_token = results["nextPageToken"]
load_comments(results, comments_list)

# Next calls to the API with the next pages. Used to get all the comments
while next_page_token:

    match = get_comment_thread(youtube, video_id, next_page_token)
    print("nb of comments = ", len(comments_list))
    if "nextPageToken" in match :
        next_page_token = match["nextPageToken"]
    else :
        break
    load_comments(match, comments_list)

# Print the comments stored in the list.
for comment in comments_list :
    print(comment, "\n")
print("\n Number of comments =", len(comments_list))

# Write the comments in a file
with open("comments.txt", "w") as f :
    for item in comments_list :
        f.write("%s\n" % item)
f.close()
