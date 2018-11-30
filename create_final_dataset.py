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
post_map = {}
MAX_COUNT = 16000
titles = ",id,post_url,date,liked,type,timestamp,tags,photo,caption,search_query,img_file_name"
with open('data/shuffled_train.csv') as f:
	reader = csv.reader(f)
	skip = True
	for line in reader:
		if skip:
			skip = False
			continue
		post_map[line[1]] = line[-2]

count = 0
emotions = list(emotion_map.keys())
emotion_regex = re.compile('|'.join(map(re.escape, ['#' + emotion for emotion in emotions])))
with open('data/shuffled_test.csv') as f:
	reader = csv.reader(f)
	skip = True
	for line in reader:
		if skip:
			skip = False
			continue
		post_map[line[1]] = line[-2]
		caption = line[-3]
		paragraph = emotion_regex.sub('', caption.lower())

		if line[-2] in paragraph:
			count += 1

with open('shuffled_dataset_softmaxes.csv') as f:
	reader = csv.reader(f)
	for line in reader:
		if line[0] not in post_map:
			print line[0]
			continue
		if float(line[1]) > 0.90 and int(line[2]) == 1:
			emotion_map[post_map[line[0]]].add(line[0])

train_map = {
	'angry': set(),
	'bored': set(),
	'calm': set(),
	'excited': set(),
	'happy': set(),
	'love': set(),
	'sad': set(),
}

validation_map = {
	'angry': set(),
	'bored': set(),
	'calm': set(),
	'excited': set(),
	'happy': set(),
	'love': set(),
	'sad': set(),
}

test_map = {
	'angry': set(),
	'bored': set(),
	'calm': set(),
	'excited': set(),
	'happy': set(),
	'love': set(),
	'sad': set(),
}

for k, v in emotion_map.iteritems():
	emotion_map[k] = list(v)
	random.shuffle(emotion_map[k])
	emotion_map[k] = emotion_map[k][:MAX_COUNT]
	for i in range(12000):
		train_map[k].add(emotion_map[k][i])
	for i in range(12000, 14000):
		test_map[k].add(emotion_map[k][i])
	for i in range(14000, 16000):
		validation_map[k].add(emotion_map[k][i])

for k, v in emotion_map.iteritems():
	print k, len(v)

for k, v in train_map.iteritems():
	print k, len(v)

for k, v in validation_map.iteritems():
	print k, len(v)

for k, v in test_map.iteritems():
	print k, len(v)


written1 = set()
written = set()
print 'writing full'
with open('data/dataset_.csv', 'w+') as file:
	writer = csv.writer(file, delimiter=',')
	for filename in ['data/shuffled_test.csv', 'data/shuffled_train.csv']:
		with open(filename) as f:
			reader = csv.reader(f)
			skip = True
			for line in reader:
				if skip:
					skip = False
					continue

				post_id = line[1]
				emotion = line[-2]
				if post_id in emotion_map[emotion] and post_id not in written1:
					written1.add(post_id)
					writer.writerow(line)

print 'writing train', len(written)
with open('data/dataset_train.csv', 'w+') as file:
	writer = csv.writer(file, delimiter=',')
	for filename in ['data/shuffled_test.csv', 'data/shuffled_train.csv']:
		with open(filename) as f:
			reader = csv.reader(f)
			skip = True
			for line in reader:
				if skip:
					skip = False
					continue

				post_id = line[1]
				emotion = line[-2]
				if post_id in train_map[emotion] and post_id not in written:
					written.add(post_id)
					writer.writerow(line)


print 'writing test', len(written)
with open('data/dataset_test.csv', 'w+') as file:
	writer = csv.writer(file, delimiter=',')
	for filename in ['data/shuffled_test.csv', 'data/shuffled_train.csv']:
		with open(filename) as f:
			reader = csv.reader(f)
			skip = True
			for line in reader:
				if skip:
					skip = False
					continue

				post_id = line[1]
				emotion = line[-2]
				if post_id in test_map[emotion] and post_id not in written:
					written.add(post_id)
					writer.writerow(line)

print 'writing val', len(written)
with open('data/dataset_val.csv', 'w+') as file:
	writer = csv.writer(file, delimiter=',')
	for filename in ['data/shuffled_test.csv', 'data/shuffled_train.csv']:
		with open(filename) as f:
			reader = csv.reader(f)
			skip = True
			for line in reader:
				if skip:
					skip = False
					continue

				post_id = line[1]
				emotion = line[-2]
				if post_id in validation_map[emotion] and post_id not in written:
					written.add(post_id)
					writer.writerow(line)
