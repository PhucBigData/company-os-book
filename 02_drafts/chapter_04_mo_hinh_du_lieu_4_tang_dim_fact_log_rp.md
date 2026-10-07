# CHƯƠNG 4: MÔ HÌNH DỮ LIỆU 4 TẦNG (DIM - FACT - LOG - RP)

---

## 1. CÂU CHUYỆN CHIẾN TRƯỜNG (THE WAR STORY)

Tháng 6 năm 2026, tôi được một chuỗi F&B 18 chi nhánh tại TP.HCM nhờ "cứu viện". Họ vừa tự hào chuyển đổi từ Excel lên Lark Base được 4 tháng. Nhưng niềm vui ngắn chẳng tày gang: 

Hệ thống Base của họ bắt đầu quay tròn như chong chóng mỗi lần mở. Các bảng tính tải mất 15 giây, công thức thỉnh thoảng báo lỗi `#CIRCULAR_REFERENCE` (tham chiếu vòng lặp), và tệ nhất là các con số báo cáo doanh thu tuần nhảy loạn xạ không kiểm soát được.

Tôi mở cấu trúc Base của họ ra. Đập vào mắt tôi là một mớ hỗn độn kỹ thuật:
- Trong một bảng duy nhất có tên `Doanh_Thu_Tong_Hop`, họ nhét vào:
  - 10 cột thông tin chi nhánh (Tên quán, địa chỉ, người quản lý, số bàn).
  - 25 cột đơn hàng bán ra mỗi ngày.
  - 15 cột công thức tính chi phí nguyên vật liệu, tiền điện nước.
  - Và ở ngay dưới đáy bảng, họ thêm vào các dòng đặc biệt mang tên: `TỔNG CỘNG TUẦN 1`, `TỔNG CỘNG THÁNG 5`, `TRUNG BÌNH CỘNG CHI NHÁNH A`.

Khi số lượng đơn hàng vượt qua mốc 30,000 bản ghi, hệ thống sụp đổ vì quá tải tính toán. 

Người dựng Base (một bạn IT trẻ) phân trần: *"Em thấy trên Excel người ta hay viết dòng Tổng cộng ở cuối bảng, nên sang Base em cũng làm y như vậy cho sếp dễ nhìn..."*

Tôi thở dài: *"Em đang mang toàn bộ tư duy 'rác' của bảng tính thế kỷ trước để áp đặt lên một cơ sở dữ liệu hiện đại. Trong một cơ sở dữ liệu chuẩn mực, **dữ liệu giao dịch phát sinh không bao giờ được phép sống chung một nhà với dữ liệu báo cáo tổng hợp**."*

Đó là lúc tôi áp dụng mô hình kiến trúc cốt lõi của Company OS: **Mô hình Dữ liệu 4 Tầng: DIM - FACT - LOG - RP**.

---

## 2. BẮT BỆNH NGUYÊN LÝ GỐC (ROOT-CAUSE DIAGNOSIS)

Tại sao hầu hết các hệ thống tự dựng trên Lark Base, Airtable hay Notion sau 3-6 tháng đều bị "phình to", chậm chạp và gãy đổ?

Bởi vì người dựng không hiểu về **vòng đời và bản chất vật lý của dữ liệu**.

Trong bất kỳ doanh nghiệp nào, dữ liệu sinh ra luôn thuộc về một trong bốn nhóm hoàn toàn khác biệt nhau về tần suất thay đổi, quy mô lưu trữ và mục đích sử dụng:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. DIM (DIMENSION) - TẦNG DANH MỤC MASTER DATA                              │
│    • Dữ liệu tĩnh, ít biến động (Khách hàng, Sản phẩm, Chi nhánh, Nhân sự)  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Link
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. FACT (TRANSACTIONS) - TẦNG GIAO DỊCH PHÁT SINH                           │
│    • Dữ liệu động, phình to theo thời gian (Đơn hàng, Tác vụ, Xuất nhập kho)│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Trigger / Rollup
                       ┌───────────────┴───────────────┐
                       ▼                               ▼
