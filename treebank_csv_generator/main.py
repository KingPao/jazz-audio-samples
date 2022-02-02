import json
import csv


def create_csv(data):
    with open('treebank_csv_new.csv', 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)

        writer.writerow(
            ["title", "key", "style", "tempo", "checked", "audio_produced", "chords", "marked_", "composers"])

        for i in range(len(data)):
            temp = [
                data[i]['title'],
                data[i]['key'],
                "",
                "",
                "",
                "",
                ", ".join(data[i]['chords']),
                measures_to_chords(data[i]['chords'], data[i]['measures'], data[i]['beats']),
                data[i]['composers']
            ]

            writer.writerow(temp)
    print("File generated")


def measures_to_chords(chords, measures, beats):
    measure_chords = []
    curr_m = 0
    curr_b = 1

    for m, c, b in zip(measures, chords, beats):
        if curr_m == m:
            if (b - curr_b) == 1:
                measure_chords.append("&" + str(c))
            elif (b - curr_b) == 2:
                measure_chords.append(" " + str(c))
        else:
            measure_chords.append("|" + str(c))
        curr_m = m
        curr_b = b

    return "".join(measure_chords) + "|"


def count_chords(data):
    with open('chords_count.csv', 'w', newline='', encoding='UTF8') as f:
        chord_dict = {}
        plain_chords = []

        for i in range(len(data)):
            chord_line = data[i]['chords']

            for chord in chord_line:
                plain_chords.append(chord)

        keys = set(plain_chords)
        for key in keys:
            occ = plain_chords.count(key)
            chord_dict[key] = occ

        writer = csv.DictWriter(f, chord_dict.keys())
        writer.writeheader()
        writer.writerow(chord_dict)


if __name__ == '__main__':
    with open("treebank.json", "r") as file:
        treebank = json.load(file)

        create_csv(treebank)
        count_chords(treebank)
