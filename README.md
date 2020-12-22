# Fake-new-Detection-for-VietNamese
1. Cài đặt môi trường
- Sử dung virtualen để tạo môi trường:
	python3 -m venv DATN
- Vào môi trường ảo đã được cài đặt, có tên là DATN: 
	source DATN/bin/activate
- Nâng cấp môi trường: 
	pip install --upgrade pip setuptools wheel
- Cài đặt thư viện để chạy webdemo:
	+ sudo apt -y install rabbitmq-server
	+ pip install pika
	+ npm install amqplib  --save
2. Cài đặt code
2.1 Cấu trúc source code
- Crawl:
	+ listweb.py: chưa biến là 1 dict, lưu trữ phân tích trang của các websites.
	+ crawl_news.py: file crawl các bài báo trên các trang được phân tích ở listweb 
- FakeNewDetection:
	+ Train: train model trên google colab Pro (có 2 file note books - model phoBERT và model BERT multilingual)
	+ Model: 
		- phobert-base: Download pretrain model phobert theo link https://huggingface.co/vinai/phobert-base/tree/main
		- 08122020: lưu trữ model theo ngày train với accuracy cao nhất đã được train
	+ Data: lưu trữ folder dataset và các file code tiền xử lý dữ liệu
	+ vncorenlp: sử dụng thư viện vncorenlp tách từ
	+ predict_sample.py: file code dự đoán 1 tin tức fake hay real
- WebDemo: đưa hệ thống dự đoán tin tức lên web, sử dụng nodejs
2.2 Dữ liệu
- Crawls: 
	Sử dụng Selenium+Chrome Driver để thu thập dữ liệu:
	+ Kiểm tra version của Google chrome đang sử dụng: 85.0.4183.87
	+ Download driver Google chrome tương ứng: 
		https://chromedriver.storage.googleapis.com/index.html?path=85.0.4183.87/ 
	+ Giải nén và lưu folder chromedriver_linux64 trong folder Crawl_news
- Dataset cho train model:
	+ Sử dụng bộ dữ liệu của cuộc thi vlsp 2020, có trong thư mục FakeNewDetection/Data/dataset
3. Train model: Thử nghiệm với 2 model
- Chạy file FakeNewDetection/Train/PhoBert+finetune.ipynb trên google colab
- Chạy file FakeNewDetection/Train/bert-multilingual-VN.ipynb trên google colab
4. Chạy code demo
- Download code: git clone https://github.com/lethanh26061998/Fake-new-Detection-for-VietNamese.git
- Copy thư mục code vừa down về trong môi trường ảo đã tạo
- Sử dụng pip để cài đặt các thư viện: pip install -r requirment.txt
- Vào thư mục WebDemo và run file: python3 message.py
- Mở 1 terminal khác, vào thư mục WebDemo để chạy server node: node index.js
