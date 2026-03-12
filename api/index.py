from flask import Flask, request
import google.generativeai as genai
import os

app = Flask(__name__)

# הגדרת Gemini - המפתח יימשך מתוך הגדרות השרת (Environment Variables)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-flash-latest")

@app.route('/api', methods=['GET', 'POST'])
def chat():
    # קבלת הטקסט מימות המשיח (פרמטר text)
    user_input = request.values.get('text', '')
    
    if not user_input:
        return "id_list_message=t-לא התקבל קלט"

    try:
        # שליחת השאלה לבינה המלאכותית
        response = model.generate_content(user_input)
        bot_text = response.text
        
        # ניקוי תווים שעלולים לשבש את הפקודה הטלפונית
        clean_text = bot_text.replace('=', ' ').replace('&', ' ו-').replace('*', '')
        
        return f"id_list_message=t-{clean_text}"
    except Exception as e:
        return "id_list_message=t-אירעה שגיאה זמנית בעיבוד"

# נדרש עבור Vercel
def handler(event, context):
    return app(event, context)
