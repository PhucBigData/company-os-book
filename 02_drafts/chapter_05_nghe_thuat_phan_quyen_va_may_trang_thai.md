# CHƯƠNG 5: NGHỆ THUẬT PHÂN QUYỀN & THIẾT KẾ MÁY TRẠNG THÁI (STATE MACHINE)

---

## 1. CÂU CHUYỆN CHIẾN TRƯỜNG (THE WAR STORY)

Tháng 8 năm 2026, tôi được một đối tác là công ty thương mại kỹ thuật tại Bình Dương gọi điện với tâm trạng vô cùng hoảng hốt:

*"Phúc ơi, công ty anh vừa mất đứt 250 triệu tiền cọc của khách hàng lớn nhất, chỉ vì một cú click chuột ngớ ngẩn!"*

Chuyện là thế này: Một bạn nhân viên kinh doanh mới vào làm được 2 tuần. Bạn mở bảng theo dõi hợp đồng trên hệ thống lên để xem thông tin. Vô tình thế nào, bạn bấm chuột vào ô trạng thái của hợp đồng trị giá 3 tỷ đồng và chuyển từ `Đang thương thảo điều khoản` sang `Đã ký hợp đồng & Chờ sản xuất`.

Hệ thống lập tức kích hoạt luồng tự động hóa:
- Gửi thông báo cho xưởng sản xuất: Bắt đầu gia công lô linh kiện theo đơn.
- Gửi thông báo cho bộ phận mua hàng: Nhập 500 triệu đồng nguyên vật liệu từ nhà cung cấp.

Ba ngày sau, khách hàng gọi điện thông báo: *"Bên tôi quyết định không ký hợp đồng nữa vì tìm được đối tác giá tốt hơn."*

Lúc này, nguyên vật liệu đã nhập về kho, xưởng đã gia công được một nửa, và công ty thiệt hại hơn 250 triệu đồng tiền phôi hỏng. 

Giám đốc gầm lên trong cuộc họp: *"Tại sao một đứa nhân viên thử việc mới vào 2 tuần lại có quyền bấm nút 'Đã ký hợp đồng' cho một dự án 3 tỷ đồng mà không cần ai duyệt?!"*

Câu trả lời rất chua chát: Bởi vì người dựng hệ thống đã mắc một sai lầm phổ biến nhất trong giới Low-code: **Để cho các trường trạng thái (Status) trôi nổi tự do như một danh sách thả xuống (Drop-down) vô tội vạ, mà không hề có một "Máy trạng thái" (State Machine) và hàng rào phân quyền bảo vệ.**

---

## 2. BẮT BỆNH NGUYÊN LÝ GỐC (ROOT-CAUSE DIAGNOSIS)

Tại sao những sự cố thất thoát dữ liệu và rò rỉ quyền hạn liên tục xảy ra trong các hệ thống doanh nghiệp?

### 2.1. Sự ngây thơ về khái niệm "Trạng thái" (Status vs. State)
Hầu hết mọi người khi dựng Base hay phần mềm đều nghĩ đơn giản: Tạo một trường Single Select mang tên `Trạng thái`, điền vào 5 lựa chọn: `Mới`, `Đang làm`, `Chờ duyệt`, `Hoàn thành`, `Hủy`.

Sau đó, họ để cho tất cả mọi người trong công ty đều có quyền bấm chọn bất kỳ trạng thái nào vào bất kỳ lúc nào. 

Đây là một lỗ hổng an ninh chết người. Trong thực tế vận hành doanh nghiệp:
- Không thể có chuyện một đơn hàng từ `Mới tạo` nhảy cóc một phát sang `Hoàn thành` mà không đi qua bước `Thanh toán` và `Xuất kho`.
- Không thể có chuyện một nhân viên cấp dưới tự ý chuyển trạng thái sang `Đã duyệt chi` mà không có chữ ký của Kế toán trưởng hay Giám đốc.

### 2.2. Khái niệm Máy Trạng Thái (Finite State Machine - FSM)
Trong khoa học máy tính, một **Máy trạng thái** là một mô hình toán học quy định:
1. **Các trạng thái hợp lệ (Valid States)**: Hệ thống chỉ có thể ở một trạng thái duy nhất tại một thời điểm.
2. **Các bước chuyển tiếp hợp lệ (Transitions)**: Chỉ được phép chuyển từ Trạng thái A sang Trạng thái B nếu thỏa mãn **Điều kiện tiên quyết (Guards/Conditions)**.
3. **Người có thẩm quyền kích hoạt (Authorized Triggers)**: Chỉ những vai trò (Roles) cụ thể mới có chìa khóa để bấm nút chuyển trạng thái.

```
MÁY TRẠNG THÁI TIÊU CHUẨN CỦA MỘT ĐƠN HÀNG TRONG COMPANY OS
┌──────────────┐     Nhân viên gửi      ┌──────────────┐
│  1. KHỞI TẠO │ ──────────────────────>│ 2. CHỜ DUYỆT │
└──────────────┘                        └──────┬───────┘
                                               │
                                 Sếp duyệt giá │ (Chiết khấu <= 15%)
                                               ▼
┌──────────────┐      Kế toán xác nhận  ┌──────────────┐
│  4. ĐANG GIAO│ <───────────────────── │  3. ĐÃ DUYỆT │
└──────┬───────┘      tiền vào TK       └──────────────┘
       │
       │ Khách ký biên bản
       ▼
┌──────────────┐
│ 5. HOÀN THÀNH│ (KHÓA TOÀN BỘ QUYỀN SỬA - READ ONLY)
└──────────────┘
```

---

