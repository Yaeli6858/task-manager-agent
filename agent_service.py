import json
import os
import httpx
from groq import Groq
from dotenv import load_dotenv
from todo_service import get_tasks, add_task, update_task, delete_task

load_dotenv()

# netfree
http_client = httpx.Client(verify=False)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    http_client=http_client
)

FUNCTIONS = [
    {
        "name": "get_tasks",
        "description": "שליפת כל המשימות מהרשימה",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "add_task",
        "description": "הוספת משימה חדשה",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "כותרת המשימה"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "update_task",
        "description": "עדכון סטטוס משימה לבוצע",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "מספר המזהה של המשימה"}
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "delete_task",
        "description": "מחיקת משימה מהרשימה",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer"}
            },
            "required": ["task_id"]
        }
    }
]

def agent(query: str):
    tools = [{"type": "function", "function": f} for f in FUNCTIONS]

    messages = [
        {
            "role": "system", 
            "content": "You are a specialized Task Manager. When a user asks to add, delete, or list tasks, you MUST use the provided tools. Ensure your tool calls are valid JSON. Respond to the user in Hebrew."
        },
        {"role": "user", "content": query}
    ]

    # שלב א': שליחה ל-Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto", # אפשר להשאיר auto אבל עם הנחיית מערכת חזקה
        temperature=0.1 # הורדת הטמפרטורה הופכת את המודל ליותר מדויק ופחות 'יצירתי' בפורמט
    )
    
    message = response.choices[0].message
    
    if not message.tool_calls:
        return message.content

    # שלב ב': ביצוע הפעולה
    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    
    # ניקוי ידני קטן לטקסט למקרה שהמודל שוב שכח סוגר (ליתר ביטחון)
    raw_args = tool_call.function.arguments
    if raw_args.count('{') > raw_args.count('}'):
        raw_args += '}'

    try:
        function_args = json.loads(raw_args)
    except json.JSONDecodeError:
        return "סליחה, המערכת ייצרה פקודה לא תקינה. נסו לנסח את הבקשה שוב."

    if function_name == "get_tasks":
        data = get_tasks()
        result = str(data) if data else "רשימת המשימות ריקה."
    elif function_name == "add_task":
        res = add_task(title=function_args.get("title", "משימה חדשה"))
        result = f"המשימה נוספה: {res}"
    elif function_name == "update_task":
        res = update_task(task_id=function_args.get("task_id"))
        result = f"הסטטוס עודכן: {res}" if res else "לא מצאתי משימה כזו."
    elif function_name == "delete_task":
        delete_task(task_id=function_args.get("task_id"))
        result = "המשימה נמחקה בהצלחה."
    else:
        result = "הפעולה לא מוכרת לי."

    # שלב ג'
    final_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            *messages,
            message,
            {
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id
            }
        ]
    )
    
    return final_response.choices[0].message.content