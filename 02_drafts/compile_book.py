import os

drafts_dir = "/Users/nguyenngocphuc/.gemini/antigravity/scratch/book_company_os/02_drafts"
output_file = os.path.join(drafts_dir, "FULL_MANUSCRIPT_COMPANY_OS.md")

file_order = [
    "00_loi_mo_dau_loi_tu_su_cua_mot_kien_truc_su.md",
    "chapter_01_cai_chet_trang_cua_excel.md",
    "chapter_02_tu_duy_bang_phang_vs_mo_hinh_quan_he.md",
    "chapter_03_nguyen_ly_goc_chuan_hoa_quy_trinh.md",
    "chapter_04_mo_hinh_du_lieu_4_tang_dim_fact_log_rp.md",
    "chapter_05_nghe_thuat_phan_quyen_va_may_trang_thai.md",
    "chapter_06_cong_thong_tin_theo_vai_tro_baseapp.md",
    "chapter_07_tu_chatbot_den_tong_chi_huy_da_tac_nhan.md",
    "chapter_08_xay_dung_ky_nang_ai_va_hang_rao_chong_ao_giac.md",
    "chapter_09_bo_nao_so_ngoai_bien_obsidian_pkm.md",
    "chapter_10_case_study_marketing_va_sales.md",
    "chapter_11_case_study_dieu_phoi_du_an_khach_hang_b2b.md",
    "chapter_12_playbook_ban_giao_va_chuyen_dich_van_hoa_so.md",
    "13_loi_ket_hanh_trinh_chua_dung_lai.md",
    "14_phu_luc_thu_vien_prompt_ai_va_template_blueprint.md"
]

total_words = 0
compiled_content = []

compiled_content.append("# COMPANY OS\n## CẨM NANG XÂY DỰNG HỆ ĐIỀU HÀNH DOANH NGHIỆP TINH GỌN BẰNG LOW-CODE & AI\n*Tác giả: Nguyễn Ngọc Phúc*\n\n---\n\n")

for filename in file_order:
    filepath = os.path.join(drafts_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            words = len(content.split())
            total_words += words
            print(f"Adding {filename}: {words} words")
            compiled_content.append(content)
            compiled_content.append("\n\n---\n\n")
    else:
        print(f"WARNING: Missing file {filename}")

with open(output_file, "w", encoding="utf-8") as out_f:
    out_f.write("".join(compiled_content))

print(f"\n==========================================")
print(f"FULL MANUSCRIPT COMPILED SUCCESSFULLY!")
print(f"Total Words: {total_words:,} words")
print(f"Output File: {output_file}")
print(f"==========================================")
