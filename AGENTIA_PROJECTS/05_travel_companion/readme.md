# Agentia Travel Companion Project

This is a **fifth project** in your **Agentia** learning path. This one brings together several capabilities from prior projects—multi-turn conversations, user preferences, knowledge graphs, and LLM-based tool-calling—to build a **Travel Companion Agent**. The goal is to **plan and book travel** (flights, hotels, car rentals, etc.) while maintaining **human oversight** throughout the process.

---

## Project Overview

1. **Goal**  
   - Develop a **Travel Companion Agent** that can help users find and compare travel options, leveraging a flight/hotel/car-rental API, existing user preferences, and a knowledge graph for contextual information (locations, personal connections, loyalty programs).  
   - Use LLM-based **tool-calling** to parse complex user requests, propose itinerary options, and summarize them—while letting the user confirm (or modify) final bookings.

2. **Key Components**  
   1. **Front-End Orchestration Agent** (existing)  
      - Central router for all user requests.  
   2. **Greeting Agent** (existing)  
      - Handles simple greeting or small talk.  
   3. **User Preference Agent** (existing)  
      - Stores user-specific data (e.g., seat preferences, hotel tier preferences, loyalty program numbers).  
   4. **Knowledge Graph Agent** (optional but beneficial)  
      - Maintains structured relationships about locations (cities, airports, hotels) and user connections (frequent travel partners, recommended destinations).  
   5. **Mail Processing Agent** (optional)  
      - Could be used to handle email confirmations or forward booking details to the user’s email.  
   6. **Travel Companion Agent** **(New)**  
      - Integrates external travel APIs (flight, hotel, car rental) via function-calling.  
      - Uses an LLM to understand user queries and to generate itinerary recommendations.  
      - Maintains a **human-in-the-loop** flow for finalizing bookings.

3. **Value Proposition**  
   - Demonstrates a more **complex orchestration** of specialized agents and external APIs.  
   - Highlights how multi-agent collaboration, LLM-based reasoning, and user-centered design can simplify a typically multi-step, detail-heavy process (travel planning).

---

## 1. Plan the Architecture

1. **Service Layout**  
   - You will add the **Travel Companion Agent** as a new service.  
   - It will interface with one or more external travel APIs (e.g., Skyscanner, Amadeus, Expedia, or any public flight/hotel aggregator).  
   - Continue to run the existing agents independently.

2. **Communication Patterns**   
   - For the LLM, set up **function-calling** definitions such as:  
     - **SearchFlights**(origin, destination, date, seat_class)  
     - **SearchHotels**(city, check_in_date, check_out_date, star_rating)  
     - **BookItinerary**(flight_id, hotel_id, user_id)  
   - The LLM can parse user utterances (e.g., “Find me a flight from New York to London next Tuesday with a window seat.”) and invoke these functions with structured parameters.

3. **Human-in-the-Loop Approval**  
   - Before actually booking a flight or hotel, the Travel Companion Agent returns a **draft** itinerary to the Front-End Agent.  
   - The user can approve or modify the itinerary (change airline, hotel rating, or price range).  
   - Once approved, the Travel Companion Agent calls `BookItinerary` to finalize the booking.

---

## 2. Travel Companion Agent

### 2.1 Responsibilities

1. **Interpret User Travel Requests**  
   - e.g., “I want to travel to Tokyo on November 5th and return on November 12th.”  
   - The agent uses the LLM to parse the date range, the destination, seat preferences, and user loyalty memberships.

2. **Search and Summarize Options**  
   - Calls **SearchFlights** with the parsed details to get flight options from an external API.  
   - Potentially calls **SearchHotels** or **SearchCarRentals**.  
   - Summarizes the top 3–5 results (price, duration, layovers, amenities) in natural language.

3. **Draft Itinerary**  
   - Proposes an itinerary (chosen flight + hotel + any extras) as a **draft**.  
   - Flags certain constraints or benefits (e.g., “Hotel matches your preference for a fitness center,” or “You have enough points for an upgrade.”).

4. **Book Itinerary**  
   - After user approval, calls **BookItinerary** (or direct external API) to finalize reservations.  
   - Could optionally trigger an email confirmation via the **Mail Processing Agent**.

