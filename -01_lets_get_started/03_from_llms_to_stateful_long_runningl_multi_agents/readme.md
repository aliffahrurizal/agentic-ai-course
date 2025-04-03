# From LLMs to Stateful Long Running Multi-Agent Systems

This document has been split into three separate set of articles, each tackling a unique question:

1. What are AI agents, and what features and functionalities can we anticipate they’ll have? What should be the Guiding Principles for Crafting Agentic AI?
2. What Architecture to use to for Multi-Agent Systems (AgentiaCloud)?
3. What technological components and infrastructure are needed to build and implement these Multi-Agent Systems (AgentiaCloud)? We will discuss in detail our AgentiaCloud technology stack.

Note: These questions are answered in topics 01, 02, and 03 in this directory.

## The Agents Have Documented

Agentic AI Development and Use Cases

Agentic AI Development and Applications

In 2025, Agentic AI emerges as a global focal point. Leading tech giants such as OpenAI, Microsoft, Google, AWS, Oracle, DeepSeek, Anthropic, Alibaba, Baidu, Huawei, ByteDance, and others are driving this trend.

Insha Allah, we aim to revolutionize Pakistan and the world through Agentic AI, with an emphasis on creating specialized Vertical Agentic solutions.

We have developed detailed documentation outlining Multi-Agent Systems, including their architecture, which will enable us to build AI Agents on a global scale. Most notably, it highlights the key vertical sectors that our thousands of students will initially target:

Here’s a comprehensive list of all the agents we’ve explored, spanning various domains and showcasing the application of **event-driven architecture (EDA)**, **three-tier architecture**, **stateless computing**, **scheduled computing (CronJobs)**, **human-in-the-loop (HITL)**, and, in some cases, **LLM intelligence**. Each agent addresses a unique use case within its domain:

1. **Email Agent** (Email Management Domain)
   - **Purpose**: Monitors incoming emails, filters them, suggests responses, and sends replies after user approval; also checks and corrects new emails composed by the user.
   - **Domain**: Personal Productivity/Communication.

2. **Supply Chain Optimization Agent** (Logistics Domain)
   - **Purpose**: Monitors inventory levels, optimizes delivery routes, and suggests actions; allows manual route adjustments with optimization.
   - **Domain**: Supply Chain/Logistics.

3. **Healthcare Patient Monitoring Agent** (Healthcare Domain)
   - **Purpose**: Monitors patient vitals, detects anomalies, suggests interventions, and notifies healthcare professionals; supports manual follow-up requests.
   - **Domain**: Healthcare/Telemedicine.

4. **Financial Trading Agent** (Finance Domain)
   - **Purpose**: Monitors market data, suggests trades based on strategies, notifies traders for approval; optimizes manual trade requests.
   - **Domain**: Financial Services/Trading.

5. **Personalized Learning Agent** (Education Domain)
   - **Purpose**: Monitors student progress, suggests personalized learning activities, notifies teachers/students; optimizes manual assignment requests.
   - **Domain**: Education/Teaching.

6. **Blood Bank ERP Agent** (Blood Bank Management Domain)
   - **Purpose**: Tracks blood units with barcodes, manages donor relationships, notifies donors of eligibility; supports manual staff requests. Adds inventory optimization, demand forecasting, donor scheduling, quality control, and reporting; includes LLM intelligence for donor engagement and insights.
   - **Domain**: Healthcare/Blood Bank Management..
   

7. **Shopping Cart and Inventory Management Agent** (E-commerce Domain)
   - **Purpose**: Manages shopping carts, tracks inventory, suggests restocking or pricing actions; supports manual inventory requests with dynamic pricing, fulfillment optimization, and recommendations.
   - **Domain**: E-commerce/Retail.

8. **Social Media Account Management Agent** (Social Media Domain)
   - **Purpose**: Monitors account activity, suggests posts/responses, notifies users; supports manual content schedules with engagement optimization and analytics.
   - **Domain**: Digital Marketing/Social Media.

9. **Customer Acquisition and Management Agent (LinkedIn)** (Sales Domain)
    - **Purpose**: Identifies prospects on LinkedIn, suggests outreach messages, notifies sales reps; manages relationships and supports manual sales requests with lead scoring and content sharing.
    - **Domain**: Customer Relationship Management (CRM)/Sales.

---

### Summary of Domains Covered
- **Communication**: Email Agent
- **Logistics**: Supply Chain Optimization Agent
- **Healthcare**: Healthcare Patient Monitoring Agent, Blood Bank ERP Agent
- **Finance**: Financial Trading Agent
- **Smart Home**: Smart Home Energy Management Agent
- **Education**: Personalized Learning Agent
- **E-commerce**: Shopping Cart and Inventory Management Agent
- **Social Media**: Social Media Account Management Agent
- **Sales/CRM**: Customer Acquisition and Management Agent (LinkedIn)

---

### Key Observations
- **Variety**: We’ve covered 10 distinct agents across 9 domains, with the Blood Bank ERP Agent having two versions to explore basic and enhanced features.
- **Automation**: Each agent leverages automation (e.g., scheduling, optimization, analytics) tailored to its domain.
- **LLM Integration**: Starting with the enhanced Blood Bank ERP Agent, we introduced LLM intelligence for content generation, insights, and user interaction, which became a recurring theme in later examples (e.g., Shopping Cart, Social Media, LinkedIn Sales).
- **HITL**: All agents incorporate human oversight for critical decisions, ensuring trust and control.



