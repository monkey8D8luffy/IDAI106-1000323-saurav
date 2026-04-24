# 🌊 FutureForward Wellness — Smart Stress Relief Pod Interface

**Course:** Design Thinking for Innovation (IDAI106)  
**Student ID:** 1000323  

FutureForward Wellness is a digital interface designed for "Smart Stress Relief Pods" in high-performance corporate environments. It uses empathetic design, dynamic biometric simulation, and ambient audio-visuals to curate a personalized, locked-in wellness environment that lowers immediate stress and restores cognitive flow.

---

## 🚨 Problem Statement

Modern corporate environments are characterized by high cognitive loads, leading to burnout, reduced focus, and musculoskeletal tension among employees. Traditional breaks often involve screen time (e.g., scrolling social media at a desk), which fails to alleviate cognitive fatigue. 

**How might we create a frictionless, immersive environment that forces users to disconnect, lowers their immediate stress levels, and restores their flow state?**

---

## 🧠 Empathy Maps

*(Note: The full 10 User Personas are located in the `Docs/` folder of this repository. Below is a synthesized Empathy Map representing our primary user: The Overworked Corporate Employee).*

### The "Stressed Employee" Persona
* **Says:** "I don't have time to take a break." / "My brain feels like it's lagging." / "I just need 5 minutes of quiet."
* **Thinks:** "If I step away from my desk, I'll fall behind." / "I am exhausted but my mind is racing." / "Why is my neck so stiff?"
* **Does:** Drinks excessive caffeine to compensate for fatigue. Mindlessly scrolls social media during "breaks" instead of resting. Rubs their temples and neck frequently.
* **Feels:** Overwhelmed, constantly accessible, physically tense, and cognitively drained. 

---

## ✨ Core Features

1. **Liquid Glass UI:** A custom, frosted-glass interface devoid of sharp edges to subconsciously reduce tension.
2. **MoodSync Technology:** An interactive calibration tool that adjusts the pod’s visual and auditory environment based on user-reported stress levels (1-10).
3. **Breathe With Me:** A locked-in "Kiosk Mode" featuring a guided, pulsing visual breathing exercise to physically slow the user's heart rate.
4. **Dynamic Audio Engine:** Integrates with the Jamendo API to dynamically fetch ambient or lo-fi audio tracks tailored to the user's current stress state.
5. **Zen Dashboard:** Tracks the user's stress reduction ("Delta") over time and rewards consistency with a gamified Zen Score.

---

## 🛠️ Tech Stack & Architecture

* **Framework:** Python / Streamlit
* **Frontend:** Custom HTML5 / CSS3 (Glassmorphism & CSS Keyframe Animations)
* **APIs Used:** * `ZenQuotes API` (For dynamic daily mindfulness nudges)
  * `Jamendo API` (For dynamic, stress-mapped background music)
* **Visuals:** Dynamic high-resolution CSS backgrounds (iPad/Safari safe)

---

## 🚀 How to Run Locally

1. Clone this repository:
   ```bash
   git clone [https://github.com/monkey8D8luffy/IDAI106-1000323-saurav.git](https://github.com/monkey8D8luffy/IDAI106-1000323-saurav.git)
