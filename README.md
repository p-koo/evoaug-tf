# EvoAug-TF
Evolution-inspired data augmentations for TensorFlow-based models for regulatory genomics. For more information, see documentation on [EvoAug-TF.ReadTheDocs.io](https://evoaug-tf.readthedocs.io/en/latest/index.html).

#### Install:

```
pip install evoaug-tf
```


#### Dependencies:

```
tensorflow 2.11.0+cu114
numpy 1.21.6
```

#### Example

```python
import os
from evoaug_tf import evoaug, augment
import tensorflow as tf
from tensorflow import keras

keras.backend.clear_session()

model_func = "DEFINE KERAS MODEL"
input_shape = (L,A) <-- DEFINE L, A and input_shape should be first arguments to model_func (eg. model = model_func(input_shape))
augment_list = [
    augment.RandomDeletion(delete_min=0, delete_max=30),
    augment.RandomRC(rc_prob=0.5),
    augment.RandomInsertion(insert_min=0, insert_max=20),
    augment.RandomTranslocation(shift_min=0, shift_max=20),
    augment.RandomNoise(noise_mean=0, noise_std=0.3),
    augment.RandomMutation(mutate_frac=0.05)
]


model = evoaug.RobustModel(model_func, input_shape, augment_list=augment_list, max_augs_per_seq=1, hard_aug=True)

model.compile(keras.optimizers.Adam(learning_rate=0.001, weight_decay=1e-6), loss='mse') 
            

# set up callbacks
es_callback = keras.callbacks.EarlyStopping(monitor='val_loss',
                                            patience=10,
                                            verbose=1,
                                            mode='min',
                                            restore_best_weights=True)

reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss',
                                                factor=0.1,
                                                patience=5, 
                                                min_lr=1e-7,
                                                mode='min',
                                                verbose=1)

# pre-train model with augmentations
model.fit(x_train, y_train,
                epochs=100,
                batch_size=100,
                shuffle=True,
                validation_data=(x_valid, y_valid),
                callbacks=[es_callback, reduce_lr])

save_path = os.path.join(output_dir, exp_name+"_aug.h5")
model.save_weights(save_path)

# set up fine-tuning
finetune_optimizer = keras.optimizers.Adam(learning_rate=0.0001, weight_decay=1e-6)
model.finetune_mode(optimizer=finetune_optimizer)

# set up callbacks
es_callback = keras.callbacks.EarlyStopping(monitor='test_pearson_r (Dev)',
                                            patience=5,
                                            verbose=1,
                                            mode='max',
                                            restore_best_weights=True)

# train model
model.fit(x_train, y_train,
                epochs=finetune_epochs,
                batch_size=batch_size,
                shuffle=True,
                validation_data=(x_valid, y_valid),
                callbacks=[es_callback])

save_path = os.path.join(output_dir, exp_name+"_finetune.h5")
model.save_weights(save_path)
```

#### Example on Google Colab:

- Example DeepSTARR analysis: https://colab.research.google.com/drive/11TA02v-azuqAIV5s3sCbWTH-C5W7_KMA
- Example ChIP-seq analysis: https://colab.research.google.com/drive/1fzpH2Qv8RFNzMvIDRJUGnUTaacFMIJBV 
