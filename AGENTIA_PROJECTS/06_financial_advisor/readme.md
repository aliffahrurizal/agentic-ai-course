# Agentia Personal Financial Advisor Project

This is a **alternative sixth project** in your **Agentia** learning path. This one focuses on **personal finance and investment management**. You will build a **Personal Financial Advisor Agent** that uses multi-agent collaboration, LLM-based tool-calling, and human-in-the-loop approvals to help users manage budgets, track expenses, and explore investment opportunities.

---

## Project Overview

1. **Goal**  
   - Create a **Personal Financial Advisor Agent** that can analyze the user’s finances, recommend budgets, and propose potential investments based on user preferences and real-time market data.  
   - Leverage **LLM function-calling** to parse user requests (e.g., “Am I on track with my monthly budget?” or “Suggest some tech stocks under \$50”), and integrate with external **financial APIs** for up-to-date prices, exchange rates, and economic news.  
   - Maintain a **human-in-the-loop** approach for critical decisions (e.g., transferring funds, executing trades).

2. **Key Components**  
   1. **Front-End Orchestration Agent** (existing)  
      - Continues as the single entry point for user interactions.  
   2. **Greeting Agent** (existing)  
      - Handles simple greeting or small talk.  
   3. **User Preference Agent** (existing)  
      - Stores user-specific data such as risk tolerance, preferred sectors, or monthly savings goals.  
   4. **Knowledge Graph Agent** (optional)  
      - Could store relationships among stocks, sectors, user financial goals, and personal spending patterns.  
   5. **Mail Processing Agent** (optional)  
      - May handle email notifications for bill reminders, monthly summaries, or urgent market updates.  
   6. **Financial Advisor Agent** **(New)**  
      - Integrates with external **finance APIs** (e.g., Yahoo Finance, Alpha Vantage, or brokerage APIs).  
      - Leverages an **LLM** to parse and interpret user queries, calling “tools” for tasks like budgeting, expense tracking, or retrieving stock quotes.  
      - Provides a **human-in-the-loop** confirmation flow before performing sensitive actions (like transferring money or placing trades).

3. **Value Proposition**  
   - Demonstrates a **multi-agent approach** to real-world financial tasks, with robust data orchestration and user oversight.  
   - Highlights advanced **LLM** usage, bridging personal data (budgets, preferences) with dynamic external data (markets, interest rates).

---

## 1. Plan the Architecture

1. **Service Layout**  
   - **Financial Advisor Agent** will act as its own service or container, just like the other agents.  
   - It connects to third-party **financial APIs** for real-time or near-real-time data on stocks, exchange rates, or economic indicators.

2. **Communication Patterns**    
   - The LLM within the Financial Advisor Agent will have “function-calling” definitions such as:  
     - **GetStockQuote**(ticker)  
     - **AnalyzeBudget**(userId)  
     - **RecommendPortfolio**(riskTolerance, investmentHorizon)  
     - **ExecuteTrade**(ticker, shares, orderType) — flagged for human approval.

3. **Security and Compliance**  
   - For demo purposes, you might simulate trading or integrate with a **paper trading** service to avoid real financial risk.  
   - If moving toward production, ensure compliance with relevant regulations (e.g., KYC/AML in finance).

---

## 2. Financial Advisor Agent

### 2.1 Responsibilities

1. **Parse Financial Queries**  
   - e.g., “How much did I spend last month?” or “Compare my expenses this month to last month.”  
   - e.g., “I have \$500 to invest; can you suggest some low-volatility ETFs?”  
   - The LLM interprets these requests and decides which tool to invoke—budget analysis, expense tracking, or investment suggestions.

2. **Retrieve and Summarize Market Data**  
   - Calls **GetStockQuote** for ticker symbols (like AAPL, TSLA) or broad market data (SPY, QQQ, etc.).  
   - Summarizes the data in natural language: “TSLA is trading at \$200, up 2% today.”

3. **Budget and Expense Tracking**  
   - Might integrate with the user’s bank API or a mock data source to categorize spending.  
   - Provide monthly/weekly analytics: “You’ve spent \$300 on groceries, \$100 on dining out, \$50 on entertainment.”

4. **Portfolio Recommendations**  
   - Based on **User Preference Agent** data (risk tolerance, time horizon, favorite sectors) and real-time market info.  
   - Returns a drafted recommendation like: “80% in broad market ETF, 10% in tech, 10% in bonds—given your moderate risk profile.”

5. **Transaction Approval**  
   - If the user wants to **ExecuteTrade** (“Buy 10 shares of TSLA”), return a **draft** response requiring human confirmation before finalizing.  
   - Once confirmed, calls the trade execution function (against a paper-trading API or sandbox for safety).


---

