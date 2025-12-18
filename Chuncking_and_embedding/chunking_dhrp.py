
import PyPDF2
from typing import List
import re
import os
from pathlib import Path
from Utilities.utils import PDF_FILE_PATH


def _split_text_into_chunks(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[str]:
    
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return []
    
    if len(sentences) == 1:
        return sentences
    
    chunks = []
    i = 0
    
    while i < len(sentences):
        # Build a chunk by adding complete sentences
        chunk_sentences = []
        chunk_length = 0
        
        while i < len(sentences):
            sentence = sentences[i]
            sentence_length = len(sentence)
            
            # Add sentence if it fits in the chunk size
            if chunk_length + sentence_length + (1 if chunk_sentences else 0) <= chunk_size:
                chunk_sentences.append(sentence)
                chunk_length += sentence_length + (1 if len(chunk_sentences) > 1 else 0)
                i += 1
            else:
                break
        
        # If we couldn't fit even one sentence, add it anyway to avoid infinite loop
        if not chunk_sentences:
            chunk_sentences.append(sentences[i])
            i += 1
        
        chunks.append(' '.join(chunk_sentences))
    
    # Add overlap between chunks (complete sentences from previous chunk)
    if len(chunks) > 1:
        overlapped_chunks = [chunks[0]]
        
        for idx in range(1, len(chunks)):
            prev_chunk = chunks[idx - 1]
            curr_chunk = chunks[idx]
            
            # Split previous chunk into sentences to add overlap
            prev_sentences = re.split(r'(?<=[.!?])\s+', prev_chunk.strip())
            prev_sentences = [s.strip() for s in prev_sentences if s.strip()]
            
            # Calculate how many sentences from previous chunk to overlap
            overlap_sentences = []
            overlap_length = 0
            
            for sent in reversed(prev_sentences):
                if overlap_length + len(sent) + 1 <= chunk_overlap:
                    overlap_sentences.insert(0, sent)
                    overlap_length += len(sent) + 1
                else:
                    break
            
            # Create overlapped chunk
            if overlap_sentences:
                overlapped_chunk = ' '.join(overlap_sentences) + ' ' + curr_chunk
            else:
                overlapped_chunk = curr_chunk
            
            overlapped_chunks.append(overlapped_chunk)
        
        return overlapped_chunks
    
    return chunks


def extract_and_chunk_pdf(
    folder_path: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    by_page: bool = True
) -> List:
    all_chunks = []
    
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' not found or is not a directory.")
        return all_chunks
    
    # Get all PDF files in the folder
    pdf_files = list(Path(folder_path).glob('*.pdf'))
    
    if not pdf_files:
        print(f"No PDF files found in '{folder_path}'")
        return all_chunks
    
    print(f"Found {len(pdf_files)} PDF file(s)")
    
    # Process each PDF file
    for pdf_file in pdf_files:
        file_name = pdf_file.name
        print(f"Processing: {file_name}")
        
        try:
            with open(str(pdf_file), 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract all pages and chunk with page tracking
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    page_chunks = _split_text_into_chunks(text, chunk_size, chunk_overlap)
                    
                    for chunk_idx, chunk_text in enumerate(page_chunks):
                        all_chunks.append({
                            'text': chunk_text,
                            'page': page_num,
                            'file_name': file_name,
                            'chunk_index': chunk_idx
                        })
        
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")
            continue
    
    print(f"Total chunks created: {len(all_chunks)}")
    return all_chunks


extract_and_chunk_pdf(PDF_FILE_PATH)