## 3. KHUNG KIẾN TRÚC GIẢI PHÁP (ARCHITECTURAL BLUEPRINT)

Để thiết kế một hệ thống vận hành an toàn tuyệt đối, bạn cần kết hợp **State Machine với Ma trận Phân quyền theo Vai trò (Role-Based Access Control - RBAC)**:

### 3.1. Ma trận Khóa quyền theo Trạng thái (State $\times$ Permission Matrix)
Nguyên tắc vàng: **Càng tiến gần về vạch đích, quyền chỉnh sửa càng phải bị thu hẹp lại.**

| Trạng thái bản ghi | Vai trò: Nhân viên | Vai trò: Trưởng phòng | Vai trò: Kế toán | Vai trò: Giám đốc |
| :--- | :---: | :---: | :---: | :---: |
| **1. Khởi tạo (Draft)** | Toàn quyền sửa | Xem & Góp ý | Không thấy | Xem |
| **2. Chờ duyệt (Pending)** | **Bị khóa (Chỉ xem)** | Được quyền Duyệt/Từ chối | Không thấy | Được quyền Duyệt |
| **3. Đã duyệt (Approved)** | Bị khóa hoàn toàn | Bị khóa hoàn toàn | Được quyền Xác nhận TT | Được quyền Mở lại |
| **4. Hoàn thành (Done)** | **KHÓA 100%** | **KHÓA 100%** | **KHÓA 100%** | **KHÓA 100%** |

Khi một bản ghi đã ở trạng thái `Hoàn thành`, ngay cả Giám đốc cũng không nên tự tiện sửa trực tiếp để bảo toàn tính toàn vẹn của lịch sử kiểm toán. Nếu muốn sửa, phải đi qua một quy trình riêng mang tên `Yêu cầu Mở khóa (Re-open Request)`.

---

## 4. HƯỚNG DẪN DỰNG THỰC TẾ & PROMPTS AI (EXECUTION & PROMPTS)

### Kỹ thuật thiết lập State Machine và RBAC trên Lark Base:
1. **Bước 1: Tách trường Trạng thái ra khỏi tầm tay người dùng**:
   - Không cho phép nhân viên bấm trực tiếp vào cột `Trạng thái`.
   - Cấu hình quyền trường (Field Permission): Đặt trường `Trạng thái` ở chế độ **Read-Only (Chỉ đọc)** cho tất cả nhân viên.
2. **Bước 2: Sử dụng Nút bấm Hành động (Action Buttons) thay vì Drop-down**:
   - Thêm cột kiểu **Button** mang tên `Gửi Duyệt`. Nút này chỉ sáng lên khi các trường bắt buộc đã được điền đủ 100%.
   - Thêm cột Button mang tên `Phê Duyệt` và chỉ phân quyền cho người có vai trò Trưởng phòng được bấm.
3. **Bước 3: Tự động khóa bản ghi bằng Điều kiện lọc (Conditional View Locking)**:
   - Tạo View mang tên `[Nhân viên] Tác vụ Đang Xử Lý` với bộ lọc: `Trạng thái = Khởi tạo`. Khi nhân viên bấm gửi duyệt, bản ghi tự động biến mất khỏi màn hình sửa của họ và bay sang View của sếp.

### 🤖 Prompt AI thiết kế Ma trận Phân quyền & Máy trạng thái:
```markdown
Tôi muốn thiết kế quy trình Phê duyệt Chi phí & Tạm ứng cho công ty quy mô 80 nhân sự trên Lark Base.
Quy trình gồm 4 vai trò: Nhân viên đề xuất, Trưởng bộ phận, Kế toán thanh toán, Tổng Giám đốc.

Hãy đóng vai trò Chuyên gia An ninh Hệ thống & Phân quyền (RBAC Architect):
1. Thiết kế Máy trạng thái (Finite State Machine) gồm các trạng thái hợp lệ và điều kiện chuyển tiếp nghiêm ngặt.
2. Lập Ma trận Phân quyền chi tiết (State-by-Role Permission Matrix) chỉ rõ ai được Xem, ai được Sửa, ai được Duyệt ở từng trạng thái.
3. Hướng dẫn cách cấu hình Field Permission và Button Action trên Lark Base để chống tình trạng nhảy cóc trạng thái hoặc sửa số liệu sau khi đã duyệt.
4. Vẽ sơ đồ luồng State Machine bằng cú pháp Mermaid.
```

---

## 5. BẢNG KIỂM NGHIỆM THU (PRACTITIONER'S CHECKLIST)

| STT | Tiêu chí nghiệm thu bảo mật và trạng thái | Đạt (An toàn) | Rủi ro (Lỗ hổng) |
| :-: | :--- | :-: | :-: |
| 1 | **Chống nhảy cóc**: Nhân viên có thể tự tay đổi trạng thái từ "Khởi tạo" sang "Đã duyệt" được không? | ⬜ Không thể | 🟥 Đổi được dễ dàng |
| 2 | **Khóa bản ghi đã duyệt**: Sau khi sếp duyệt, nhân viên có sửa được số tiền hợp đồng không? | ⬜ Bị khóa cứng | 🟥 Vẫn sửa được |
| 3 | **Cơ chế nút bấm có điều kiện**: Nút bấm duyệt có tự động ẩn đối với những người không có thẩm quyền không? | ⬜ Ẩn đúng người | 🟥 Ai cũng thấy nút |
| 4 | **Lịch sử vết duyệt**: Hệ thống có ghi lại chính xác ai là người bấm duyệt vào giây thứ mấy không? | ⬜ Ghi nhận đầy đủ | 🟥 Không có vết |