## 3. Front-End Orchestration Agent: Extended Logic

1. **Identify Financial Requests**  
   - If the user’s input mentions budgets, stocks, or expenses, route to the **Financial Advisor Agent**.  
   - Otherwise, forward to the relevant agent (Greeting, Mail Processing, etc.).

2. **Draft Approval**  
   - If the response from the Financial Advisor Agent is marked `draft: true` (e.g., to execute a trade), the Front-End Agent asks for confirmation or modification.  
   - Upon user approval, the front-end calls a finalization endpoint (e.g., `POST /financial_advisor/finalize`) to actually execute the trade or update the user’s budget data.

3. **Fallback**  
   - If the user’s request is unclear or out of scope (e.g., advanced derivatives strategies not supported by the system), prompt for clarification or show an error.

---

## 4. Demonstration Scenario

1. **User**: “Hello!”  
   - **Front-End** → **Greeting Agent** → Returns a simple welcome.  
2. **User**: “Show me how much I spent this month on dining out.”  
   - **Front-End** → **Financial Advisor Agent**  
   - The Financial Advisor Agent calls the appropriate tool (e.g., `AnalyzeExpenses`) for “dining out.”  
   - Returns: “You’ve spent \$120 on dining out so far this month.”  
3. **User**: “What’s the current price of TSLA, and should I buy a few shares?”  
   - **Front-End** → **Financial Advisor Agent**  
   - The agent calls `GetStockQuote(ticker='TSLA')` for real-time price, and possibly `RecommendPortfolio` to see if TSLA fits the user’s risk profile.  
   - Returns a draft: “TSLA is at \$200. Buying 2 shares might be suitable given your moderate risk. Approve trade?”  
4. **User**: “Yes, do it.”  
   - **Front-End** → finalizes the trade with the Financial Advisor Agent.  
   - The agent executes a paper-trade or simulated trade, then confirms success: “Trade completed. You now have 2 shares of TSLA.”

---

## 5. Deployment and Testing

1. **Local or Cloud Setup**  
   - For real or simulated financial data, use **sandbox** APIs (e.g., IEX Cloud sandbox, Alpha Vantage free tier, or a mock data generator).

2. **LLM Function-Calling**  
   - Define “tools” for major tasks: analyzing expenses, retrieving quotes, recommending portfolios, executing trades.  
   - Verify the LLM can parse a user’s financial request and call the correct tools with structured parameters.

3. **Security and Authorization**  
   - If integrating with real bank accounts or brokerages, add secure OAuth flows or API keys.  
   - For a proof-of-concept, a mock or paper account is safer to avoid real financial transactions.

4. **Logging and Auditing**  
   - **Financial Advisor Agent**: Log every recommendation, trade, or budget update.  
   - **Front-End**: Log user confirmations or modifications.

5. **Error Handling**  
   - If the finance API is unreachable, return an informative error message.  
   - If a user tries to invest more than they have, clarify next steps.

---

## 6. Possible Enhancements

1. **Advanced Budget Analysis**  
   - Integrate machine learning to categorize transactions automatically, forecast monthly budgets, or detect unusual spending (fraud alerts).

2. **Portfolio Optimization**  
   - Implement algorithms (e.g., Markowitz portfolio optimization) to recommend an ideal asset mix.  
   - Factor in real-time market volatility or sentiment analysis.

3. **Goal-Oriented Savings**  
   - Let the user define goals (e.g., saving \$5,000 for a vacation) and receive ongoing status updates and advice.

4. **Notifications and Email Summaries**  
   - Via the **Mail Processing Agent**, send weekly or monthly financial summaries.  
   - Alert the user if spending surpasses a limit or if a favored stock dips below a target price.

5. **Integration with Knowledge Graph**  
   - Store relationships between user expenses, merchants, categories, or stocks.  
   - For instance, linking “this merchant is in the user’s travel category” or “this stock is in the tech sector.”  
   - Empower advanced queries: “Which categories are draining my budget the fastest this quarter?”

6. **Voice Interface**  
   - Optionally add voice-based commands: “Hey agent, how’s my portfolio doing today?”

---

## Conclusion

This **alternative sixth project** centers on building a **Personal Financial Advisor Agent**, leveraging:

- **Multi-agent** orchestration, with existing agents for greeting, preferences, (optional) knowledge graph, etc.  
- **LLM-based tool-calling** for tasks like budget analysis, stock quote retrieval, and portfolio recommendations.  
- **Human-in-the-loop** workflows for finalizing trades or major financial decisions.

By tackling personal finance and investment management, you demonstrate how **Agentia** can extend into a **high-stakes domain** requiring both **advanced data integrations** (financial APIs) and **robust user confirmations**, showcasing the versatility and practicality of your multi-agent architecture.