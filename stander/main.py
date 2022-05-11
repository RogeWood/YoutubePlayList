from youtubeService import YoutubeService
import re
import json

def main():
    yt = YoutubeService()
    with open('listlink.json', newline='') as jsonfile:
        data = json.load(jsonfile)

    myChannelID = data["channel"].split('channel/')[1]
    plIDs = []
    for i in data["playlists"]:
        plIDs.append(i.split('=')[1])

    for i in range(len(plIDs)):
        print(i, plIDs[i])
    myplaylistID = plIDs[int(input("Input playlist index: "))]
    print("channel: ", myChannelID)
    print("main playlist: ", myplaylistID)


    running = True
    while running:
        s = input("input command: ")

        if re.search("add v", s): #新增
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

        elif re.search("delete v", s): # 刪除
            s = input("input video index: ")
            if s.isdigit():
                index = int(s)
            else:
                print("wrong index!!!")
            yt.playlist_delete_video(myplaylistID, index)

        elif re.search("show pl", s): # 顯示
            yt.playlist_show(myplaylistID)

        elif re.search("search v", s): # 搜尋
            s = input("input the key: ")
            yt.playlist_search_video(myplaylistID, s)

        elif re.search("add new pl", s): #新增播放清單
            s = input("input playlist name: ")
            response = yt.account_creat_new_playlist(myChannelID, s)
            plIDs.append(response["id"])
            print(f'playlist link: https://www.youtube.com/playlist?list={response["id"]}')

        elif re.search("clear pl", s):
            response = yt.playlist_clear(myplaylistID)
            print("\nclear complete\n")

        elif re.search("merge pl", s):
            for i in range(len(plIDs)):
                print(i, plIDs[i])
            s = int(input("Input source playlist index: "))
            response = yt.playlist_mergeList(myplaylistID, plIDs[s])
        elif re.search("move v", s):
            c = int(input("Input current video index: "))
            t = int(input("Input target video index: "))
            response = yt.playlist_move_video(myplaylistID, c, t)
        elif re.search("change pl name", s):
            s = input("Input new name: ")
            response = yt.playlist_modify_title(myplaylistID, s)
            print("change finish")

        elif re.search("change main pl", s):
            for i in range(len(plIDs)):
                print(i, plIDs[i])
            myplaylistID = plIDs[int(input("Input playlist index: "))]
if __name__ == '__main__':
    main()
