import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 개인 정보 설정
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8000/callback"

# 접근 권한 설정
scope = 'playlist-modify-public playlist-modify-private'

# 인증
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

# 본인 user id
user_id = sp.current_user()['id']

# ▶️ 플레이리스트 제목 입력받기
playlist_name = input("🎵 새 플레이리스트 제목을 입력하세요: ")
playlist_description = "자동 생성된 추천 운동용 플레이리스트"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=playlist_description)

playlist_id = playlist['id']
print(f"✅ Created new playlist: {playlist_name} (ID: {playlist_id})")

# ▶️ 추천곡 리스트
track_names = [
    # 웨이트
    "Bring Me The Horizon - Can You Feel My Heart",
    "Papa Roach - Born for Greatness",
    "Nothing More - Go To War",
    "Falling In Reverse - Popular Monster",
    "Royal Blood - Typhoons",
    
    # 러닝
    "Fred again.. - Danielle (smile on my face)",
    "John Summit - Where You Are (feat. Hayla)",
    "MEDUZA - Lose Control",
    "Alok - Hear Me Now",
    "Jonas Blue - Mama",
    
    # K-pop
    "XG - LEFT RIGHT",
    "SEVENTEEN - HOT",
    "TAEMIN - Criminal",
    "ENHYPEN - Bite Me",
    "FIFTY FIFTY - Cupid",
    
    # 락
    "Paramore - This Is Why",
    "The Hives - Hate To Say I Told You So",
    "Franz Ferdinand - Take Me Out",
    "The Killers - When You Were Young",
    "Nothing But Thieves - Amsterdam",
    
    # Funk / Disco
    "Dua Lipa - Hallucinate",
    "Purple Disco Machine - Hypnotized",
    "Doja Cat - Say So",
    "Kylie Minogue - Padam Padam",
    "Oliver Heldens - Gecko (Overdrive)"
]

# ▶️ 플레이리스트에 이미 추가된 트랙들 가져오기 → 중복 방지용
existing_tracks = []
results = sp.playlist_tracks(playlist_id)
while results:
    existing_tracks += [item['track']['uri'] for item in results['items']]
    if results['next']:
        results = sp.next(results)
    else:
        results = None

# ▶️ 트랙 검색 + URI 수집 (중복 방지 적용)
track_uris_to_add = []
for track in track_names:
    result = sp.search(q=track, type='track', limit=1)
    if result['tracks']['items']:
        uri = result['tracks']['items'][0]['uri']
        if uri not in existing_tracks:
            track_uris_to_add.append(uri)
            print(f"🎵 Adding: {track} → {uri}")
        else:
            print(f"🔁 Skipping (already in playlist): {track}")
    else:
        print(f"⚠️ Track not found: {track}")

# ▶️ 최종 추가
if track_uris_to_add:
    sp.playlist_add_items(playlist_id, track_uris_to_add)
    print(f"\n✅ {len(track_uris_to_add)} tracks added to playlist '{playlist_name}'!")
else:
    print("\n⚠️ No new tracks were added (all were already in the playlist).")
