import pandas as pd
import bar_chart_race as bcr
import os

# 1. Diyaarinta Xogta (Dataset)
# Tusaale: Waxaan halkan ku samaynaynaa xog kooban. 
# Waad bedeli kartaa adoo ka keenaya API ama URL kale oo xog nooceeda ah laga helo.
data = {
    'Dates': ['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04'],
    'Somalia': [10, 15, 30, 45],
    'Kenya': [20, 22, 25, 28],
    'Ethiopia': [15, 25, 28, 50],
    'Djibouti': [5, 12, 18, 22]
}

df = pd.DataFrame(data)
df.set_index('Dates', inplace=True)

# 2. Samaynta Bar Chart Race Video
output_filename = 'bar_chart_race.mp4'

print("Guda galka samaynta muqaalka...")
bcr.bar_chart_race(
    df=df,
    filename=output_filename,
    orientation='h',
    sort='desc',
    n_bars=4,
    fixed_max=True,
    steps_per_period=10,
    period_length=500,
    title='Kobac Bilowga Sanadka 2026 (Tusaale)'
)
print(f"Muqaalka waa la diyaariyay: {output_filename}")
