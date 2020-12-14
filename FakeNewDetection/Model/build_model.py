import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K
from tensorflow.keras import layers

from transformers import TFAutoModel, AutoTokenizer, AutoModelForMaskedLM, TFAutoModelForSequenceClassification, PhobertTokenizer

MAX_LEN = 256
# roberta = "vinai/phobert-base"
roberta = "/home/thanh/DATN/FakeNewDetection/Model/phobert-base"

def build_model(bert_model_name_or_path=roberta, max_len=384, n_hiddens=-1):
    print("start===00000===")
    bert_model = TFAutoModel.from_pretrained(bert_model_name_or_path)
    print("start====1111=====")
    bert_input_word_ids = tf.keras.layers.Input(
        shape=(max_len,), dtype=tf.int32, name="bert_input_id"
    )
    bert_attention_mask = tf.keras.layers.Input(
        shape=(max_len,), dtype=tf.int32, name="bert_attention_mask"
    )
    bert_token_type_ids = tf.keras.layers.Input(
        shape=(max_len,), dtype=tf.int32, name="bert_token_type_ids"
    )

    bert_sequence_output = bert_model(
        bert_input_word_ids,
        attention_mask=bert_attention_mask,
        token_type_ids=bert_token_type_ids,
        output_hidden_states=True,
        output_attentions=True,
        
    )

    # print(len(bert_sequence_output)) # 4

    # print(bert_sequence_output[0].shape) # (None, max_len, 768)

    # print(bert_sequence_output[1].shape) # (None, 768)
    # print(len(bert_sequence_output[2])) # 13
    # print(bert_sequence_output[2][0].shape) # (None, max_len, 768)
    # print(len(bert_sequence_output[3])) # 12
    # print(bert_sequence_output[3][0].shape) # (None, 12, None, max_len)

    # TODO: get bert embedding

    if n_hiddens == -1:  # get [CLS] token embedding only
        # print("Get pooler output of shape (batch_size, hidden_size)")
        bert_sequence_output = bert_sequence_output[0][:, 0, :]
    else:  # concatenate n_hiddens final layer
        # print(f"Concatenate {n_hiddens} hidden_states of shape (batch_size, hidden_size)")
        bert_sequence_output = tf.concat(
            [bert_sequence_output[2][-i] for i in range(n_hiddens)], axis=-1)

    # print("bert_sequence_output shape", bert_sequence_output.shape)

# MLP 
    # batch_norm1 = BatchNormalization()(bert_sequence_output)
    flatten = tf.keras.layers.Flatten()(bert_sequence_output)
    # bert_output = tf.keras.layers.Dense(16, activation="relu")(bert_sequence_output)
    bert_output = tf.keras.layers.Dense(16, activation="relu")(flatten)

    timestamp_post = tf.keras.layers.Input(shape=(1,), dtype=tf.float32, name="timestamp_post")
    num_like_post = tf.keras.layers.Input(shape=(1,), dtype=tf.float32, name="num_like_post")
    num_comment_post = tf.keras.layers.Input(shape=(1,), dtype=tf.float32, name="num_comment_post")
    num_share_post = tf.keras.layers.Input(shape=(1,), dtype=tf.float32, name="num_share_post")

    aulixiary_info = tf.keras.layers.Concatenate()([timestamp_post, num_like_post, num_comment_post, num_share_post])

    out = tf.keras.layers.Concatenate()([bert_output, aulixiary_info]) 
    # out = tf.keras.layers.Flatten()(bert_sequence_output)
    out = tf.keras.layers.Dense(1, activation="sigmoid")(out)
# # CNN
#     out = tf.keras.layers.Dropout(0.15)(bert_sequence_output)
#     out = tf.keras.layers.Conv1D(768, 2,padding='same')(out)
#     out = tf.keras.layers.LeakyReLU()(x1)
#     out = tf.keras.layers.Conv1D(64, 2,padding='same')(out)
#     out = tf.keras.layers.Dense(1)(out)
#     out = tf.keras.layers.Flatten()(out)
#     out = tf.keras.layers.Activation('softmax')(out)

    model = tf.keras.models.Model(
        inputs=[
            bert_input_word_ids,
            bert_attention_mask,
            bert_token_type_ids,  # bert input
            # user_name,
            timestamp_post,
            num_like_post,
            num_comment_post,
            num_share_post,
        ],
        outputs=out,
    )
    model.compile(
        tf.keras.optimizers.Adam(lr=5e-5),
        loss="binary_crossentropy",
        metrics=[tf.keras.metrics.AUC()],
    )

    return model
# print("Start==========huhu===========")
# model = build_model(max_len=MAX_LEN)
# print("Built==========****===========")
# model.summary()