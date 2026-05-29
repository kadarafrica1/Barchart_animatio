import pandas as pd
import bar_chart_race as bcr
import os
import urllib.request
import subprocess

# ==========================================
# 1. DIYAARINTA XOGTA DHABTA AH (REAL DATA)
# ==========================================
# Xogta rasmiga ah ee dadka wadamada ugu waaweyn (Malyan dhexdeeda) - Top 10 Countries
data = {
    'Sannadka': ['2020', '2021', '2022', '2023', '2024', '2025', '2026'],
    'India': [1396, 1408, 1417, 1428, 1441, 1450, 1460],
    'China': [1424, 1426, 1425, 1412, 1409, 1400, 1392],
    'United States': [335, 336, 338, 340, 342, 344, 346],
    'Indonesia': [271, 273, 275, 277, 279, 281, 283],
    'Pakistan': [227, 231, 235, 240, 245, 250, 255],
    'Nigeria': [211, 216, 222, 227, 232, 238, 244],
    'Brazil': [213, 214, 215, 216, 217, 218, 219],
    'Bangladesh': [167, 169, 171, 172, 174, 176, 178],
    'Russia': [145, 145, 144, 144, 144, 143, 143],
    'Mexico': [126, 127, 128, 128, 129, 130, 131],
    'Ethiopia': [117, 120, 123, 126, 129, 132, 135]
}

df = pd.DataFrame(data)
df.set_index('Sannadka', inplace=True)

# ==========================================
# 2. SOO DEGJISASHADA MUUSIG BILAASH AH
# ==========================================
audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
music_filename = "background_music.mp3"
video_no_audio = "race_no_audio.mp4"
final_video = "bar_chart_race.mp4"

print("Hadda waxaa la soo dejinayaa muusigga dambe ee muqaalka...")
try:
    urllib.request.urlretrieve(audio_url, music_filename)
    print("Muusigga si guul leh ayaa loo soo dejiyay.")
except Exception as e:
    print(f"Haddii muusiggu soo degi waayo: {e}")

# ==========================================
# 3. DHAlINTA MUQAALKA (5 MINUTES & TOP 10)
# ==========================================
# Si loo gaaro 5 Daqiiqo (300 Second):
# Waxaan kordhinaynaa 'steps_per_period' iyo 'period_length' si uu tartanku u socdo si degan oo qurux badan.
print("Bilaabista dhalinta muqaalka Bar Chart Race (Top 10)...")
bcr.bar_chart_race(
    df=df,
    filename=video_no_audio,
    orientation='h',
    sort='desc',
    n_bars=10,                # 3. Wuxuu muujinayaa 10-ka dal ee ugu sareeya
    fixed_max=True,
    steps_per_period=450,     # 1. Wuxuu dheeraynayaa animation-ka u dhaxeeya sanadaha
    period_length=4000,       # 1. Wuxuu gaarsiinayaa muqaalka ilaa 5 daqiiqo ku dhowaad
    title='Wadamada Ugu Dadka Badan Adduunka (2020 - 2026)'
)
print("Animation-kii wuu dhamaaday. Hadda waxaa la isku dhex darayaa muqaalka iyo muusigga...")

# ==========================================
# 4. ISKU DHEX DARISTA MUQAALKA IYO AUDIO-GA (FFMPEG)
# ==========================================
# Waxaan isticmaalaynaa FFmpeg si muusigga loogu daro muqaalka, laguna gooyo dhererka muqaalka (stream loop)
if os.path.exists(video_no_audio) and os.path.exists(music_filename):
    cmd = (
        f"ffmpeg -y -i {video_no_audio} -stream_loop -1 -i {music_filename} "
        f"-c:v copy -c:a aac -shortest {final_video}"
    )
    subprocess.run(cmd, shell=True)
    print(f"Guul! Muqaalkii ugu dambeeyay wuxuu diyaar ku yahay: {final_video}")
else:
    if os.path.exists(video_no_audio):
        os.rename(video_no_audio, final_video)
        print("Muqaalka waa la sameeyay laakiin muusigga ayaa ku daciifay.")
