# Lab 03: Sign-In Travel Assistant with RAG Chat (Ho Chi Minh City)

## 1. Student Info & City Selection

- **Student Name:** Nguyen Dang Hoang Ngan
- **Student ID:** 25127098
- **Class:** 25C09
- **Chosen City:** Ho Chi Minh City


## 2. Setup and Execution

### Step 1: Start the Ollama Backend (Google Colab + Pinggy)

This application connects to a remote Ollama server hosted on Google Colab rather than running heavy models locally:

1. Open the Ollama server notebook on Google Colab and ensure both required models (`embeddinggemma` for embeddings and `qwen3:4b` for text generation) are pulled and running.

2. Expose port `11434` via Pinggy in the Colab terminal:

   ```bash
   ssh -p 443 -R0:localhost:11434 -t qr@free.pinggy.io "u:Host:localhost:11434"
   ```

3. Copy the generated public HTTPS URL (e.g., `https://xxxx.run.pinggy-free.link`).

### Step 2: Install Local Dependencies

Clone the repository, navigate to the project folder, and install the required Python packages (such as `streamlit`, `requests`, `numpy`, and `python-dotenv`):

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Firebase Authentication & Environment Variables
1. In the [Firebase Console](https://console.firebase.google.com/), create a project (or reuse your Lab 3 project), go to **Authentication $\rightarrow$ Sign-in method**, and enable **Email/Password**.
2. Create a test user under the **Users** tab, then copy your **Web API Key** from **Project Settings $\rightarrow$ General**.
3. Create `.env` in the root directory and fill in your credentials:

```ini
FIREBASE_API_KEY=your_firebase_api_key
OLLAMA_BASE_URL=[https://your-pinggy-tunnel-url.pinggy.link](https://your-pinggy-tunnel-url.pinggy.link)
```

### Step 4: Launch the Streamlit App

Run the application locally:

```bash
streamlit run app.py
```

Once started, open the local URL shown in your terminal (typically `http://localhost:8501`), sign in with a registered Firebase Email/Password account, and begin asking questions about Ho Chi Minh City.

## 3. Test Results Table

| Question | Type | Expected ID | Retrieved IDs | Correct? | Failure Reason (if wrong) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `What ingredients are in Saigon Com Tam?` | Answerable | `[G11]` | `[G11]`, `[G08]`, `[G02]` | Yes | N/A |
| `Where can I buy local souvenirs in Saigon?` | Answerable | `[G01]` | `[G01]`, `[G07]`, `[G03]` | Yes | N/A |
| `What is special about the Saigon Notre Dame Cathedral?` | Answerable | `[G02]` | `[G02]`, `[G03]`, `[G06]` | Yes | N/A |
| `What style of architecture is the main post office in Saigon` | Paraphrase | `[G03]` | `[G03]` , `[G05]`, `[G02]` | Yes | N/A |
| `How far is Vung Tau beach from Saigon` | Not in guide | None | `[G10]`, `[G06]`, `[G07]` | Yes | Correctly refused ("I don't know", max score 0.4365 < threshold 0.45) |
| `Tell me about the construction year of the historic post office` | Not in guide (Paraphrase / Missing) | `[G03]` | `[G03]`, `[G12]`, `[G02]` | No | Failed at Retrieval/Missing Data (Score 0.3826 < threshold 0.45, text lacks exact year) |

## 4. Limitations & AI Tools Used

- **Limitations:** Vector similarity relies on embedding thresholds. Ambiguous questions with generic keywords may retrieve lower-relevance documents.
- **AI Tools Used:** ChatGPT / Gemini were used to help structure the code architecture, Streamlit UI callbacks, and format Markdown components.

## 5. Demonstration Video Link

- **Demo Video URL:** [Insert Public Link to Video Here]