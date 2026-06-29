# nn.py
# Smartwatch Sentiment Analyzer - ABC X1 Smartwatch
# Using Streamlit + TextBlob

import streamlit as st
from textblob import TextBlob
from datetime import datetime

# ----------------------------
# Helper function: sentiment
# ----------------------------
def analyze_sentiment(review_text: str):
    """
    Analyze sentiment using TextBlob.
    Returns: polarity (float), subjectivity (float), label (str)
    """
    blob = TextBlob(review_text)
    polarity = blob.sentiment.polarity      # range: [-1.0, 1.0]
    subjectivity = blob.sentiment.subjectivity  # range: [0.0, 1.0]

    # Simple rules for label
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"

    return polarity, subjectivity, label


# ----------------------------
# Streamlit App
# ----------------------------
def main():
    # Page config
    st.set_page_config(
        page_title="Smartwatch Sentiment Analyzer",
        page_icon="⌚",
        layout="centered"
    )

    # Title & intro
    st.title("⌚ Smartwatch Sentiment Analyzer")
    st.subheader("Uncovering Customer Sentiments for ABC X1 Smartwatch")

    st.write(
        """
        This tool helps *ABC Company* quickly understand how customers feel  
        about the *ABC X1 Smartwatch* based on their written reviews.  

        ➤ Type or paste a customer review in the box below  
        ➤ Click *Analyze Sentiment*  
        ➤ Get instant feedback: *Positive, Negative, or Neutral*
        """
    )

    st.markdown("---")

    # Initialize history in session_state
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # Text input area
    review_text = st.text_area(
        "Enter a smartwatch review here:",
        placeholder="Example: This is a very nice watch with great battery life and display.",
        height=150
    )

    # Analyze button
    if st.button("Analyze Sentiment"):
        if not review_text.strip():
            st.warning("⚠ Please enter a review before analyzing.")
        else:
            polarity, subjectivity, label = analyze_sentiment(review_text)

            # Display result nicely
            st.markdown("### 🧠 Sentiment Result")

            if label == "Positive":
                st.success(f"✅ Sentiment: *{label}*")
            elif label == "Negative":
                st.error(f"❌ Sentiment: *{label}*")
            else:
                st.info(f"ℹ Sentiment: *{label}*")

            st.write(f"*Polarity Score:* {polarity:.3f}  (range: -1.0 to 1.0)")
            st.write(f"*Subjectivity Score:* {subjectivity:.3f}  (0 = very objective, 1 = very subjective)")

            # Save to history
            st.session_state["history"].append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "review": review_text,
                "label": label,
                "polarity": round(polarity, 3),
                "subjectivity": round(subjectivity, 3),
            })

    st.markdown("---")

    # Show Review History (for PPT: "Review History Storage")
    with st.expander("📜 View Analyzed Review History"):
        if len(st.session_state["history"]) == 0:
            st.write("No reviews analyzed yet.")
        else:
            for item in reversed(st.session_state["history"]):
                st.write(f"*Time:* {item['time']}")
                st.write(f"*Review:* {item['review']}")
                st.write(f"*Sentiment:* {item['label']}")
                st.write(
                    f"*Polarity:* {item['polarity']} | *Subjectivity:* {item['subjectivity']}"
                )
                st.markdown("---")


if _name_ == "_main_":
    main()