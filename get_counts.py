import csv

emotion_map = {
	'angry': 0,
	'bored': 0,
	'calm': 0,
	'excited': 0,
	'happy': 0,
	'love': 0,
	'sad': 0,
}
post_map = {}
titles = ',id,post_url,date,liked,type,timestamp,tags,photo,caption,search_query,img_file_name'
with open('data/shuffled_train.csv') as f:
	reader = csv.reader(f)
	skip = True
	for line in reader:
		if skip:
			skip = False
			continue
		post_map[line[1]] = line[-2]

with open('data/shuffled_test.csv') as f:
	reader = csv.reader(f)
	skip = True
	for line in reader:
		if skip:
			skip = False
			continue
		post_map[line[1]] = line[-2]

with open('combined.csv') as f:
	reader = csv.reader(f)
	for line in reader:
		if line[0] not in post_map:
			print line[0]
			continue
		if float(line[1]) > 0.99 and int(line[2]) == 1:
			emotion_map[post_map[line[0]]] += 1
print emotion_map
