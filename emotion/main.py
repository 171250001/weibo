# -*- coding:utf-8 -*-

"""
      ┏┛ ┻━━━━━┛ ┻┓
      ┃　　　　　　 ┃
      ┃　　　━　　　┃
      ┃　┳┛　  ┗┳　┃
      ┃　　　　　　 ┃
      ┃　　　┻　　　┃
      ┃　　　　　　 ┃
      ┗━┓　　　┏━━━┛
        ┃　　　┃   神兽保佑
        ┃　　　┃   代码无BUG！
        ┃　　　┗━━━━━━━━━┓
        ┃CREATE BY SNIPER┣┓
        ┃　　　　         ┏┛
        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
          ┃ ┫ ┫   ┃ ┫ ┫
          ┗━┻━┛   ┗━┻━┛

"""
import tensorflow as tf
from utils import get_data
from bert_fc import Bert

for gpu in tf.config.experimental.list_physical_devices('GPU'):
    tf.config.experimental.set_memory_growth(gpu, True)

train_X, train_y, val_X, val_y = get_data()

callbacks = [
    tf.keras.callbacks.ModelCheckpoint(filepath='output/model.ckpt', save_best_only=True)
]

model = Bert()

optimizer = tf.keras.optimizers.Adam(1e-6)
model.compile(optimizer=optimizer, loss=tf.keras.losses.categorical_crossentropy, metrics=['acc'])

try:
    model.load_weights('output/model.ckpt')
    print('load saved model')
except:
    print('train model for init')

model.fit(
    x=train_X,
    y=train_y,
    epochs=5,
    batch_size=16,
    validation_data=(val_X, val_y),
    callbacks=callbacks
)