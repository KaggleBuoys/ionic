#
# Stephen Vondenstein, Matthew Buckley
# 10/09/2018
#
import tensorflow as tf

def process(dataset, training, config, len):
    dataset = dataset.map(parse_data, num_parallel_calls=config.batch_size)
    dataset = dataset.map(resize_data, num_parallel_calls=config.batch_size)
    dataset = dataset.map(normalize_data, num_parallel_calls=config.batch_size)
    if config.augment and training:
        dataset = dataset.concatenate(augment_data(dataset, config))
        dataset = dataset.shuffle(len * 2)
    dataset = dataset.batch(config.batch_size)

    return dataset

def parse_data(image_paths, label_paths, names):
    image_content = tf.read_file(image_paths)
    images = tf.image.decode_png(image_content, channels=1)

    mask_content = tf.read_file(label_paths)
    masks = tf.image.decode_png(mask_content, channels=1)

    return images, masks, names

def resize_data(image, mask, name):
    image = tf.image.resize_images(image, [128, 128])
    mask = tf.image.resize_images(mask, [128, 128])

    return image, mask, name

def normalize_data(image, mask, name):
    image = tf.cast(image, tf.float32)
    image = image / 255.0

    mask = tf.cast(mask, tf.float32)
    mask = mask / 255.0

    return image, mask, name

def augment_data(dataset, config):
    dataset = dataset.map(flip_data, num_parallel_calls=config.batch_size)

    return dataset

def flip_data(image, mask, name):
    image = tf.image.flip_left_right(image)
    mask = tf.image.flip_left_right(mask)

    return image, mask, name
