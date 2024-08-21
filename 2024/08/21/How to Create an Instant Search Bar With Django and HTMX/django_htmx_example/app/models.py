import csv

from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=100)
    performer = models.CharField(max_length=100)
    chart_debut = models.CharField(max_length=500)
    peak_position = models.IntegerField()
    time_on_chart = models.IntegerField()

# You can run this function in the django shell after creating the database
def load_data():
    # You can download the CSV from the following link.
    # https://github.com/HipsterVizNinja/random-data/tree/main/Music/hot-100
    song_data = {}
    with open("data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row["song"], row["performer"]) not in song_data:
                song_data[(row["song"], row["performer"])] = {
                    "chart_debut": row["chart_debut"],
                    "peak_position": int(row["peak_position"]),
                    "time_on_chart": int(row["time_on_chart"])
                }
            else:
                song_data[(row["song"], row["performer"])]["peak_position"] = min(song_data[(row["song"], row["performer"])]["peak_position"], int(row["peak_position"]))
                song_data[(row["song"], row["performer"])]["time_on_chart"] = max(song_data[(row["song"], row["performer"])]["time_on_chart"], int(row["time_on_chart"]))

    for s in song_data:
        Song.objects.create(
            title=s[0], 
            performer=s[1], 
            chart_debut=song_data[s]["chart_debut"], 
            peak_position=song_data[s]["peak_position"], 
            time_on_chart=song_data[s]["time_on_chart"]
        )