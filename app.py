import pandas as pd
import bar_chart_race as bcr
import os
import urllib.request
import subprocess
import requests

# 1. DOWNLOAD REAL DATA (WORLD BANK API WITH CORRECT KEYS)
print("Downloading official data from World Bank API...")
url = "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?per_page=16000&format=json"
response = requests.get(url).json()

data_list = []
# response[1] dhexdiisa waxaa ku jira liiska wadamada iyo xogta dadka
for item in response[1]:
    # Hubi in shay kasta uu leeyahay xogta wadanka iyo dadka si aysan cillo u imaan
    if item.get('country') and item.get('value') is not None:
        country_name = item['country']['value']
        
        # Ka saar gobolada guud si ay wadamada dhabta ah oo kaliya u haraan
        if country_name not in [
            'World', 'High income', 'Low & middle income', 'Low income', 
            'Lower middle income', 'Upper middle income', 'East Asia & Pacific', 
            'Europe & Central Asia', 'Latin America & Caribbean', 'Middle East & North Africa', 
            'North America', 'South Asia', 'Sub-Saharan Africa', 'IDA & IBRD total', 
            'Post-demographic dividend', 'OECD members', 'Early-demographic dividend',
            'East Asia & Pacific (excluding high income)', 'Europe & Central Asia (excluding high income)',
            'Latin America & Caribbean (excluding high income)', 'Middle East & North Africa (excluding high income)',
            'Sub-Saharan Africa (excluding high income)', 'IBRD only', 'IDA total', 'IDA blend', 'IDA only'
        ]:
            data_list.append({
                'Country': country_name,
                'Year': int(item['date']),
                'Population': item['value']
            })

# U beddel DataFrame
df_raw = pd.DataFrame(data_list)

# Habayn shaxda (Pivoting): Sanadaha -> Index, Wadamada -> Columns
df = df_raw.pivot(index='Year', columns='Country', values='Population')

# Kala shaandhee sanadaha (1960 ilaa 2024 oo ah xogta ugu dambaysay ee dhammaystiran)
df = df.loc[1960:2024]
df = df.dropna(how='all', axis=1)

print("Data processing complete successfully!")

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
print("Generating Bar Chart Race video (Top 10)...")
bcr.bar_chart_race(
    df=df,
    filename=video_no_audio,
    orientation='h',
    sort='desc',
    n_bars=10,                # Mar walba Top 10-ka u sareeya
    fixed_max=False,
    steps_per_period=140,     # Transition degan si loo gaaro 5 Daqiiqo
    period_length=4600,       # Dhererka guud ee muqaalka oo 5 daqiiqo ku dhow
    title='Top 10 Most Populous Countries in the World (1960 - 2024)',
    interpolate_period=True
)

# 4. MERGE VIDEO AND AUDIO VIA FFMPEG
if os.path.exists(video_no_audio) and os.path.exists(music_filename):
    print("Merging video and background music...")
    cmd = (
        f"ffmpeg -y -i {video_no_audio} -stream_loop -1 -i {music_filename} "
        f"-c:v copy -c:a aac -shortest {final_video}"
    )
    subprocess.run(cmd, shell=True)
    print(f"Success! Final video created: {final_video}")
else:
    if os.path.exists(video_no_audio):
        os.rename(video_no_audio, final_video)
        print("Video generated without audio.")
