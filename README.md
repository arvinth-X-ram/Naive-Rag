Credit Risk RAG Assistant
Overview
1. The Credit Risk RAG Assistant is a Retrieval-Augmented Generation (RAG) system designed to support credit risk analysis and credit decisioning using an institution’s internal credit risk knowledge base.
2. The system strictly enforces policy-driven decisioning and does not use external knowledge, assumptions, judgment, or market practices. Every output is explicitly grounded in retrieved internal documents.
---
Scope and Responsibility
The assistant’s sole responsibility is to:
1. Answer credit risk–related questions
2. Evaluate credit requests
3. Make credit decisions
---
All outputs are:
Fully supported by retrieved internal knowledge
Produced after a mandatory retrieval step
Auditable and explainable
---
Operating Modes
1. Information Mode
    Activated when no customer-specific data is provided.
2. Decision Mode
    Activated when customer data is provided.

Decision outcomes:
1. APPROVE
2. CONDITIONAL APPROVAL
3. REJECT
4. ESCALATE
---
Mandatory Retrieval Rule
Exactly one retrieval tool must be called before answering.
<table border="1" cellpadding="8" cellspacing="0">
    <thead>
        <tr>
            <th>Tool Name</th>
            <th>Usage</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>fts_search</strong></td>
            <td>
                Exact policy names, credit products, acronyms (PD, LGD, LTV, DTI, RWA),
                frameworks, and model names
            </td>
        </tr>
        <tr>
            <td><strong>query_document</strong></td>
            <td>
                Conceptual or descriptive questions and general eligibility criteria
            </td>
        </tr>
        <tr>
            <td><strong>_hybrid_search</strong></td>
            <td>
                Customer-specific approval scenarios, multi-condition, or complex queries
            </td>
        </tr>
    </tbody>
</table>

---
Folder Structure
```
src/
├── api/
│   └── v1/
│       ├── routes/query.py
│       ├── agents/agents.py
│       ├── schemas/query_schema.py
│       └── tools/
│           ├── fts_search_tool.py
│           ├── hybrid_search_tool.py
│           └── vector_search_tool.py
├── ingestion/ingestion.py
├── core/db.py
├── streamlit_ui/ui.py
├── uploaded_pdfs/
├── main.py
├── pyproject.toml
├── uv.lock
├── .env
└── README.md
```
---
Setup
```bash
git clone <repository-url>
cd <repository-name>
uv sync
```
---
Run Backend
```bash
uv run uvicorn main:app --reload
```
Run UI
```bash
streamlit run ./streamlit_ui/ui.py
```
---

==== TCS Confidential ====