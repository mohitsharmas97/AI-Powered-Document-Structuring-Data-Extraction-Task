import os
from services.pdf_reader import extract_pdf_text
from services.gemini_processor import extract_key_value_pairs
from services.excel_writer import write_to_excel

def process_document():
    # Setup paths
    input_folder = "uploads"
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # Find PDF
    files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]
    if not files:
        print("❌ No PDF found in 'input' folder.")
        return

    pdf_path = os.path.join(input_folder, files[0])
    print(f"📄 Processing: {files[0]}")

    # 1. Extract Text
    text = extract_pdf_text(pdf_path)
    
    # 2. Get Data from AI
    json_data = extract_key_value_pairs(text)
    
    # 3. Save to Excel
    output_file = os.path.join(output_folder, files[0].replace(".pdf", ".xlsx"))
    write_to_excel(json_data, output_file)
    print(f"🎉 Done! Saved to {output_file}")

if __name__ == "__main__":
    process_document()