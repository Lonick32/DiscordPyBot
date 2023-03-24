import spotipy
from spotipy.oauth2 import SpotifyOAuth
import interactions

client_id = 'Your client_id'
client_secret = 'Your client_secret'
redirect_uri = 'http://localhost:8888/callback'

bot = interactions.Client(token="Your Discord Bot Token")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,redirect_uri=redirect_uri, scope="user-read-currently-playing user-read-playback-state user-modify-playback-state user-read-recently-played user-top-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-library-modify user-library-read user-follow-modify user-follow-read app-remote-control streaming user-read-email user-read-private"))

@bot.command(name="search", description="Search for a track on Spotify", options=[interactions.Option(type=interactions.OptionType.STRING, name = "query", description="The track to search for", required=True)])

async def search(ctx: interactions.CommandContext, query: str):
    
    result = sp.search(query, limit=1, type="track")
    track = result["tracks"]["items"][0]
    name = track["name"]
    artists = ", ".join([artist["name"] for artist in track["artists"]])
    url = track["external_urls"]["spotify"]
    await ctx.send(f"{name} by {artists} ({url})")

@bot.command(name="related", description="Search for similar artists on Spotify", options=[interactions.Option(type=interactions.OptionType.STRING, name = "query", description="Search for similar artists", required=True)])

async def related(ctx: interactions.CommandContext, query: str):
    results = sp.search(q=query, type='artist')
    artist = results['artists']['items'][0]
    related_artists = sp.artist_related_artists(artist['id'])
    response = f'Related artists for {artist["name"]}:'
    for related_artist in related_artists['artists']:
        response += f'\n- {related_artist["name"]}'
    await ctx.send(response)

bot.start()