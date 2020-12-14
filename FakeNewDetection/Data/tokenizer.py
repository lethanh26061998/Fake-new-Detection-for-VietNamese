from vncorenlp import VnCoreNLP

class VnCoreTokenizer():
    def __init__(self, path="/home/thanh/DATN/FakeNewDetection/vncorenlp/VnCoreNLP-1.1.1.jar"):
        self.rdrsegmenter = VnCoreNLP(path,
                                      annotators="wseg", max_heap_size='-Xmx500m')
    def tokenize(self, text: str) -> str:
        sentences = self.rdrsegmenter.tokenize(text)
        output = ""
        for sentence in sentences:
            output += " ".join(sentence)
        return output

# tokenizer = VnCoreTokenizer("/home/thanh/DATN/FakeNewDetection/vncorenlp/VnCoreNLP-1.1.1.jar")
# print(tokenizer.tokenize("Tôi là sinh viên đại học Bách Khoa Hà Nội"))
