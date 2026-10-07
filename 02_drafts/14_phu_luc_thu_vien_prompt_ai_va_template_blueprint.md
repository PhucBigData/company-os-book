# PHỤ LỤC: THƯ VIỆN PROMPT AI & MẪU THIẾT KẾ BLUEPRINT CHUẨN

---

## PHẦN A: BỘ THƯ VIỆN 5 PROMPT CHỈ HUY AI THỰC CHIẾN

### PROMPT 1: KHẢO SÁT & BÓC TÁCH BÀI TOÁN DOANH NGHIỆP (DISCOVERY PROMPT)
```markdown
Bạn là Chuyên gia Tư vấn Chuyển đổi số & Kiến trúc Quy trình (Lead Business Analyst). 
Tôi đang quản lý một doanh nghiệp với bối cảnh thực tế sau:
- Ngành nghề kinh doanh: [ĐIỀN NGÀNH NGHỀ]
- Quy mô nhân sự: [SỐ LƯỢNG NHÂN SỰ]
- Vấn đề nhức nhối nhất hiện tại: [MÔ TẢ NỖI ĐAU VẬN HÀNH / TẮC NGHẼN]

Hãy giúp tôi thực hiện bước Discovery khảo sát chuyên sâu:
1. Đặt ra 5 câu hỏi cốt lõi để làm rõ dòng chảy dữ liệu giữa các phòng ban.
2. Xác định đâu là "Nút thắt cổ chai" (Bottleneck) lớn nhất đang làm thất thoát tiền bạc hoặc thời gian.
3. Đề xuất phạm vi triển khai tối thiểu (MVP - Minimum Viable Product) để giải quyết dứt điểm nỗi đau này trong vòng 14 ngày.
```

---

### PROMPT 2: CHUYỂN HÓA SƠ ĐỒ QUY TRÌNH THÀNH LƯỢC ĐỒ ERD (PROCESS TO ERD)
```markdown
Dưới đây là mô tả quy trình nghiệp vụ đã được chuẩn hóa của công ty tôi:
[DÁN QUY TRÌNH HOẶC SƠ ĐỒ SWIMLANE VÀO ĐÂY]

Hãy đóng vai trò Kỹ sư Cơ sở Dữ liệu Doanh nghiệp (Data Engineer):
1. Chuyển hóa toàn bộ quy trình này thành mô hình 4 tầng Company OS:
   - Tầng DIM (Danh mục master data)
   - Tầng FACT (Giao dịch phát sinh)
   - Tầng LOG (Vết kiểm toán)
   - Tầng RP (Báo cáo tổng hợp)
2. Chỉ định rõ ràng các trường khóa chính (Primary Key), trường liên kết (Link Field), trường tra cứu (Lookup), và trường tổng hợp (Rollup).
3. Xuất ra sơ đồ thực thể ERD hoàn chỉnh bằng cú pháp Mermaid.
```

---

### PROMPT 3: LẬP TRÌNH CÔNG THỨC BASE PHỨC TẠP (COMPLEX FORMULA GENERATOR)
```markdown
Tôi đang cấu hình một trường Formula trên Lark Base với yêu cầu tính toán logic sau:
- Trường đầu vào 1: [Tên trường & Kiểu dữ liệu]
- Trường đầu vào 2: [Tên trường & Kiểu dữ liệu]
- Logic mong muốn: [Mô tả bằng lời điều kiện IF / SWITCH / DATEDIF / REGEX]

Hãy viết công thức chuẩn mực tương thích 100% với cú pháp hàm của Lark Base:
1. Trả về đoạn code công thức sạch, không thừa dấu cách.
2. Giải thích ngắn gọn cách công thức xử lý các trường hợp ngoại lệ (giá trị rỗng, lỗi chia cho 0).
3. Đưa ra 2 ví dụ kiểm thử với dữ liệu giả định để đối soát.
```

---

### PROMPT 4: THIẾT KẾ MA TRẬN PHÂN QUYỀN RBAC & FIELD PERMISSION
```markdown
Tôi có một bảng quản lý [TÊN NGHIỆP VỤ] trên Lark Base với các trạng thái sau:
[DÁN DANH SÁCH TRẠNG THÁI: Khởi tạo -> Chờ duyệt -> Đã duyệt -> Hoàn thành]

Trong công ty có 4 nhóm vai trò: Nhân viên, Trưởng phòng, Kế toán, Giám đốc.

Hãy lập Ma trận Phân quyền bảo mật cấp độ trường (Field-Level RBAC Matrix):
1. Bảng đối chiếu: Trạng thái x Vai trò x Quyền hạn (Không thấy / Chỉ xem / Được sửa / Được duyệt).
2. Chỉ ra các trường nhạy cảm cần khóa cứng ở từng trạng thái để chống gian lận.
3. Hướng dẫn cách chia các View lọc dữ liệu cá nhân hóa cho từng phòng ban.
```

