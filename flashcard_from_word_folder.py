
import os
import json
import re
from docx import Document
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Global flashcard list
all_flashcards = []

def extract_flashcards_from_docx(doc_path):
    """
    Extract flashcards from a .docx file by using each heading as the question and the text under it as the answer.
    """
    try:
        doc = Document(doc_path)
    except Exception as e:
        print(f"[Warning] Skipping file (not a valid .docx): {doc_path} ({e})")
        return []

    flashcards = []
    current_question = None
    current_answer = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # If this paragraph is a heading, treat as a new question
        if para.style.name.startswith("Heading"):
            if current_question and current_answer:
                flashcards.append({
                    "question": current_question,
                    "answer": "\n".join(current_answer)
                })
            current_question = text
            current_answer = []
        else:
            current_answer.append(text)

    # Add the last flashcard if any
    if current_question and current_answer:
        flashcards.append({
            "question": current_question,
            "answer": "\n".join(current_answer)
        })

    return flashcards

def generate_flashcards():
    global all_flashcards
    folder = filedialog.askdirectory(title="Select Folder with Word Files")
    if not folder:
        return

    all_flashcards = []
    for filename in os.listdir(folder):
        if filename.endswith(".docx"):
            path = os.path.join(folder, filename)
            flashcards = extract_flashcards_from_docx(path)
            all_flashcards.extend(flashcards)

    if not all_flashcards:
        messagebox.showinfo("No Flashcards", "No questions found in .docx files.")
        return

    output_file = os.path.join(folder, "flashcards.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_flashcards, f, ensure_ascii=False, indent=2)

    messagebox.showinfo("Success", f"✅ {len(all_flashcards)} flashcards saved to:\n{output_file}")

def search_flashcards():
    keyword = search_entry.get().strip().lower()
    result_text.delete("1.0", tk.END)

    if not keyword:
        result_text.insert(tk.END, "⚠️ Enter a keyword to search.")
        return

    matched = [f for f in all_flashcards if keyword in f["question"].lower() or keyword in f["answer"].lower()]
    
    if not matched:
        result_text.insert(tk.END, "❌ No results found.")
        return

    for i, card in enumerate(matched, 1):
        result_text.insert(tk.END, f"{i}. {card['question']}\n{card['answer']}\n\n")

# GUI
root = tk.Tk()
root.title("📄 Flashcard Maker & Search")
root.geometry("700x600")


# Generate button
btn_gen = tk.Button(root, text="📂 Load .docx & Generate Flashcards", command=generate_flashcards, bg="green", fg="white", height=2)
btn_gen.pack(pady=10)

# Load JSON button
def load_json_flashcards():
    global all_flashcards
    file_path = filedialog.askopenfilename(title="Select flashcards JSON file", filetypes=[("JSON Files", "*.json")])
    if not file_path:
        return
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            all_flashcards = json.load(f)
        messagebox.showinfo("Loaded", f"✅ Loaded {len(all_flashcards)} flashcards from JSON.")
        result_text.delete("1.0", tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load JSON: {e}")
        all_flashcards = []

btn_load_json = tk.Button(root, text="📑 Load Existing flashcards.json", command=load_json_flashcards, bg="#FFC107", fg="black", height=2)
btn_load_json.pack(pady=5)

# Search bar
search_frame = tk.Frame(root)
search_frame.pack(pady=5)
search_label = tk.Label(search_frame, text="🔍 Search Topic:")
search_label.pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side=tk.LEFT, padx=5)
btn_search = tk.Button(search_frame, text="Search", command=search_flashcards, bg="#2196F3", fg="white")
btn_search.pack(side=tk.LEFT)

# Results box
result_text = scrolledtext.ScrolledText(root, width=80, height=25)
result_text.pack(padx=10, pady=10)

root.mainloop()
