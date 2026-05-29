import pandas as pd
import bar_chart_race as bcr
import os
import urllib.request
import subprocess
import requests

# 1. DOWNLOAD REAL DATA (WORLD BANK API)
print("Downloading official data from World Bank API...")
url = "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?per_page=16000&format=json"
response = requests.get(url).json()

data_list = []
for item in response[1]:
    if item['countryvalue'] not in [
        'World', 'High income', 'Low & middle income', 'Low income', 
        'Lower middle income', 'Upper middle income', 'East Asia & Pacific', 
        'Europe & Central Asia', 'Latin America & Caribbean', 'Middle East & North Africa', 
        'North America', 'South Asia', 'Sub-Saharan Africa', 'IDA & IBRD total', 
        'Post-demographic dividend', 'OECD members', 'Early-demographic dividend'
    ]:
        data_list.append({
            'Country': item['countryvalue'],
            'Year': int(item['date']),
            'Population': item['value']
        })

df_raw = pd.DataFrame(data_list)
df = df_raw.pivot(index='Year', columns='Country', values='Population')
df = df.loc[1960:2024]
df = df.dropna(how='all', axis=1)

print("Data processing complete.")

# 2. DOWNLOAD COPYRIGHT-FREE MUSIC
audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
music_filename = "background_music.mp3"
video_no_audio = "race_no_audio.mp4"
final_video = "bar_chart_race.mp4"

print("Downloading background music...")
try:
    urllib.request.urlretrieve(audio_url, music_filename)
except Exception as e:
    print(f"Music download failed: {e}")

# 3. GENERATE VIDEO (5 MINUTES & TOP 10)
print("Generating Bar Chart Race video...")
bcr.bar_chart_race(
    df=df,
    filename=video_no_audio,
    orientation='h',
    sort='desc',
    n_bars=10,                # Top 10 countries
    fixed_max=False,
    steps_per_period=140,     # Slow transition for longer duration
    period_length=4600,       # Reaches approx. 5 minutes total
    title='Top 10 Most Populous Countries in the World (1960 - 2024)',
    interpolate_period=True
)

# 4. MERGE VIDEO AND AUDIO VIA FFMPEG
if os.path.exists(video_no_audio) and os.path.exists(music_filename):
    cmd = (
        f"ffmpeg -y -i {video_no_audio} -stream_loop -1 -i {music_filename} "
        f"-c:v copy -c:a aac -shortest {final_video}"
    )
    subprocess.run(cmd, shell=True)
    print(f"Success! Final video created: {final_video}")
else:
    if os.path.exists(video_no_audio):
        os.rename(video_no_audio, final_video)
