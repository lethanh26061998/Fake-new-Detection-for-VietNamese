import transformers
from transformers import TFAutoModel, AutoTokenizer, TFAutoModelForSequenceClassification, PhobertTokenizer
import numpy as np 
import pandas as pd 

MAX_LEN = 256

roberta = 'vinai/phobert-base' 
# roberta_tokenizer = AutoTokenizer.from_pretrained(roberta)
roberta_tokenizer = PhobertTokenizer.from_pretrained(roberta)
# roberta_model = TFAutoModel.from_pretrained(roberta)

def regular_encode(df, max_len=MAX_LEN):
    
    roberta_enc_di = roberta_tokenizer.batch_encode_plus(
        df["post_message"].values,
        return_token_type_ids=True,
        pad_to_max_length=True,
        max_length=max_len,
        truncation=True,
    )
    
    # user_name = (df["user_name"]).values
    
    timestamp_post = (df["timestamp_post"]/1e13).values
    num_like_post = (df["num_like_post"]/1e5).values
    num_comment_post = (df["num_comment_post"]/1e4).values
    num_share_post = (df["num_share_post"]/1e4).values
    
    roberta_enc = (
        np.array(roberta_enc_di["input_ids"]),
        np.array(roberta_enc_di["attention_mask"]),
        np.array(roberta_enc_di["token_type_ids"]),
        # user_name,
        timestamp_post,
        num_like_post,
        num_comment_post,
        num_share_post,
        
        # np.concatenate([num_like_post, num_comment_post, num_share_post], axis=0)
    )
    
    
    return roberta_enc