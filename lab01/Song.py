class Song:
    """Class for representing information about a song"""
    def __init__(self, title, artist, album):
        self.title = title
        self.artist = artist
        self.album = album

    def output(self):
        print('Title: "{0}"').format(self.title)
        print('Artist: {0}').format(self.artist)
        print('Album: {0}\n').format(self.album)

if __name__ == "__main__":
    songs = []
    songs.append(Song("Between Two Points", "The Glitch Mob", "Drink the Sea"))
    songs.append(Song("Ghosts 'n' Stuff (Sub Focus Remix)", "Deadmau5", "Ghosts Album"))
    songs.append(Song("All the Cash", "Evil Nine", "All the Cash (Single)"))

    for song in songs: song.output()