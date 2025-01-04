# Agentia Mail Processing Project

This is the **fourth project** in your **Agentia** learning path, which focuses on integrating **LLM tool-calling** (sometimes called “function calling”) to autonomously process emails while keeping a **human-in-the-loop** approval step. This project builds on your previous multi-agent architecture and introduces a more advanced conversational flow, leveraging Large Language Models (LLMs) for understanding and automating email handling.

---

## Project Overview

1. **Goal**  
   - Incorporate a **Mail Processing Agent** that uses an LLM with **tool-calling** (function calling) capabilities to parse and respond to emails.  
   - Maintain a **human-in-the-loop** (HITL) approach: the system drafts responses or takes actions automatically, but requires user approval before finalizing critical steps (e.g., sending an email, creating a calendar event).

2. **Key Components**  
   1. **Front-End Orchestration Agent**  
      - Single entry point for user instructions.  
      - Delegates requests to the Mail Processing Agent (or other specialized agents) and consolidates outputs for the user.
   2. **Greeting Agent** *(Existing from earlier projects)*  
      - Handles greetings and simple chit-chat.
   3. **User Preference Agent** *(Existing from earlier projects)*  
      - Stores/retrieves user-specific information such as names, preferences, etc.
   4. **Knowledge Graph Agent** *(Optional from earlier projects)*  
      - If desired, store complex relationships (e.g., contact relationships, meeting locations).
   5. **Mail Processing Agent** **(New)**  
      - Integrates with an email service (Gmail, IMAP, Exchange, etc.).  
      - Uses an **LLM** with **tool-calling** to:  
        - Parse incoming emails, extract relevant info, and detect tasks or requests.  
        - Draft suggested replies or actions.  
        - Wait for user approval before finalizing actions.

3. **Value Proposition**  
   - Showcases how a **conversational LLM** can orchestrate real-world tasks (email reading, response drafting) by calling specialized tools (e.g., scheduling, knowledge lookup).  
   - Preserves **human oversight** to ensure correctness and user satisfaction.

---

## 1. Plan the Architecture

1. **Service Layout**  
   - You will have at least two new services or components for email processing:  
     1. **Mail Processing Agent** (with an LLM at its core).  
     2. **Email Integration Layer** (optional if you want direct SMTP/IMAP integration).
   - Continue running the existing agents (Front-End, Greeting, User Preference, Knowledge Graph if needed) as separate processes or containers.

2. **Tool-Calling / Function-Calling Setup**  
   - Modern LLM providers (e.g., OpenAI, Anthropic, or local LLM frameworks) often allow you to define “functions” or “tools” that the model can invoke when certain intentions are detected. Examples of tools:
     - **SendEmail**: Takes a recipient, subject, and body, then sends the email.
     - **CheckCalendar**: Retrieves user availability.  
     - **StoreInKnowledgeGraph**: Links data about the sender, subject, or attachments to your knowledge graph.  
   - The LLM will parse user requests and either respond with text or invoke these tools with structured JSON.

3. **Human-in-the-Loop Mechanism**  
   - Introduce a “draft mode” for critical actions:  
     - The LLM prepares a draft email or outlines an action (e.g., scheduling a meeting).  
     - The draft is sent back to the **Front-End Agent**, which displays it to the user for approval.  
     - The user can **approve** or **reject** (and optionally modify) the draft.  
     - Upon approval, the **Front-End Agent** instructs the Mail Processing Agent to finalize the action (e.g., actually send the email or confirm the meeting).

---

## 2. Mail Processing Agent

### 2.1 Responsibilities

1. **Parse Incoming Emails**  
   - Automatically read or receive email content (subject, body, sender).  
   - Use the LLM’s NLU capabilities to identify tasks (meeting requests, action items, summaries) or relevant metadata (dates, times, locations).
2. **Draft Responses**  
   - The user can request: “Please reply that I am available on Monday.”  
   - The LLM calls the **CheckCalendar** tool to confirm availability.  
   - The LLM then constructs a draft reply email, returning it to the Front-End Orchestration Agent for approval.
3. **Finalize Actions**  
   - Once the user approves the draft, the agent calls the **SendEmail** tool (or a real SMTP/IMAP API) to dispatch the email.  
   - For other tasks (e.g., storing data in the Knowledge Graph), the LLM calls the relevant agent or function.



---

## 3. Demonstration Scenario

1. **User**: “Hello!”  
   - **Front-End** → **Greeting Agent** → “Hi there! How can I help you?”  
2. **User**: “Check my emails.”  
   - **Front-End** → **Mail Processing Agent**  
   - The Mail Processing Agent:  
     - Uses a tool (e.g., `FetchEmailList`) to retrieve unread messages.  
     - Summarizes the user’s unread emails via LLM processing.  
     - Returns something like: “You have an email from Jane about scheduling a meeting.”  
3. **User**: “Please respond to Jane that Monday works for me.”  
   - **Front-End** → **Mail Processing Agent**  
   - The LLM calls `CheckCalendar` to confirm Monday availability, then drafts: “Hi Jane, Monday works great for me. Thanks, John.”  
   - This response is sent back with `draft: true`.  
4. **Front-End** asks the user: “Draft: ‘Hi Jane, Monday works great…’ Approve or modify?”  
   - **User**: “Looks good, approve.”  
5. **Front-End** → Tells **Mail Processing Agent** to finalize.  
   - The Mail Processing Agent calls `SendEmail`, resulting in the email actually being sent.  
6. **User**: “Awesome, thanks!”  
   - End of the flow.

---



4. **Logging and Observability**  
   - **Mail Processing Agent**: Log all incoming user requests, tool calls, and final actions.  
   - **Front-End Agent**: Log the user’s decisions (approve, modify) for auditing.

5. **Error Handling**  
   - If the email provider is unavailable, return an error message to the user.  
   - If the user attempts to finalize without an approved draft, handle gracefully.

---

## 6. Possible Enhancements

1. **Advanced NLP and Summarization**  
   - Let the LLM automatically summarize long email threads, highlight action items, or categorize messages by priority.  
2. **Context Sharing**  
   - Combine the **User Preference Agent** to personalize replies (e.g., use the user’s name or preferences in automated drafts).  
   - Integrate the **Knowledge Graph Agent** so the system can check relationships (e.g., “Jane is my manager”) and tailor responses.
3. **Auto-Approval Rules**  
   - For non-critical tasks or known patterns, let the user define auto-approval if confidence is high (e.g., routine meeting invites from certain people).  
   - Keep all sensitive actions behind manual approval to maintain the HITL safety net.
4. **Calendar Integration**  
   - Expand the `CheckCalendar` tool to also **create events** or **send invites** when the user approves.  
5. **Multi-Language Support**  
   - If you have international email correspondents, incorporate language detection and translation.  
6. **Security and Authentication**  
   - Integrate OAuth or another secure mechanism for connecting to external email/calendar services (Gmail API, Microsoft Graph).

---

## Conclusion

This **fourth project** brings together **LLM-driven tool-calling** and the **multi-agent** paradigm to deliver a **human-in-the-loop, email-processing** workflow. You’ll learn to:

- **Orchestrate** user requests among multiple agents (Front-End, Greeting, Preferences, optional Knowledge Graph).  
- **Leverage** an LLM’s function-calling capabilities to parse emails, extract tasks, draft replies, and only proceed upon user approval.  
- **Integrate** with real or mock email systems for end-to-end testing.  

By implementing this project, you are essentially **demonstrating the future** of how AI-powered assistants can handle day-to-day communication autonomously—yet responsibly—under a **human’s supervision**, aligning perfectly with the **Agentia** vision of collaborative, natural language-driven software agents.