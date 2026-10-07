import os
import glob
import json

vault_path = os.path.expanduser("~/Documents/Obsidian Vault")
lark_scan_file = "/Users/nguyenngocphuc/.gemini/antigravity/scratch/lark_scan_results.json"
skills_dir = os.path.expanduser("~/.gemini/config/skills")

book_index = {
    "project": "COMPANY OS Book",
    "total_raw_notes_mapped": 0,
    "chapters_material_map": {
        "Chapter_01_Crisis_of_Excel": {
            "title": "Cái Chết Trắng Của Những File Excel 100 Cột",
            "obsidian_sources": [],
            "lark_sources": ["Docx 1.1 Quản lý dự án", "Docx 1.2 Tổng hợp công việc"],
            "core_themes": ["Sự phình to của bảng tính", "Nghẽn cổ chai vận hành", "Mất mát dữ liệu khi nhân sự nghỉ"]
        },
        "Chapter_02_Flat_vs_Relational": {
            "title": "Tư Duy Bảng Phẳng vs. Mô Hình Quan Hệ (First Principles)",
            "obsidian_sources": [],
            "lark_sources": ["Bảng tính Thái Dương", "ERD concepts"],
            "core_themes": ["Sự khác nhau giữa Sheet và Database", "Chuẩn hóa dữ liệu 3NF", "Khái niệm thực thể"]
        },
        "Chapter_03_First_Principles_Process": {
            "title": "Nguyên Lý Gốc: Chuẩn Hóa Quy Trình Trước Khi Mua Công Cụ",
            "obsidian_sources": [],
            "lark_sources": ["SOP templates", "Decision notes"],
            "core_themes": ["Bẫy mua phần mềm", "BPMN & Swimlane ranh giới trách nhiệm", "RACI matrix"]
        },
        "Chapter_04_DIM_FACT_LOG_RP_Model": {
            "title": "Mô Hình Dữ Liệu 4 Tầng (DIM - FACT - LOG - RP)",
            "obsidian_sources": [],
            "lark_sources": ["Base Giang Anh 7 bảng", "Base Nobelik", "Bitable schemas"],
            "core_themes": ["Dimension tables", "Fact tables", "Audit Log", "Reporting aggregation", "Formula & Rollup"]
        },
        "Chapter_05_State_Machines_and_Approvals": {
            "title": "Nghệ Thuật Phân Quyền & Thiết Kế Máy Trạng Thái (State Machine)",
            "obsidian_sources": [],
            "lark_sources": ["Approval Blueprint Builder", "Lark Approval native"],
            "core_themes": ["Vòng đời bản ghi", "472 quy chuẩn duyệt", "Điều kiện rẽ nhánh ma trận phê duyệt", "RBAC"]
        },
        "Chapter_06_Role_Based_BaseApp": {
            "title": "Cổng Thông Tin Theo Vai Trò (Role-Based BaseApp & Portal)",
            "obsidian_sources": [],
            "lark_sources": ["BaseApp Pages", "AppMode Blocks", "Portal Marketing Nobelik"],
            "core_themes": ["Giao diện CEO Dashboard vs Quản lý vs Nhân viên", "Biểu mẫu nhập liệu động", "Trải nghiệm UX"]
        },
        "Chapter_07_From_Chatbot_to_Multi_Agent": {
            "title": "Từ Chatbot Giải Trí Đến Tổng Chỉ Huy Đa Tác Nhân (Agentic AI)",
            "obsidian_sources": [],
            "lark_sources": ["Codex CLI logs", "Antigravity transcripts"],
            "core_themes": ["Thoát khỏi bẫy prompt chat đơn giản", "Kiến trúc Multi-Agent", "Dual-Tier Model Routing"]
        },
        "Chapter_08_Custom_AI_Skills_and_Guardrails": {
            "title": "Xây Dựng Kỹ Năng AI Tùy Biến (Custom Skills) & Hàng Rào Chống Ảo Giác",
            "obsidian_sources": [],
            "lark_sources": ["41 Custom Skills", "SKILL.md architecture", "Completion Gate"],
            "core_themes": ["Đặc tả kỹ năng", "Anti-hallucination protocols", "Fail-fast verification"]
        },
        "Chapter_09_External_Brain_PKM": {
            "title": "Xây Dựng Bộ Não Số Ngoại Biên: Kết Hợp Markdown, PKM & AI",
            "obsidian_sources": [],
            "lark_sources": ["Obsidian Vault architecture", "Atomic Notes", "Graph view"],
            "core_themes": ["Personal Knowledge Management", "Liên kết hai chiều", "Không bao giờ mất tri thức"]
        },
        "Chapter_10_Marketing_and_Sales_Case": {
            "title": "Case Study 1: Số Hóa Vận Hành Phòng Marketing & Kênh Bán Hàng",
            "obsidian_sources": [],
            "lark_sources": ["Base Giang Anh Marketing", "Base Nobelik", "Leads tracking"],
            "core_themes": ["Kế hoạch nội dung", "Tác vụ media", "Đo lường lead & ROI"]
        },
        "Chapter_11_Project_Delivery_Case": {
            "title": "Case Study 2: Điều Phối Dự Án Khách Hàng B2B Diện Rộng",
            "obsidian_sources": [],
            "lark_sources": ["65 Client groups", "Lark Tasks 525 jobs", "Minutes consultation"],
            "core_themes": ["Kỷ luật thực thi 99.8%", "Không trôi deadline", "Quản trị kỳ vọng khách hàng"]
        },
        "Chapter_12_Handover_Playbook_Culture": {
            "title": "Bộ Playbook Bàn Giao & Chuyển Dịch Văn Hóa Số Doanh Nghiệp",
            "obsidian_sources": [],
            "lark_sources": ["137 Wiki Spaces", "Playbook triển khai Lark 15 phần", "Cộng đồng Chuyển đổi số"],
            "core_themes": ["Chống đối thay đổi", "Đào tạo nhân sự dùng hệ thống", "Duy trì văn hóa vận hành số"]
        }
    }
}

