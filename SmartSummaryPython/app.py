import os
import streamlit as st
from openai import OpenAI

# Sayfa başlığı ve ikon
st.set_page_config(page_title="SmartSummary (Python)", page_icon="🧠")
st.title("🧠 Akıllı Metin Özeti Uygulaması")

# API anahtarı kontrolü
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ OpenAI API anahtarı bulunamadı. Birazdan nasıl ekleneceğini göstereceğim.")
    st.stop()

# OpenAI istemcisi
client = OpenAI(api_key=api_key)

# Kullanıcı arayüzü
with st.form("summary_form"):
    text = st.text_area("Metni buraya yapıştır:", height=200, placeholder="Uzun metni buraya girin...")
    col1, col2 = st.columns(2)
    with col1:
        sentence_count = st.number_input("Cümle sayısı", min_value=1, max_value=10, value=3)
    with col2:
        language = st.text_input("Çıktı dili (örnek: Turkish, English)", value="")
    submitted = st.form_submit_button("Özetle")

# Özetleme işlemi
if submitted:
    if not text.strip():
        st.warning("⚠️ Lütfen özetlenecek metni girin.")
    else:
        with st.spinner("🧠 Özet hazırlanıyor..."):
            prompt = f"Summarize the following text in {sentence_count} sentences."
            if language.strip():
                prompt += f" Answer in {language.strip()}."
            prompt += "\n\n" + text

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a concise summarizer. Keep the core meaning, avoid fluff."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )
                summary = response.choices[0].message.content
                st.success("✅ Özet:")
                st.write(summary)
            except Exception as e:
                st.error(f"🚫 Hata: {e}")

