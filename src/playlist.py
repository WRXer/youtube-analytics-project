import os
from googleapiclient.discovery import build
from src.video import Video

from datetime import timedelta, datetime
import isodate


class PlayList:
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.playlist_info = self.youtube.playlists().list(id=self.__playlist_id, part='contentDetails,snippet', maxResults=50,).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.__playlist_id, part='contentDetails', maxResults=50, ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)).execute()

    @property
    def total_duration(self):
        """
        Функция возвращает общую продолжительность всех видео
        """
        total_duration = timedelta(0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration_str = isodate.parse_duration(iso_8601_duration)
            total_duration += duration_str
        return total_duration

    def show_best_video(self):
        """
        Функция возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        top_likes = 0
        for video in self.video_response['items']:
            video_likes = int(video['statistics']['likeCount'])
            if video_likes > top_likes:
                top_likes = video_likes
                best_video_id = video['id']
        return f"https://youtu.be/{best_video_id}"