# Scan Obsidian notes and map
if os.path.exists(vault_path):
    for root, dirs, files in os.walk(vault_path):
        if ".obsidian" in root or ".trash" in root or ".smart-env" in root:
            continue
        rel = os.path.relpath(root, vault_path)
        for f in files:
            if f.endswith(".md"):
                fp = os.path.join(root, f)
                book_index["total_raw_notes_mapped"] += 1
                if "Approval Queue" in rel:
                    book_index["chapters_material_map"]["Chapter_05_State_Machines_and_Approvals"]["obsidian_sources"].append(f)
                elif "Lark Base" in rel:
                    book_index["chapters_material_map"]["Chapter_04_DIM_FACT_LOG_RP_Model"]["obsidian_sources"].append(f)
                    book_index["chapters_material_map"]["Chapter_06_Role_Based_BaseApp"]["obsidian_sources"].append(f)
                elif "Projects" in rel or "Project Recaps" in rel:
                    book_index["chapters_material_map"]["Chapter_11_Project_Delivery_Case"]["obsidian_sources"].append(f)
                elif "Decisions" in rel or "Weekly Reviews" in rel:
                    book_index["chapters_material_map"]["Chapter_01_Crisis_of_Excel"]["obsidian_sources"].append(f)
                    book_index["chapters_material_map"]["Chapter_03_First_Principles_Process"]["obsidian_sources"].append(f)
                elif "Knowledge" in rel or "Templates" in rel:
                    book_index["chapters_material_map"]["Chapter_09_External_Brain_PKM"]["obsidian_sources"].append(f)

# Truncate lists in display for readability
summary_counts = {}
for ch, data in book_index["chapters_material_map"].items():
    summary_counts[ch] = {
        "title": data["title"],
        "obsidian_notes_count": len(data["obsidian_sources"]),
        "lark_sources": data["lark_sources"]
    }

out_path = "/Users/nguyenngocphuc/.gemini/antigravity/scratch/book_company_os/01_raw_materials/raw_material_mapping.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(book_index, f, ensure_ascii=False, indent=2)

print(f"Mapped {book_index['total_raw_notes_mapped']} raw Obsidian notes!")
print(json.dumps(summary_counts, ensure_ascii=False, indent=2))
