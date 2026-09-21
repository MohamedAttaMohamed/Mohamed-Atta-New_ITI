"""
Script to generate data/raw/rag_evaluation_handbook.pdf using ReportLab.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def make_pdf():
    output_path = os.path.join("data", "raw", "rag_evaluation_handbook.pdf")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = styles['Title']
    heading_style = styles['Heading2']
    body_style = styles['Normal']

    story.append(Paragraph("RAG Pipeline Evaluation and Optimization Handbook", title_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("1. Evaluation Methodology", heading_style))
    story.append(Paragraph(
        "Evaluating a Retrieval-Augmented Generation (RAG) system requires assessing two key aspects: "
        "Retrieval Quality and Generation Faithfulness. Retrieval quality measures whether the vector store "
        "returns chunks containing the ground-truth answer. Generation faithfulness measures whether the LLM "
        "answers strictly based on the retrieved context without hallucinating external information.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Groundedness and Citation Testing", heading_style))
    story.append(Paragraph(
        "Groundedness ensures that every claim made in the generated answer directly maps to a retrieved source chunk. "
        "Auditable source citations (e.g., referencing source filenames like 'ai_rag_overview.txt') are verified "
        "during test suite execution. Failure cases typically occur when retrieval top_k is set too small or when chunk "
        "boundaries split key entities across separate fragments.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Mitigation Strategies", heading_style))
    story.append(Paragraph(
        "To mitigate context fragmentation, implement fixed-size chunking with overlapping windows (e.g., 800 characters "
        "with 150 characters overlap). To mitigate hallucination, enforce strict prompt system instructions requiring the model "
        "to state 'I don't know' if the answer is not present in the context.",
        body_style
    ))

    doc.build(story)
    print(f"Successfully generated PDF: {output_path}")

if __name__ == "__main__":
    make_pdf()
