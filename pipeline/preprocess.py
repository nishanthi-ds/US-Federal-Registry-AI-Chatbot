
import aiohttp
import fitz  # PyMuPDF
import pandas as pd
import fitz  # PyMuPDF - used for reading PDF files
import re
import asyncio

# Normalize font name to remove styles like Italic or Oblique (for consistency)
def normalize_font(font_name):
    return re.sub(r'[-\s]?(Italic|Oblique)', '', font_name, flags=re.IGNORECASE)


# Function to decide whether a line should be ignored
def is_irrelevant_line(line):

    # Keywords that indicate noisy header/footer lines to ignore
    LINE_IGNORE_KEYWORDS = [
        "federal register / vol.", 
        "[fr doc.", 
        "billing code"
    ]

    line_lower = line.lower().strip()
    if any(key in line_lower for key in LINE_IGNORE_KEYWORDS):
        return True
    if re.fullmatch(r"[\d\s]+", line):  # If it contains only digits or spaces (e.g., page numbers)
        return True
    if re.findall(r"[a-zA-Z]:\\[^\s\n]+", line):  # Looks like a file path (Windows format)
        return True
    return False

# Main function to extract and clean structured text from PDF
def extract_text_clean(pdf_data):

    # Open the PDF from bytes
    doc = fitz.open(stream=pdf_data, filetype="pdf")
    # doc = fitz.open(pdf_path)  # Open PDF
    full_text = []  # Final cleaned paragraphs list
    current_paragraph = ""  # Temporary storage for building paragraph
    previous_y = None  # Used to calculate vertical gap between lines
    last_line_ended_with_dot = False  # Helps detect sentence-ending lines

    # Regex pattern to detect lines that likely begin new paragraphs
    NEW_PARAGRAPH_START_RE = re.compile(r'^\(?\d{1,2}\)|^\d{1,2}\.|^Section\b|^Article\b|^Sec\.\b', re.IGNORECASE)

    for page in doc:
        blocks = page.get_text("dict")["blocks"]  # Get text blocks from the page
        for block in blocks:
            if block["type"] != 0:
                continue  # Skip non-text blocks

            for line in block["lines"]:
                line_text = ""
                line_y = line["bbox"][1]  # Get vertical position of the line
                line_sizes = set()  # Store font sizes used in the line

                for span in line["spans"]:
                    if span["size"] < 7:
                        continue  # Skip very small text (likely footnotes)
                    #font = normalize_font(span["font"])
                    line_sizes.add(round(span["size"], 1))  # Track the font size
                    text = span["text"].strip()
                    if not text:
                        continue
                    # Combine span texts to form the full line
                    line_text += " " + text if line_text else text

                line_text = line_text.strip()
                if not line_text or is_irrelevant_line(line_text):
                    continue  # Skip blank or unwanted lines

                # Determine if the line starts a new paragraph
                is_new_para = False
                if previous_y is not None and line_sizes:
                    line_gap = line_y - previous_y
                    max_size = max(line_sizes)
                    if line_gap > 1.5 * max_size:  # Large gap indicates new para
                        is_new_para = True

                if NEW_PARAGRAPH_START_RE.match(line_text):  # Matches numbered/section lines
                    is_new_para = True

                # Paragraph building logic
                if current_paragraph:
                    if is_new_para or (last_line_ended_with_dot and line_text[0].isupper()):
                        full_text.append(current_paragraph.strip())
                        current_paragraph = line_text
                    else:
                        current_paragraph += " " + line_text
                else:
                    current_paragraph = line_text

                previous_y = line_y
                last_line_ended_with_dot = line_text.endswith(('.', '!', '?'))

    # Append any remaining paragraph
    if current_paragraph:
        full_text.append(current_paragraph.strip())

    return "\n".join(full_text)

# === Asynchronous download & extract function (your format) ===
async def fetch_and_process(session, pdf_url, idx):
    try:
        # print(f"Fetching PDF for row {idx}")
        async with session.get(pdf_url) as response:
            if response.status == 200:
                pdf_data = await response.read()
                return extract_text_clean(pdf_data)
            else:
                print(f"Failed to fetch row {idx}: HTTP {response.status}")
                return ""
    except Exception as e:
        print(f"Error at row {idx}: {e}")
        return ""
    
# === Main runner ===
async def process_pdfs(df):
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_and_process(session, row["pdf_url"], idx)
            for idx, row in df.iterrows()
        ]
        return await asyncio.gather(*tasks)
