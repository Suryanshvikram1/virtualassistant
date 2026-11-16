import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from tools.web_search import search_web
from tools.task_manager import add_task, list_tasks, clear_tasks

load_dotenv()
SYSTEM_PROMPT = (
    "You are Astra, a helpful personal virtual assistant for a college student. "
    "Answer clearly and naturally. Do not claim actions you did not perform."
)

class AstraAssistant:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b").strip()
        self.chat = ChatGroq(
            groq_api_key=api_key, model_name=model,
            temperature=0.4, max_tokens=800
        ) if api_key else None
        self.history = []

    def reset_history(self):
        self.history = []

    def _ask_ai(self, text, context=None):
        if not self.chat:
            return ("Groq API key is missing. Add it to GROQ_API_KEY in .env "
                    "and restart Astra. Basic commands still work.")
        prompt = text
        if context:
            prompt = (
                "Answer using the PDF text below. If the answer is not in it, say so.\\n\\n"
                f"PDF TEXT:\\n{context[:12000]}\\n\\nQUESTION:\\n{text}"
            )
        messages = [SystemMessage(content=SYSTEM_PROMPT)]
        messages.extend(self.history[-8:])
        messages.append(HumanMessage(content=prompt))
        try:
            result = self.chat.invoke(messages)
            answer = str(result.content).strip()
            self.history.extend([HumanMessage(content=text), result])
            return answer or "I couldn't generate a response."
        except Exception as exc:
            print(f"Groq API error: {exc}")
            return "I couldn't reach Groq. Check your API key, internet, model and usage limits."

    def answer_with_context(self, text, context):
        return self._ask_ai(text, context)

    def handle(self, text):
        lower = text.lower().strip()
        if lower in ("help", "what can you do", "what can you do?"):
            return ("I can answer questions, tell the date and time, search the web, "
                    "manage tasks, and answer questions about an uploaded PDF.")
        if "time" in lower or "date" in lower:
            return datetime.now().strftime("It is %I:%M %p on %A, %d %B %Y.")
        if lower.startswith("add task "):
            task = text[9:].strip()
            return add_task(task) if task else "Please provide a task."
        if "list tasks" in lower or "show my tasks" in lower:
            return list_tasks()
        if "clear tasks" in lower or "delete all tasks" in lower:
            return clear_tasks()
        if lower.startswith("search the web for "):
            return search_web(text[len("search the web for "):].strip())
        if lower.startswith("search for "):
            return search_web(text[len("search for "):].strip())
        return self._ask_ai(text)
