import numpy
import h5py
import tensorflow as tf


def Spearman(y_true, y_pred):
     return ( tf.py_function(spearmanr, [tf.cast(y_pred, tf.float32), 
                       tf.cast(y_true, tf.float32)], Tout = tf.float32) )
     

def pearson_r(y_true, y_pred):
    y_true = tf.cast(y_true, 'float32')
    y_pred = tf.cast(y_pred, 'float32')
    eps = tf.constant(1e-7, 'float32')
    mean_cross = tf.reduce_mean(tf.multiply(y_true, y_pred), axis=0)
    mean_true = tf.reduce_mean(y_true, axis=0)
    mean_true_sqr = tf.reduce_mean(tf.math.square(y_true), axis=0)
    norm_true = tf.math.sqrt(mean_true_sqr - tf.math.square(mean_true) + eps)

    mean_pred = tf.reduce_mean(y_pred, axis=0)
    mean_pred_sqr = tf.reduce_mean(tf.math.square(y_pred), axis=0)
    norm_pred = tf.math.sqrt(mean_pred_sqr - tf.math.square(mean_pred) + eps)

    covariance = mean_cross - tf.multiply(mean_true, mean_pred)
    correlation = tf.divide(covariance, tf.math.multiply(norm_true, norm_pred) + eps)

    return tf.reduce_mean(correlation)


def H5DataLoader(data_path, stage=None, lower_case=True, transpose=False, downsample=None):
    x = 'X'
    y = 'Y'
    if lower_case:
        x = 'x'
        y = 'y'
    if stage == "fit" or stage is None:
        with h5py.File(data_path, 'r') as dataset:
            x_train = np.array(dataset[x+'_train']).astype(np.float32)
            y_train = np.array(dataset[y+'_train']).astype(np.float32).transpose()
            x_valid = np.array(dataset[x+'_valid']).astype(np.float32)
            if transpose:
                x_train = np.transpose(x_train, (0,2,1))
                x_valid = np.transpose(x_valid, (0,2,1))
            if downsample:
                x_train = x_train[:downsample]
                y_train = y_train[:downsample]
            y_valid = np.array(dataset[y+"_valid"].astype(np.float32)).transpose()

    if stage == "test" or stage is None:
        with h5py.File(data_path, "r") as dataset:
            x_test = np.array(dataset[x+"_test"]).astype(np.float32)
            if transpose:
                x_test = np.transpose(x_test, (0,2,1))
            y_test = np.array(dataset[y+"_test"]).astype(np.float32).transpose()
    
    return x_train, y_train, x_valid, y_valid, x_test, y_test