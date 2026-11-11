# Sign-In Travel Assistant with RAG Chat (Ho Chi Minh City)

## 1. Student Info & City Selection

- **Student Name:** Nguyen Dang Hoang Ngan
- **Student ID:** 25127098

## 2. Setup and Execution

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Copy `.env.example` to `.env` and fill in your keys:

```ini
FIREBASE_API_KEY=your_firebase_api_key
OLLAMA_BASE_URL=https://your-pinggy-tunnel-url.pinggy.link
```

### Step 3: Launch Streamlit App

```bash
streamlit run app.py
```

## 3. Test Results Table

| Question | Type | Expected ID | Retrieved IDs | Correct? | Failure Reason (if wrong) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `What ingredients are in Saigon Com Tam?` | Answerable | `[G11]` | `[G11]`, `[G08]`, `[G02]` | Yes | N/A |
| `Where can I buy local souvenirs in Saigon?` | Answerable | `[G01]` | `[G01]`, `[G07]`, `[G03]` | Yes | N/A |
| `What is special about the Saigon Notre Dame Cathedral?` | Answerable | `[G02]` | `[G02]`, `[G03]`, `[G06]` | Yes | N/A |
| `What style of architecture is the main post office in Saigon` | Paraphrase | `[G03]` | `[G03]` | Yes | N/A |
| `How far is Vung Tau beach from Saigon` | Not in guide | None | `[G10]`, `[G06]`, `[G07]` | Yes | Correctly refused ("I don't know", max score 0.4365 < threshold 0.45) |
| `Tell me about the construction year of the historic post office` | Paraphrase / Missing | `[G03]` | `[G03]`, `[G12]`, `[G02]` | No | Failed at Retrieval/Missing Data (Score 0.3826 < threshold 0.45, text lacks exact year) |

## 4. Limitations & AI Tools Used

- **Limitations:** Vector similarity relies on embedding thresholds. Ambiguous questions with generic keywords may retrieve lower-relevance documents.
- **AI Tools Used:** ChatGPT / Gemini were used to help structure the code architecture, Streamlit UI callbacks, and format Markdown components.

## 5. Demonstration Video Link

- **Demo Video URL:** [Insert Public Link to Video Here]