---

### PROMPT 5: SOẠN THẢO PLAYBOOK BÀN GIAO WIKI (HANDOVER PLAYBOOK DRAFTER)
```markdown
Hệ thống Lark Base cho phòng [TÊN PHÒNG BAN] đã được dựng xong với các tính năng:
[LIỆT KÊ CÁC TÍNH NĂNG VÀ FORM NHẬP LIỆU]

Hãy đóng vai trò Giám đốc Đào tạo & Văn hóa Số (Change Management Lead):
1. Soạn thảo một trang Cẩm nang Vận hành (SOP Playbook) chuẩn mực trên Lark Wiki.
2. Viết bằng ngôn ngữ thân thiện, dễ hiểu, hướng đến người dùng cuối không rành công nghệ.
3. Cấu trúc chuẩn 5 phần: Mục tiêu & Quyền lợi -> Hướng dẫn 3 bước -> Checklist tự kiểm tra -> Xử lý sự cố thường gặp (FAQ) -> Tiêu chuẩn nghiệm thu.
```

---

## PHẦN B: MẪU BLUEPRINT KIẾN TRÚC BASE DOANH NGHIỆP CHUẨN

```markdown
# 🏛️ BASE BLUEPRINT: [TÊN HỆ THỐNG]
*Mã dự án: COS_BASE_[MÃ]* | *Phiên bản: 1.0*

## 1. MỤC TIÊU & PHẠM VI (SCOPE)
- Phòng ban áp dụng: [Marketing / Sales / Kho / Kế toán]
- Bài toán giải quyết: [Số hóa đơn hàng, kiểm soát tồn kho, đo lường KPI]
- Người sở hữu hệ thống (System Owner): [Họ tên & Chức vụ]

## 2. KIẾN TRÚC MÔ HÌNH DỮ LIỆU (DATA ARCHITECTURE)
| Tên bảng | Phân tầng | Mục đích sử dụng | Khóa chính (Primary Key) |
| :--- | :---: | :--- | :--- |
| `DIM_KhachHang` | DIM | Lưu danh mục khách hàng master data | `Ma_KH` (Auto-number) |
| `DIM_SanPham` | DIM | Lưu danh mục sản phẩm & đơn giá niêm yết | `Ma_SKU` (Text) |
| `FACT_DonHang` | FACT | Lưu các giao dịch đơn hàng phát sinh | `Ma_Don` (Formula) |
| `FACT_ChiTietDon` | FACT | Bảng nối N-N lưu chi tiết sản phẩm mua | `Ma_ChiTiet` (Formula) |
| `LOG_TrangThai` | LOG | Ghi vết lịch sử chuyển trạng thái | `Ma_Log` (Auto-number) |
| `RP_BaoCaoTuan` | RP | Báo cáo KPI tổng hợp theo tuần | `Ma_Tuan` (Text: W40-2026) |

## 3. MÁY TRẠNG THÁI & CHUYỂN TIẾP (STATE MACHINE TRANSITIONS)
1. `Khởi tạo (Draft)`: Nhân viên nhập liệu $\rightarrow$ Bấm nút "Gửi duyệt".
2. `Chờ duyệt (Pending)`: Hệ thống gửi thông báo cho Trưởng phòng $\rightarrow$ Trưởng phòng bấm "Duyệt" hoặc "Từ chối".
3. `Đã duyệt (Approved)`: Tự động khóa quyền sửa của nhân viên $\rightarrow$ Chuyển thông báo cho Kế toán.
4. `Đang giao (Shipping)`: Kho xác nhận xuất hàng $\rightarrow$ Cập nhật mã vận đơn.
5. `Hoàn tất (Completed)`: Khách nhận hàng $\rightarrow$ Khóa 100% quyền sửa vĩnh viễn.

## 4. MA TRẬN PHÂN QUYỀN HIỂN THỊ (APPMODE PORTAL PAGES)
- **Trang 1: Executive Dashboard (CEO)**: 3 Thẻ Metric KPI + Biểu đồ doanh thu + Bảng cảnh báo đơn trễ.
- **Trang 2: Manager Dispatch Hub (Trưởng phòng)**: Bảng Kanban kéo thả trạng thái + Nút phê duyệt nhanh.
- **Trang 3: Staff Workspace (Nhân viên)**: Bảng cá nhân "Việc của tôi" + Form nhập liệu tối giản.
```
