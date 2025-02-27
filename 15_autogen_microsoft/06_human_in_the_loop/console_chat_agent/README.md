# AutoGen Human Agent Chat Loop

1. Add openai_key in .env

2. Run  
```bash
uv run hil
```

3. Sample Logs
```bash
Hello! How can I assist you today? Feel free to ask me any questions you have.
Enter your response: Hi 
---------- user_proxy ----------
Hi
---------- assistant ----------
Hello! How can I help you today? If you have any questions, feel free to ask!
Enter your response: TERMINATE
---------- user_proxy ----------
TERMINATE
APPR---------- assistant ----------
TERMINATE
Enter your response: APPROVE
---------- user_proxy ----------
APPRAPPROVE
```