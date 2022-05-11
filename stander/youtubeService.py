import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import re

class YoutubeService:
    def __init__(self):
        #初始化
        scopes = ["https://www.googleapis.com/auth/youtube"]

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        # print(flow.authorization_url(prompt='consent'))
        credentials = flow.run_console()
        # 主要 youtube Service
        self.youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    def account_channal(self, channelID): # 頻道資訊
        request = self.youtube.channels().list(
            part = "snippet",
            id = channelID
        )
        response = request.execute()

        return response

    def account_creat_new_playlist(self, channelID, title): # 新增播放清單
        request = self.youtube.playlists().insert(
            part = "snippet",
            body = {
                "snippet": {
                    "title": title,
                    "channelId": channelID
                }
            }
        )
        response = request.execute()
        return response

    def get_playlist_response(self, playlistID): # 取得播放清單request
        request = self.youtube.playlistItems().list(
            part = "snippet",
            playlistId= playlistID ,
            maxResults = 50
        )
        response = request.execute()
        return response

    def playlist_show(self, playlistID): # 顯示播放清單內容
        response = self.get_playlist_response(playlistID)

        print("---------")
        for i in range(len(response['items'])):
            print(f'{i}:  {response["items"][i]["snippet"]["title"]}')
        print("---------")
        return response

    def playlist_insert_video(self, playlistID, videoID, index = -1): # 插入影片
        if index < 0: # 如果沒有選取插入 index 自動加在最尾端
            response = self.get_playlist_response(playlistID)
            index = len(response['items'])

        request = self.youtube.playlistItems().insert(
            part="snippet",
            body={
                'snippet': {
                    'playlistId': playlistID,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': videoID
                        },
                    'position': index
                }
            }
        )
        response = request.execute()
        # print(response)
        print(f'Add {response["snippet"]["title"]} to playlist')
        return response

    def playlist_delete_video(self, playlistID, videoIndex): # 刪除影片
        response = self.get_playlist_response(playlistID)
        if videoIndex >= len(response["items"]):
            print("index out of length!")
            return
        print(f'Delete the viod: {response["items"][videoIndex]["snippet"]["title"]}')
        request = self.youtube.playlistItems().delete(id = response['items'][videoIndex]['id'])
        response = request.execute()
        return response

    def playlist_search_video(self, playlistID, keyString): # 搜尋影片
        response = self.get_playlist_response(playlistID)

        findVideo = [] # 以找到的影片
        for i in range(len(response["items"])):
            # if keyString in response["items"][i]["snippet"]["title"]:
            # print(re.search(keyString, response["items"][i]["snippet"]["title"]))
            if re.search(keyString, response["items"][i]["snippet"]["title"]):
                findVideo.append(response["items"][i]["snippet"]["title"])
                print('find video\n-------')
                print(f'{i}:   {response["items"][i]["snippet"]["title"]}')
                print('-------')

        if not len(findVideo): # 沒有找到影片
            print(f'-------\nNot found video: {keyString}\n-------')
        else: # 找到影片
            print('\nfind video')
            print('-------')
            for i in range(len(findVideo)):
                print(f'{i}:   {findVideo[i]}')
            print('-------')
        return

    def playlist_move_video(self, playlistID, currentIndex, moveIndex): # 移動影片順序
        response = self.get_playlist_response(playlistID)

        listlength = len(response['items'])
        # 索引號錯誤
        if moveIndex >= listlength or moveIndex < 0 or currentIndex >= listlength or currentIndex < 0:
            print("Worng index")
            return response

        # 移動
        print(f'move {currentIndex} to {moveIndex}')
        if currentIndex < moveIndex:
            self.playlist_delete_video(playlistID, currentIndex)
            self.playlist_insert_video(playlistID, response['items'][currentIndex]['snippet']['resourceId']['videoId'], moveIndex)
        else:
            self.playlist_insert_video(playlistID, response['items'][currentIndex]['snippet']['resourceId']['videoId'], moveIndex)
            self.playlist_delete_video(playlistID, currentIndex+1)

        return response

    def playlist_mergeList(self, myplaylistID, sourcePlaylistID): # 合併播放清單
        mylistrespone = self.get_playlist_response(myplaylistID)
        sourcelistrespone = self.get_playlist_response(sourcePlaylistID)

        for item in sourcelistrespone['items']:
            self.playlist_insert_video(myplaylistID, item['snippet']['resourceId']['videoId'])

        print("-------\nmerge finish\n-------")
        return

    def playlist_modify_title(self, myPlaylistID, title):
        request = self.youtube.playlists().update(
            part = "snippet",
            body = {
                "id": myPlaylistID,
                "snippet": {
                    "title": title,
                }
            }
        )
        response = request.execute()
        return response

    def playlist_clear(self, playlistID):
        response = self.get_playlist_response(playlistID)
        for i in range(len(response['items'])):
            self.playlist_delete_video(playlistID, 0)
