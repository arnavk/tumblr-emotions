import io
import os
import sys

import pandas as pd
import tensorflow as tf

from PIL import Image
from urllib.request import urlopen
from text_model.text_preprocessing import preprocess_one_df
from text_model.text_preprocessing import _load_embedding_weights_glove, _load_embedding_weights_word2vec

# Number of words in a post
_POST_SIZE = 50

def download_im(search_query, start, end, dataset_dir, subdir='photos'):
    """Download images using the urls in the dataframe specified by the search query.

    Parameters:
        search_query: A string giving the sentiment to load the corresponding dataframe.
        start: A start index for the loaded dataframe.
        end: An end index for the loaded dataframe.
        dataset_dir: A directory where the dataframes are stored.
        subdir: A subdirectory to store the photos.

    Returns:
        Images downloaded in the directory dataset_dir/subdir/search_query, having 
        the posts ids as names.
    """
    # Load data
    print("Attempting to scrape", search_query, "and save in", dataset_dir)
    sys.stdout.flush()
    df = pd.read_csv(os.path.join(dataset_dir, search_query + '.csv'), encoding='utf-8')
    links = df['photo']
    queries = df['search_query']
    ids = df['id']
    # Create subdir if it doesn't exist
    subdir = "dump_images"
    if not tf.gfile.Exists(os.path.join(dataset_dir, subdir)):
        tf.gfile.MakeDirs(os.path.join(dataset_dir, subdir))
    '''
    # Create search_query folder if it doesn't exist
    photos_dir = os.path.join(dataset_dir, subdir, search_query)
    if not tf.gfile.Exists(photos_dir):
        tf.gfile.MakeDirs(photos_dir)
    '''
    print("Attempting to scrape", df.shape[0], "images")
    sys.stdout.flush()
    for i in range(df.shape[0]):
        # Check for NaNs
        if links[i] == links[i]:
            # Open url and convert to JPEG image
            try:
                f = urlopen(links[i])
                image_file = io.BytesIO(f.read())
                im = Image.open(image_file)
                w, h = im.size
                # The filename is the index of the image in the dataframe
                #filename = str(i) + '.jpg'
                filename = str(queries[i]) + '_' + str(ids[i]) + '.jpg'
                print("Attempting to write to:", os.path.join(dataset_dir, subdir, filename))
                sys.stdout.flush()
                new_w = min(w, 256)
                new_h = int((1.0 * h * new_w) / w)
                im.convert('RGB').resize((new_w, new_h)).save(os.path.join(dataset_dir, subdir, filename), 'JPEG')
            except Exception as error:
                print("FAILED ON", i)
                print(error)
                sys.stdout.flush()
                continue

def download_im_with_text(search_query, start, end, dataset_dir='data', subdir='photos'):
    """Download images using the urls in the dataframe specified by the search query.

    Parameters:
        search_query: A string giving the sentiment to load the corresponding dataframe.
        start: A start index for the loaded dataframe.
        end: An end index for the loaded dataframe. -1 corresponds to the last row.
        dataset_dir: A directory where the dataframes are stored.
        subdir: A subdirectory to store the photos.

    Returns:
        Images downloaded in the directory dataset_dir/subdir/search_query, having 
        the posts ids as names.
    """
    # Load data
    emb_name = 'glove'
    text_dir = 'text_model'
    emb_dir = 'embedding_weights'
    filename = 'glove.6B.50d.txt'
    if emb_name == 'word2vec':
        vocabulary, embedding = _load_embedding_weights_word2vec(text_dir, emb_dir, filename)
    else:
        vocabulary, embedding = _load_embedding_weights_glove(text_dir, emb_dir, filename)

    df = preprocess_one_df(vocabulary, embedding, search_query, _POST_SIZE)
    if end == -1:
        end = df.shape[0]

    links = df['photo']
    # Create subdir if it doesn't exist
    if not tf.gfile.Exists(os.path.join(dataset_dir, subdir)):
        tf.gfile.MakeDirs(os.path.join(dataset_dir, subdir))
    # Create search_query folder if it doesn't exist
    photos_dir = os.path.join(dataset_dir, subdir, search_query)
    if not tf.gfile.Exists(photos_dir):
        tf.gfile.MakeDirs(photos_dir)
    for i in range(start, end):
        # Check for NaNs
        if links[i] == links[i]:
            # Open url and convert to JPEG image
            try:
                f = urlopen(links[i])
            except Exception:
                continue
            image_file = io.BytesIO(f.read())
            im = Image.open(image_file)
            # The filename is the index of the image in the dataframe
            filename = str(i) + '.jpg'
            im.convert('RGB').save(os.path.join(photos_dir, filename), 'JPEG')
