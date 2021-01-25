# -*- coding:utf-8 -*-

import tensorflow as tf
from transformers import TFBertModel


class Bert(tf.keras.Model):
    def __init__(self):
        super(Bert, self).__init__()
        self.bert = TFBertModel.from_pretrained('bert-base-chinese')
        self.dense = tf.keras.layers.Dense(2, activation='sigmoid')
    def call(self, inputs,training=True):
        ids, attention_mask, token_type = inputs
        out = self.bert(ids, attention_mask=attention_mask, token_type_ids=token_type,training=training)
        out = out[1]
        out = self.dense(out)
        return out
