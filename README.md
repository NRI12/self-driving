
---
**Tên Dự Án:** Xe tự lái raspberry sử dụng CNN

**Mô Tả:**

Dự án này là một backend phát triển các thuật toán lái xe tự động. Qua việc tích hợp mô hình dự đoán hướng lái với môi trường xe tự hành raspberry

**Luồng Dữ Liệu và Xử Lý:**
1. **Thu Thập Dữ Liệu:**
   - Sử dụng `collect_data.py` để thu thập dữ liệu hình ảnh từ môi trường mô phỏng. Mỗi hình ảnh được gắn nhãn với thông tin về hướng lái tương ứng, được lưu trữ trong `image_log.csv`.

2. **Huấn Luyện Mô Hình:**
   - Chạy `train.py` để huấn luyện mô hình dự đoán hướng lái dựa trên các dữ liệu đã thu thập. Mô hình (`model_steering_prediction.h5`) sử dụng mạng nơ-ron tích chập để xử lý hình ảnh và dự đoán góc lái.

3. **Sử Dụng Mô Hình:**
   - `use_model.py` sử dụng mô hình đã huấn luyện để thực hiện dự đoán trong môi trường mô phỏng thời gian thực. Mô hình sẽ nhận dữ liệu hình ảnh từ môi trường và tính toán hướng lái phù hợp.

**Cài Đặt và Khởi Chạy:**

- Clone và cài đặt các phụ thuộc:
  ```
  git clone https://github.com/NRI12/self-driving.git
  cd self-driving-main
  pip install -r requirements.txt
  ```
- Khởi chạy mô phỏng:
  ```
  python main_func.py
  ```

**Cấu Trúc Thư Mục:**

- `captured_images`: Chứa hình ảnh thu thập được.
- `collect_data.py`: Script thu thập dữ liệu.
- `image_log.csv`: Ghi nhận hình ảnh và thông tin lái.
- `main_func.py`: Điểm khởi đầu của mô phỏng.
- `model_steering_prediction.h5`: Mô hình huấn luyện.
- `requirements.txt`: Các gói cần thiết.
- `train.py`: Script huấn luyện mô hình.
- `use_model.py`: Script sử dụng mô hình trong mô phỏng.

**Yêu Cầu Phần cứng**
- Xe tự hành với đầy đủ các thành phần như  động cơ kết nối l29n raspberry.

**Yêu Cầu Hệ Thống:**

- Python 3.7+
- PyGame 1.9.6+
- TensorFlow 2.x
**Liên Hệ:**

Để biết thêm thông tin hoặc tham gia, vui lòng gửi email đến [ctv55345@gmail.com](ctv55345@gmail.com).

