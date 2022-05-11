from youtubeService import YoutubeService
import re

# https://www.youtube.com/channel/UCiFRmRKUf8yepwXD9R5m4uA
# https://www.youtube.com/playlist?list=PL94KgMwB4qGj8Tlu_hVY0e9eyaNnmysH1
def main():
    yt = YoutubeService()
    myChannelID = ""
    myplaylistID = ""
    s = input("input playlist link: ")

    s = "https://www.youtube.com/playlist?list=PL94KgMwB4qGj8Tlu_hVY0e9eyaNnmysH1"

    s = s.split('=')
    print(s)
    myplaylistID = s[1]
    print(myplaylistID)
    s = input("input channel link: ")

    s = "https://www.youtube.com/channel/UCiFRmRKUf8yepwXD9R5m4uA"

    s = s.split('channel/')
    myChannelID = s[1]
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
