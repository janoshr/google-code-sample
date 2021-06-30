"""A video player class."""
import operator
import random
import re
from src.video_playlist import Playlist
from .video_library import VideoLibrary


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._current_video = None
        self._paused = False
        self._playlists = dict({})

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        videos = self._video_library.get_all_videos()
        for video in (sorted(videos, key=operator.attrgetter('title'))):
            print("{0} ({1}) [{2}] {3}".format(
                video.title,
                video.video_id,
                ' '.join(video.tags),
                ("- FLAGGED (reason: " + video.flag_reason + ")") if video.flagged else ""
            ))

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if (not video):
            print("Cannot play video: Video does not exist")
        elif (video.flagged):
            print("Cannot play video: Video is currently flagged (reason: {})".format(video.flag_reason))
        else:
            self.play(video)

    def stop_video(self):
        """Stops the current video."""
        if (self._current_video):
            print("Stopping video: {}".format(self._current_video.title))
            self._current_video = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        allowed_list = []
        for video in self._video_library.get_all_videos():
            if (not video.flagged):
                allowed_list.append(video)
        if (len(allowed_list) == 0):
            print("No videos available")
            return
        
        video = random.choice(allowed_list)
        if (video.flagged):
            print("Cannot play video: Video is currently flagged (reason: {})".format(video.flag_reason))
        else:
            self.play(video)

    def pause_video(self):
        """Pauses the current video."""
        if (self._paused):
            print("Video already paused: {}".format(self._current_video.title))
        elif (not self._current_video):
            print("Cannot pause video: No video is currently playing")
        else:
            self._paused = True
            print("Pausing video: {}".format(self._current_video.title))

    def continue_video(self):
        """Resumes playing the current video."""
        if (not self._current_video):
            print("Cannot continue video: No video is currently playing")
        elif (not self._paused):
            print("Cannot continue video: Video is not paused")
        else:
            self._paused = False
            print("Continuing video: {}".format(self._current_video.title))

    def show_playing(self):
        """Displays video currently playing."""
        if (not self._current_video):
            print("No video is currently playing")
        else:
            video = self._current_video
            print("Currently playing: {0} ({1}) [{2}] {3}".format(
                video.title,
                video.video_id,
                " ".join(video.tags),
                "- PAUSED" if self._paused else ""
            ))

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if (playlist_name.upper() not in self._playlists.keys()):
            self._playlists[playlist_name.upper()] = Playlist(playlist_name)
            print("Successfully created new playlist: {}".format(playlist_name))
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if (playlist_name.upper() not in self._playlists.keys()):
            print("Cannot add video to {}: Playlist does not exist".format(playlist_name))
            return
        playlist = self._playlists[playlist_name.upper()]
        video = self._video_library.get_video(video_id)
        if (not video):
            print("Cannot add video to {}: Video does not exist".format(playlist_name))
        elif (video.flagged):
            print("Cannot add video to {0}: Video is currently flagged (reason: {1})".format(playlist_name, video.flag_reason))
        elif (playlist.has_video(video_id)):
            print("Cannot add video to {}: Video already added".format(playlist_name))
        else:
            playlist.add_video(video.video_id)
            print("Added video to {0}: {1}".format(playlist_name, video.title))

    def show_all_playlists(self):
        """Display all playlists."""
        if (len(self._playlists) == 0):
            print("No playlists exist yet")
            return
        print("Showing all playlists:")
        for playlist in (sorted(self._playlists.values(), key=operator.attrgetter("name"))):
            print(playlist.name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if (playlist_name.upper() not in self._playlists.keys()):
            print("Cannot show playlist {}: Playlist does not exist".format(playlist_name))
            return
        playlist = self._playlists.get(playlist_name.upper())
        print("Showing playlist:",playlist_name)
        if (len(playlist.get_all_videos()) == 0):
            print("No videos here yet")
        for video_id in playlist.get_all_videos():
            video = self._video_library.get_video(video_id)
            print("{0} ({1}) [{2}] {3}".format(
                video.title,
                video.video_id,
                ' '.join(video.tags),
                ("- FLAGGED (reason: " + video.flag_reason + ")") if video.flagged else ""
            ))

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if (playlist_name.upper() not in self._playlists.keys()):
            print("Cannot remove video from {}: Playlist does not exist".format(playlist_name))
            return
        video = self._video_library.get_video(video_id)
        playlist = self._playlists.get(playlist_name.upper())
        if (not video):
            print("Cannot remove video from {}: Video does not exist".format(playlist_name))
            return
        elif (not playlist.has_video(video_id)):
            print("Cannot remove video from {}: Video is not in playlist".format(playlist_name))
            return
        playlist.remove_video(video_id)
        print("Removed video from {0}: {1}".format(playlist_name, video.title))

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if (playlist_name.upper() not in self._playlists.keys()):
            print("Cannot clear playlist {}: Playlist does not exist".format(playlist_name))
            return
        playlist = self._playlists.get(playlist_name.upper())
        playlist.clear_all()
        print("Successfully removed all videos from {}".format(playlist_name))

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if (playlist_name.upper() not in self._playlists.keys()):
            print("Cannot delete playlist {}: Playlist does not exist".format(playlist_name))
            return
        del self._playlists[playlist_name.upper()]
        print("Deleted playlist: {}".format(playlist_name))

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self._video_library.get_all_videos()
        result_list = []
        for video in videos:
            if re.search(search_term,video.title, re.IGNORECASE) and not video.flagged:
                result_list.append(video)
        if (len(result_list) == 0):
            print("No search results for {}".format(search_term))
            return
        print("Here are the results for {}:".format(search_term))
        for i, item in enumerate(sorted(result_list, key=operator.attrgetter('title'))):
            print("{0}) {1} ({2}) [{3}]".format((i+1),item.title, item.video_id, ' '.join(item.tags)))
        print("Would you like to play any of the above? If yes, "
            "specify the number of the video.")
        print("If your answer is not a valid number, we will assume "
               "it's a no.")
        try:
            answer = int(input())
            if answer <= len(result_list):
                result = result_list[answer-1]
                self._current_video = result
                print("Playing video: {}".format(result.title))
        except ValueError:
            return

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = self._video_library.get_all_videos()
        result_list = []
        for video in videos:
            if (video_tag in video.tags and not video.flagged):
                result_list.append(video)
        if (len(result_list) == 0):
            print("No search results for {}".format(video_tag))
            return
        print("Here are the results for {}:".format(video_tag))
        for i, item in enumerate(sorted(result_list, key=operator.attrgetter('title'))):
            print("{0}) {1} ({2}) [{3}]".format((i+1),item.title, item.video_id, ' '.join(item.tags)))
        print("Would you like to play any of the above? If yes, "
            "specify the number of the video.")
        print("If your answer is not a valid number, we will assume "
               "it's a no.")
        try:
            answer = int(input())
            if answer <= len(result_list):
                result = result_list[answer-1]
                self._current_video = result
                print("Playing video: {}".format(result.title))
        except ValueError:
            return

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id) 
        if (not video):
            print("Cannot flag video: Video does not exist")
            return
        elif (video.flagged):
            print("Cannot flag video: Video is already flagged")
            return
        if (flag_reason == ""):
            flag_reason = "Not supplied"
        if (self._current_video == video):
            print("Stopping video: {}".format(video.title))
            self._current_video = None
            self._paused = False
        self._video_library.flag_video(video_id,flag_reason)
        print("Successfully flagged video: {0} (reason: {1})".format(video.title, flag_reason))

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if (not video):
            print("Cannot remove flag from video: Video does not exist")
            return
        elif (not video.flagged):
            print("Cannot remove flag from video: Video is not flagged")
            return
        
        self._video_library.unflag_video(video_id)
        print("Successfully removed flag from video: {}".format(video.title))

    def play(self, video):
        if (self._current_video):
            print("Stopping video: {}".format(self._current_video.title))
        self._current_video = video
        self._paused = False
        print("Playing video: {}".format(video.title))