5. **Incorporate Payment Handling**  
- Add a [Stripe Agentic Payments](https://docs.stripe.com/agents) so users can finalize bookings within the same conversation.


---

## 3. Front-End Orchestration Agent: Extended Logic

1. **Routing Travel Requests**  
   - If the user’s input indicates travel planning, the request is forwarded to the Travel Companion Agent.  
   - The existing logic remains for greeting or email requests, etc.

2. **Draft Itinerary Approval**  
   - Upon receiving a draft, the Front-End Agent displays the results to the user.  
   - If the user says “Yes, book it,” the Front-End Agent calls the Travel Companion Agent’s **booking** endpoint.  
   - If the user wants changes, the agent prompts the Travel Companion Agent with updated parameters (“Look for an earlier departure” or “I want a cheaper hotel”).

3. **Fallback**  
   - If the Travel Companion Agent is unavailable or the user’s request is unclear, the Front-End Agent can ask clarifying questions or provide an error message.

---

## 4. Demonstration Scenario

1. **User**: “Hello!”  
   - **Front-End** → **Greeting Agent** → “Hi there! How can I help you today?”  
2. **User**: “I’d like to go to Tokyo in mid-November for a week, and stay in a 3-star hotel.”  
   - **Front-End** → **Travel Companion Agent**.  
   - The Travel Companion Agent:  
     - Calls `SearchFlights(origin=UserLocation, destination=Tokyo, date=Mid-November)` and `SearchHotels(city=Tokyo, star_rating=3, date_range=NovXX–NovXX)`.  
     - Summarizes top results (prices, durations, amenities).  
     - Returns them as a **draft**.  
3. **User**: “That flight price is too high. Any cheaper options?”  
   - **Front-End** → The Travel Companion Agent again, with updated constraints.  
   - The agent searches and replies with cheaper flights (maybe with more layovers or different airlines).  
4. **User**: “Okay, let’s go with that cheaper flight, but keep the original 3-star hotel.”  
   - **Front-End** → The Travel Companion Agent.  
   - The agent sends back a final draft itinerary (flight + hotel).  
5. **User**: “Yes, book it.”  
   - **Front-End** → The Travel Companion Agent.  
   - The agent calls `BookItinerary` or the external API.  
   - Optionally triggers an email confirmation via the **Mail Processing Agent** so the user receives details in their inbox.

---

## 5. Deployment and Testing

1. **Local or Cloud Setup**  
   - Continue containerizing each agent.  
   - For the Travel Companion Agent, either **mock** the external travel API or use a **sandbox** environment if the API provides one.  
   - Ensure your LLM can call the required “tools” for searching and booking travel.

2. **Logs and Observability**  
   - **Travel Companion Agent**: Log each function call, flight/hotel search, and booking attempt.  
   - **Front-End Agent**: Log the user’s acceptance or modifications to the itinerary.

3. **Error Handling**  
   - If the external API fails or returns no results, the agent should produce a clear fallback (e.g., “No flights found for those dates. Please try different dates or a different airport.”).

---

## 6. Optional Enhancements


1. **Advanced NLP and Recommendations**  
   - Use the **Knowledge Graph Agent** to store historical travel data or user’s frequent destinations, then recommend loyalty program options or travel deals.  
   - Filter results by the user’s budget or loyalty tier automatically.



2. **Combine with Email Processing**  
   - Let the user forward confirmation emails to the Mail Processing Agent, which automatically updates the Travel Companion Agent’s knowledge graph (linking reservation details, flight numbers).

3. **Multi-User Collaboration**  
   - If multiple people want to travel together, the Travel Companion Agent could coordinate calendars, seating preferences, or group discounts.

4. **Voice Interface**  
   - Integrate a speech-to-text layer for fully voice-based travel planning: “Book me a flight to San Francisco next weekend.”

5. **Smart Upsells**  
   - Suggest additional services like airport transfers or local tours if relevant to the user’s profile.

---

## Conclusion

This **fifth project** extends your **Agentia** environment into the realm of **real-world travel planning**. You will:

- **Combine** multi-agent orchestration with LLM-based function-calling, external APIs, and user feedback loops.  
- **Demonstrate** how an AI system can handle complex tasks like flight/hotel searching, itinerary drafting, and final booking—while still keeping humans in control.  
- **Unify** your prior agents (Greeting, User Preference, Knowledge Graph, possibly Mail Processing) in a single cohesive workflow.

By completing this Travel Companion project, you’ll showcase a high-value, practical use case for multi-agent systems powered by natural language interfaces, robust data orchestration, and LLM-based reasoning.