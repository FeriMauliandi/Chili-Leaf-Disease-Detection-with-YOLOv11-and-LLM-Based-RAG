import json
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def retrieve_disease_info(disease_name):
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(disease_name)

def build_prompt(disease_name, info):
    return f"""
Anda adalah penyuluh pertanian cabai.

Gunakan HANYA informasi berikut.
Jangan menambahkan fakta baru.

TUGAS ANDA:
1. jelaskan nama penyakit
2. jelaskan penyebab
2. Jelaskan gejala utama
3. Jelaskan penanganan 
4. Jelaskan pencegahan
 
Nama penyakit: {disease_name}

Penyebab:
- {'; '.join(info['penyebab'])}

Gejala:
- {'; '.join(info['gejala'])}

Penanganan:
- {'; '.join(info['penanganan'])}

Pencegahan:
- {'; '.join(info['pencegahan'])}

Gunakan bahasa sederhana untuk para petani cabai.
dan jika nama penyakitnya: sehat maka jelaskan saja jika daunnya sehat
"""

def generate_narrative(prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[
                {"role": "system", "content": "Anda adalah asisten pertanian cabai."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.6
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ LLM ERROR: {str(e)}"


# xiaomi/mimo-v2-flash:free
# deepseek/deepseek-r1-0528:free