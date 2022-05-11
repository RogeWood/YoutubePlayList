from youtubeService import YoutubeService
import re
import json
# https://www.youtube.com/channel/UCiFRmRKUf8yepwXD9R5m4uA
# https://www.youtube.com/playlist?list=PL94KgMwB4qGj8Tlu_hVY0e9eyaNnmysH1
def main():
    # yt = YoutubeService()
    with open('listlink.json', newline='') as jsonfile:
        data = json.load(jsonfile)

    myChannelID = data["channel"].split('channel/')[1]
    myplaylistID = data["playlist"].split('=')[1]
    print(myplaylistID)
    print(myChannelID)


    running = True
    while running:
        s = input("input command: ")

        if re.search("add video", s):
            s = input("input video link: ")
            if re.search("youtu.be", s):
                s = s.split('youtu.be/')
            elif re.search("=", s):
                s = s.split('=')
            else:
                print("invalid link")
                continue
            id = s[1]
            yt.playlist_insert_video(myplaylistID, id)

        elif re.search("delete video", s):
            s = input("input video index: ")
            if s.isdigit():
                index = int(s)
            else:
                print("wrong index!!!")
            yt.playlist_delete_video(myplaylistID, index)

        elif re.search("show playlist", s):
            yt.playlist_show(myplaylistID)

        elif re.search("search video", s):
            s = input("input the key: ")
            yt.playlist_search_video(myplaylistID, s)

        elif re.search("add new playlist", s):
            s = input("input playlist name: ")
            response = yt.account_creat_new_playlist(myChannelID, s)
            print(f'playlist link: https://www.youtube.com/playlist?list={response["id"]}')

if __name__ == '__main__':
    main()
