import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mineral Deficiency Awareness Tool",
    layout="centered"
)

st.title("Mineral Deficiency Awareness Tool")
st.divider()

# -------------------------------
# Symptom input (Present / Absent)
# -------------------------------
st.subheader("Select symptoms you are currently experiencing:")

symptoms = {
    "Fatigue": st.selectbox("Persistent fatigue / low energy", ["Absent", "Present"]),
    "Dizziness": st.selectbox("Dizziness or lightheadedness", ["Absent", "Present"]),
    "Shortness_of_Breath": st.selectbox("Shortness of breath on mild activity", ["Absent", "Present"]),
    "Tingling": st.selectbox("Tingling or numbness (hands/feet)", ["Absent", "Present"]),
    "Muscle_Cramps": st.selectbox("Muscle cramps or spasms", ["Absent", "Present"]),
    "Hair_Loss": st.selectbox("Hair loss or thinning", ["Absent", "Present"]),
    "Brain_Fog": st.selectbox("Poor concentration / brain fog", ["Absent", "Present"]),
    "Cold_Intolerance": st.selectbox("Cold intolerance", ["Absent", "Present"]),
    "Frequent_Infections": st.selectbox("Frequent infections / slow wound healing", ["Absent", "Present"]),
    "Bone_Pain": st.selectbox("Bone or joint pain", ["Absent", "Present"]),
    "Palpitations": st.selectbox("Heart palpitations", ["Absent", "Present"]),
    "Low_Mood": st.selectbox("Low mood / irritability", ["Absent", "Present"]),
}

# Convert Present / Absent → 1 / 0
symptom_vector = pd.Series({k: 1 if v == "Present" else 0 for k, v in symptoms.items()})

# -------------------------------
# Symptom–Mineral Weight Table
# -------------------------------
weights = pd.DataFrame({
    "Iron":        [3,2,3,0,0,2,2,2,2,0,2,1],
    "Vitamin B12": [3,2,2,3,1,1,3,1,1,0,2,2],
    "Magnesium":   [2,1,1,2,3,0,2,0,0,0,3,2],
    "Zinc":        [1,0,0,0,0,2,1,0,3,0,0,1],
    "Calcium":     [0,0,0,0,2,0,0,0,0,3,1,0],
    "Iodine":      [2,1,0,0,0,1,2,3,0,0,1,2],
    "Potassium":   [1,1,0,1,3,0,1,0,0,0,3,1],
}, index=symptom_vector.index)

# -------------------------------
# Compute scores
# -------------------------------
scores = symptom_vector.dot(weights)

# -------------------------------
# Function to classify score
# -------------------------------
def classify_score(score):
    if score >= 12:
        return "High likelihood"
    elif score >= 7:
        return "Moderate likelihood"
    else:
        return None

# -------------------------------
# Output logic
# -------------------------------
any_symptom_selected = symptom_vector.sum() > 0

if not any_symptom_selected:
    st.info("Select at least one symptom to see possible mineral deficiency insights.")
else:
    if scores.max() < 5:
        st.warning(
            "Your symptoms do not strongly align with common mineral deficiencies. "
            "If symptoms persist, consider seeking medical evaluation."
        )
    else:
        results = pd.DataFrame({
            "Mineral": scores.index,
            "Score": scores.values
        })
        results["Likelihood"] = results["Score"].apply(classify_score)
        results = results.dropna(subset=["Likelihood"])
        top_results = results.sort_values("Score", ascending=False).head(3)

        if not top_results.empty:
            st.subheader("Most Relevant Mineral Deficiencies")
            for _, row in top_results.iterrows():
                st.write(f"• **{row['Mineral']}** — {row['Likelihood']}")
        else:
            st.info(
                "Your symptoms do not strongly suggest a common mineral deficiency. "
                "This tool is for awareness only and does not replace clinical evaluation."
            )

st.divider()
st.caption(
    "⚠️ Disclaimer: This tool is for educational purposes only and does not "
    "diagnose, treat, or recommend supplements. Always consult a healthcare professional."
)
