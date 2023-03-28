import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Video():
    """
    Класс Видео на ютуб канале
    """
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, video_id):
        self.__video_id = video_id
        self.title = None
        self.url = None
        self.view_count = None
        self.like_count = None
        try:
            self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=self.__video_id).execute()
            self.video = self.youtube.channels().list(id=self.__video_id, part='snippet,statistics').execute()
            items = self.video_response.get('items', [])
            if items:
                self.title: str = self.video_response['items'][0]['snippet']['title']
                self.url = f"https://youtu.be/{self.__video_id}"
                self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
                self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
            #print(self.video_response['items'])
        except HttpError as e:
            print(f'An error occurred: {e}')

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)  # вызываем метод базового класса
        self.playlist_id = playlist_id

    def __str__(self):
        return f"{self.title}"