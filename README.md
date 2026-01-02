# Geo-Expert Document Indexing Module

מודול פייתון שפותח כחלק ממטלת בית עבור Geo Mobility. הסקריפט מבצע תהליך מלא של עיבוד מסמכי רכב (PDF/DOCX), לבינתיים נטען קובץ תעודת אחריות, חלוקתם למקטעים, יצירת Embeddings בעזרת Gemini API ושמירתם במסד נתונים PostgreSQL.

## דרישות מערכת

- Python 3.9+
- מסד נתונים PostgreSQL (מומלץ Neon.tech)
- Gemini API Key

## התקנה

1. שכפל את המאגר (Clone):
   ```bash
   git clone [https://github.com/ArielGuralnick/Geo-Expert-Indexing]
   ```
2. התקן את הספריות הנדרשות :
   pip install google-generativeai psycopg2-binary python-dotenv pypdf python-docx cryptography

3. הגדר משתני סביבה: צור קובץ .env בתיקייה הראשית והזן את הפרטים הבאים:
   GEMINI_API_KEY: המפתח שקיבלת מ-Google AI Studio.
   POSTGRES_URL: כתובת החיבור למסד הנתונים שלך.

## שימוש

להרצת תהליך האינדוקס, וודא שיש קובץ בשם Warranty_Certificate.pdf בתיקייה והרד:
python index_documents.py

## אסטרטגיית Chunking

בפרויקט זה נעשה שימוש בשיטת Fixed-size with overlap (גודל קבוע עם חפיפה) כדי להבטיח רציפות בהקשר הסמנטי בין המקטעים השונים
