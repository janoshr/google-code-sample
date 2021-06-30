"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, playlist_name:str) -> None:
        self._name = playlist_name
        self._vidoes = []

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def videos(self) -> list:
        return self._vidoes
    
    def add_video(self, video):
        self._vidoes.append(video)

    def has_video(self, video):
        return video in self._vidoes

    def remove_video(self, video):
        self._vidoes.remove(video)
    
    def get_all_videos(self):
        return self._vidoes

    def clear_all(self):
        self._vidoes.clear()
