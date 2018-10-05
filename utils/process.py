import csv
import sys
from nltk.tokenize import TweetTokenizer
from preprocess_twitter import tokenize

def read_glove(glove_filename):
    glovefile = open(glove_filename)
    vocab = set()
    for line in glovefile:
        word = line.split()[0]
        word = unicode(word, "utf-8")
        vocab.add(word)
    return vocab

def proc_file(in_filename, out_filename, glove_vocab):
    infile = open(in_filename)
    reader = csv.reader(infile, quotechar='"')
    outfile = open(out_filename, 'w')
    writer = csv.writer(outfile, quotechar='"')
    tumblr_vocab = set()
    tokenizer = TweetTokenizer()
    for i,line in enumerate(reader):
        if len(line) != 10:
            continue
        caption = tokenizer.tokenize(tokenize(line[8]))
        num_in = len([x for x in caption if x in glove_vocab])
        for word in caption:
            tumblr_vocab.add(word)
        if num_in * 2 > len(caption):
            writer.writerow(line)
    print "Tumblr vocab size:", len(tumblr_vocab)
    print "Overlap:", len(glove_vocab & tumblr_vocab)

def main():
    gloveprefix = "/projects/tir2/users/asrivats/embeddings/glove/"
    glove_filename = "glove.twitter.27B.200d.txt"
    vocab = read_glove(gloveprefix + glove_filename)
    print "GloVe vocab size:", len(vocab)
    prefix = "/projects/tir3/users/asrivats/multimodal/data/"
    in_filename = sys.argv[1]
    out_filename = sys.argv[2]
    proc_file(prefix + in_filename, prefix + out_filename, vocab)

if __name__ == "__main__":
    main()
