# 📝 AI Meeting Preparation Agent

**Empower your meetings with multi-agent intelligence. Turn hours of research into minutes of strategy.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg.svg)](https://streamlit.io/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/Framework-CrewAI-red.svg)](https://crewai.com)
[![Anthropic](https://img.shields.io/badge/LLM-Claude--3.5--Sonnet-orange.svg)](https://anthropic.com)

---

## 🚀 Overview

The **AI Meeting Preparation Agent** is a sophisticated multi-agent system built with **CrewAI** and **Streamlit**. It is designed to bridge the "Intelligence Gap" in high-stakes business meetings. Unlike generic AI summaries, this agent is **perspective-aware**—it re-aligns its entire research and strategy engine based on whether you are **pitching a client** or **evaluating a vendor**.

### 💡 The Value Proposition
Most professionals spend 2–4 hours researching a client, yet often miss recent news, internal culture shifts, or strategic leverage points. This agent automates executive-level research and drafts a comprehensive **Strategic Dossier** in under 2 minutes.

---

## ✨ Key Features

- **Dual-Perspective Intelligence:** Switch between "Provider/Seller" and "Customer/Buyer" roles to customize the strategic output.
- **Asymmetric Information Advantage:** Leverages real-time web search to find recent news (e.g., mergers, awards, funding) that occurred after the LLM's knowledge cutoff.
- **Multi-Agent Orchestration:**
    - **Context Specialist:** Analyzes company background and news.
    - **Industry Expert:** Spots market trends and competitive gaps.
    - **Meeting Strategist:** Creates time-boxed agendas and talking points.
    - **Communication Specialist:** Synthesizes everything into an actionable Executive Brief.
- **Comprehensive Output:** Generates a full preparation package including:
    - 60-180 minute time-boxed agendas.
    - Perspective-specific talking points with supporting data.
    - Anticipated Q&A (Objection handling for sellers, Vetting for buyers).
    - 30-60-90 day implementation roadmaps.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Orchestration:** [CrewAI](https://crewai.com/)
- **LLM:** [Anthropic Claude 3.5 Sonnet](https://www.anthropic.com/claude) (via CrewAI LLM)
- **Search Engine:** [Serper.dev](https://serper.dev/) (Google Search API)
- **Environment:** Python 3.12+

---

## 🏁 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd advanced_ai_agents/single_agent_apps/ai_meeting_agent
```

### 2. Set Up Virtual Environment
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install "crewai[anthropic]"
```

### 4. Required API Keys
You will need the following keys (enter them in the app sidebar):
- **Anthropic API Key:** [Get it here](https://console.anthropic.com/)
- **Serper API Key:** [Get it here](https://serper.dev/)

---

## 📖 Usage

1. **Launch the App:**
   ```bash
   streamlit run meeting_agent.py
   ```
2. **Input Your Context:**
   - Enter **Your Company Name** and a brief description.
   - Select your **Role** (Seller vs. Buyer).
3. **Input Meeting Details:**
   - Enter the **Client/Vendor Name**.
   - Define the **Objective** (e.g., "Partnership Deal").
   - List the **Attendees** and their titles.
4. **Generate Strategy:** Click "Prepare Meeting" and watch the agents collaborate in real-time.

---

## 🗺️ Roadmap

- [ ] **LinkedIn Integration:** Automatic attendee profile scraping.
- [ ] **Financial API Integration:** Pull real-time stock data and balance sheets.
- [ ] **CRM Sync:** Export meeting briefs directly to Salesforce or HubSpot.
- [ ] **Vector Memory:** Recall context from previous meetings with the same company.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

### 🎓 Tutorial
**[Follow the step-by-step walkthrough here](https://www.theunwindai.com/p/build-multi-agent-ai-meeting-preparation-assistant)** to learn how to build this from scratch.
