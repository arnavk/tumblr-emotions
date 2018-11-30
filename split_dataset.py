import re
import csv
import random

emotion_map = {
	'angry': set(),
	'bored': set(),
	'calm': set(),
	'excited': set(),
	'happy': set(),
	'love': set(),
	'sad': set(),
}
# titles = ",id,post_url,date,liked,type,timestamp,tags,photo,caption,search_query,img_file_name"
with open('data/train_set.csv', 'w+') as train_file:
	train_writer = csv.writer(train_file, delimiter=',')
	with open('data/test_set.csv', 'w+') as test_file:
		test_writer = csv.writer(test_file, delimiter=',')
		with open('data/val_set.csv', 'w+') as val_file:
			val_writer = csv.writer(val_file, delimiter=',')

			with open('data/dataset.csv') as f:
				reader = csv.reader(f)
				for line in reader:
					emotion = line[-2]
					post_id = line[1]
					if len(emotion_map[emotion]) < 12000:
						train_writer.writerow(line)
						emotion_map[emotion].add(post_id)
					elif len(emotion_map[emotion]) < 14000:
						test_writer.writerow(line)
						emotion_map[emotion].add(post_id)
					else:
						val_writer.writerow(line)
						emotion_map[emotion].add(post_id)
