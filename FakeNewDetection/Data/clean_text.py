import re
import math

def clean_post(text):
    # Remove hashtag
    text = re.sub(r'#\w*','', str(text))
    # Remove tickers
    text = re.sub(r'\$\w*', '', text)
    # Remove URL, RT, mention(@)
    text=  re.sub(r'http(\S)+', '',text)
    text=  re.sub(r'https(\S)+', '',text)
    text=  re.sub(r'http ...', '',text)
    text = re.sub(r'@[\S]+','',text)
    
    # Remove repeating syllables
    text = re.sub(r'(\D)\1+', r'\1', text)

    # Remove words with > 7 letters ("nghiêng" - longest)
    text = re.sub(r'\b[a-zA-Z]{8,}\b', '', text)

    # Remove other characters
    # text = re.sub(r'_', ' ' , text)
    text = re.sub(r'\:\D{1}', ' ' , text)
    text = re.sub(r'<url>', '' , text)
    text = re.sub(r'< url >', '' , text)
    text = re.sub(r'<URL>', '' , text)
    text = re.sub(r'< URL >', '' , text)
     # Remove emoji
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text) # no emoji
    
    # Remove whitespace
    text = re.sub(r'\s\s+',' ', text)
    text = re.sub(r'[ ]{2, }',' ',text)
    return text
# cleaned_text = clean_post("https://soict.hust.edu.vn/ #sad Ghê chưa, <url> 😂 Tôi là cảnh_sát khu vực HBT, hãy gọi cho tôi, sdt của tôi là 0967374782")
# print(cleaned_text)

def extract_num(text):
    if type(text)==str:
        if text=="unknown":
            return math.nan
        return re.findall("\d+", text)[0]
    return text