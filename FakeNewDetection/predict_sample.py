import time
import os
import math
import numpy as np 
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K
from tensorflow.keras import layers
from tensorflow.python.keras import initializers
import re
import string
import transformers
from transformers import TFAutoModel, AutoTokenizer, AutoModelForMaskedLM, TFAutoModelForSequenceClassification, PhobertTokenizer

roberta = '/home/thanh/DATN/FakeNewDetection/Model/phobert-base' 
MAX_LEN = 256

from Data.clean_text import clean_post, extract_num
from Data.regular_encode import regular_encode
from Data.tokenizer import VnCoreTokenizer
from Model.build_model import build_model

output_dir = '/home/thanh/DATN/FakeNewDetection/Model/08122020'

def predict(test_dataframe):

  test_dataframe['post_message'] = test_dataframe['post_message'].apply(clean_post)
  test_dataframe["post_message"] = test_dataframe["post_message"].apply(VnCoreTokenizer().tokenize)

  test_dataframe["post_message"] = test_dataframe["post_message"].astype(str)
  test_dataframe["timestamp_post"] = test_dataframe["timestamp_post"].astype(float)

  for col in ["timestamp_post", "num_like_post", "num_comment_post", "num_share_post"]:
    test_dataframe[col] = test_dataframe[col].apply(extract_num)
    test_dataframe[col] = test_dataframe[col].astype(float)
    test_dataframe[col] = test_dataframe[col].fillna(0)

  X_test = regular_encode(test_dataframe, max_len=MAX_LEN)
  y_test = np.zeros((len(test_dataframe),1))
  model = build_model(max_len=MAX_LEN)
  preds = []
  for i, file_name in enumerate(os.listdir(output_dir)):
      print('_'*80)
      K.clear_session()
      model_path = os.path.join(output_dir, file_name)
      print(f'Inferencing with model from: {model_path}')
      model.load_weights(model_path)
      pred = model.predict(X_test,y_test)
      print(pred)
      preds.append(pred)
  preds = np.mean(preds, axis=0)
  print("predict weight is: ", preds)

data_test = [{'post_message': '3 công nhân trung quốc làm cty hòa phát bị nhiễm visrut corona là sự thật mọi người đề phòng mặc dù hòa phát ngăn chặn yếm mọi thông tin nhưng công nhân làm ở hòa phát đã nói lại sự thật trên... mình đăng tin này có thể bị lực lượng chức năng ngăn chặn nguồn tin và xử phạt và bắt giữ mình nhưng mình cũng muốn nói vì đó là sự thật. sau 1 giờ mình sẽ xóa tin này vì k muốn bị lực lượng nhà nước cưỡng chế áp giải bắt bớ mình dù đó là sự thật.' ,
              'timestamp_post': 1596255660, 
              'num_like_post': 0 , 
              'num_comment_post': 0, 
              'num_share_post': 0}] 
df_test_1 = pd.DataFrame(data = data_test) 
start_time = time.time()
predict(df_test_1)
print("--- Time predict is %s seconds ---" % (time.time() - start_time))