┌──────────────────────────────────────┐  ┌───────────────────────────────────┐
│ 3. LOG (AUDIT LOGS)                  │  │ 4. RP (REPORTING & AGGREGATE)     │
│    • Nhật ký vết, bất biến           │  │    • Báo cáo tổng hợp, snapshot   │
│    • Lưu lịch sử chuyển trạng thái   │  │    • KPI tuần, doanh thu tháng    │
└──────────────────────────────────────┘  └───────────────────────────────────┘
```

---

## 3. KHUNG KIẾN TRÚC GIẢI PHÁP (ARCHITECTURAL BLUEPRINT)

Hãy mổ xẻ chi tiết 4 tầng dữ liệu chuẩn Company OS:

### 3.1. Tầng 1: DIM (Dimension Tables - Bảng Danh Mục Gốc)
- **Bản chất**: Đây là "khung xương" của doanh nghiệp. Nó lưu trữ các thực thể cốt lõi mà công ty sở hữu hoặc quản lý.
- **Đặc điểm**: Số lượng bản ghi ít (vài chục đến vài nghìn dòng), tần suất thêm mới rất thấp, nhưng tần suất được đọc và liên kết thì liên tục.
- **Ví dụ**:
  - `[DIM] Khách Hàng`: Mã KH, Tên, Số điện thoại, Phân hạng VIP.
  - `[DIM] Sản Phẩm`: Mã SKU, Tên sản phẩm, Giá niêm yết, Đơn vị tính.
  - `[DIM] Nhân Sự`: Mã NV, Họ tên, Phòng ban, Chức vụ, Email.
  - `[DIM] Chi Nhánh`: Mã kho/quán, Địa chỉ, Quản lý phụ trách.

### 3.2. Tầng 2: FACT (Fact/Transaction Tables - Bảng Giao Dịch Thực Tế)
- **Bản chất**: Đây là "dòng máu" chảy trong huyết mạch doanh nghiệp. Bất kỳ khi nào một hành động kinh doanh phát sinh, một dòng FACT được sinh ra.
- **Đặc điểm**: Phình to rất nhanh (hàng nghìn đến hàng trăm nghìn dòng mỗi tháng). Mỗi dòng FACT bắt buộc phải gắn (Link) với ít nhất một hoặc nhiều bảng DIM.
- **Ví dụ**:
  - `[FACT] Đơn Hàng`: Ngày tạo, Link tới `[DIM] Khách Hàng`, Link tới `[DIM] Chi Nhánh`, Tổng tiền.
  - `[FACT] Chi Tiết Đơn Hàng`: Link tới `[FACT] Đơn Hàng`, Link tới `[DIM] Sản Phẩm`, Số lượng bán, Đơn giá thực tế.
  - `[FACT] Tác Vụ Sản Xuất`: Ngày giao, Link tới `[DIM] Nhân Sự`, Trạng thái hoàn thành.

### 3.3. Tầng 3: LOG (Audit & System Logs - Bảng Nhật Ký Vết)
- **Bản chất**: Đây là "hộp đen máy bay" của hệ thống. Nó ghi lại toàn bộ sự biến thiên trạng thái của các dòng FACT nhằm mục đích kiểm toán và chống gian lận.
- **Đặc điểm**: Bất biến (Append-only) — chỉ thêm mới, tuyệt đối không ai được sửa hoặc xóa.
- **Ví dụ**:
  - `[LOG] Trạng Thái Đơn Hàng`: Mã đơn, Trạng thái cũ (*Chờ duyệt*), Trạng thái mới (*Đã duyệt*), Người thực hiện, Thời điểm chính xác (Timestamp).

### 3.4. Tầng 4: RP (Reporting & Aggregate Tables - Bảng Tổng Hợp Báo Cáo)
- **Bản chất**: Đây là "bảng điều khiển taplo" dành cho CEO và các Trưởng phòng. Nó không chứa từng giao dịch lẻ, mà chỉ chứa các con số tổng hợp theo chu kỳ thời gian.
- **Đặc điểm**: Mỗi dòng đại diện cho một chu kỳ: `Tuần 40/2026`, `Tháng 09/2026`, hoặc `Quý 3/2026`.
- **Cơ chế hoạt động**: Sử dụng các trường **Rollup có điều kiện lọc** từ bảng FACT để tính: Tổng doanh thu, Số đơn thành công, Tỷ lệ hủy đơn, Chi phí bình quân.

---

## 4. HƯỚNG DẪN DỰNG THỰC TẾ & PROMPTS AI (EXECUTION & PROMPTS)

### Quy trình 3 bước triển khai mô hình 4 tầng trên Lark Base:
1. **Quy tắc đặt tên (Naming Convention)**:  
   Luôn gắn tiền tố vào tên bảng để bất kỳ ai mở Base ra cũng hiểu ngay vai trò:  
   `DIM_KhachHang`, `DIM_SanPham`, `FACT_DonHang`, `LOG_ThayDoiTrangThai`, `RP_BaoCaoTuan`.
2. **Kỹ thuật Rollup thông minh ở bảng RP**:
   - Trong bảng `RP_BaoCaoTuan`, tạo trường Link trỏ về `FACT_DonHang`.
   - Tạo trường Rollup: Hàm `SUM(Thành tiền)` với điều kiện lọc `Trạng thái = Đã hoàn thành`.
   - Tạo trường Rollup thứ hai: Hàm `COUNT(Mã đơn)` với điều kiện lọc `Trạng thái = Đã hủy`.
   - Tạo trường Formula: `Tỷ lệ hủy = [Đơn hủy] / ([Đơn thành công] + [Đơn hủy])`.
3. **Cơ chế Auto-Logging bằng Automation**:
   - Cấu hình Automation Trigger: *Khi một bản ghi trong `FACT_DonHang` thay đổi trường `Trạng thái`*.
   - Action: *Tạo bản ghi mới trong bảng `LOG_ThayDoiTrangThai`* ghi lại ai đổi, từ trạng thái nào sang trạng thái nào.

### 🤖 Prompt AI thiết kế kiến trúc 4 tầng chuẩn Company OS:
```markdown
Tôi muốn xây dựng hệ thống quản lý vận hành bán hàng và kho cho công ty thời trang 5 chi nhánh.
Hãy đóng vai trò Principal Data Architect, thiết kế kiến trúc Lark Base theo mô hình 4 tầng DIM - FACT - LOG - RP:
1. Phân loại rõ ràng danh sách các bảng thuộc tầng DIM (Danh mục), FACT (Giao dịch), LOG (Nhật ký) và RP (Báo cáo).
2. Chi tiết các trường (fields) quan trọng cho từng bảng kèm kiểu dữ liệu (Text, Number, Single Select, Link, Lookup, Rollup, Formula).
3. Hướng dẫn cơ chế liên kết Link giữa các tầng để số liệu từ FACT tự động tổng hợp về RP mà không làm chậm hệ thống.
4. Xuất sơ đồ quan hệ thực thể (ERD) bằng cú pháp Mermaid.
```

---

## 5. BẢNG KIỂM NGHIỆM THU (PRACTITIONER'S CHECKLIST)

| STT | Tiêu chuẩn nghiệm thu kiến trúc 4 tầng | Đạt | Vi phạm |
| :-: | :--- | :-: | :-: |
| 1 | **Tách biệt báo cáo**: Có dòng nào mang tính chất "Tổng cộng / Trung bình" nằm chung trong bảng giao dịch FACT không? | ⬜ Đã tách sang RP | 🟥 Vẫn nhét chung |
| 2 | **Khóa danh mục DIM**: Bảng danh mục DIM có được phân quyền nghiêm ngặt để nhân viên bình thường không tự tiện thêm bừa bãi không? | ⬜ Đã khóa quyền | 🟥 Ai cũng thêm được |
| 3 | **Cơ chế vết kiểm toán**: Khi có tranh chấp hoặc nhầm lẫn số liệu, có bảng LOG ghi lại lịch sử thay đổi không? | ⬜ Có bảng LOG | 🟥 Không có vết |
| 4 | **Hiệu năng tải trang**: Toàn bộ hệ thống có tải mượt mà dưới 3 giây không? | ⬜ Dưới 3s | 🟥 Quay trên 10s |
