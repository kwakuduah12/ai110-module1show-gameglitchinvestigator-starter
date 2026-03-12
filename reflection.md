# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  "the number of tries didn't match the information in developer debugger info"
  "number of attempts is inconsistent with error message"
  "score in developer debugger info is inconsistent with error message"
  "history board is not cleared when new game button is clicked"
  "hint message misleads user"

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude Code (Claude Sonnet) as my primary AI tool throughout this project to help identify and fix the bugs in the starter code.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
**Correct AI suggestion — swapped hint messages in `check_guess()`:**
The AI correctly identified that the hint messages in `logic_utils.py` were backwards: when `guess > secret`, the code was returning `"Go HIGHER!"` instead of `"Go LOWER!"`, and vice versa. The AI suggested swapping the message strings so that `"Too High"` maps to `"📈 Go LOWER!"` and `"Too Low"` maps to `"📉 Go HIGHER!"`. I verified this by running the game, entering a number I knew was above the secret (visible in the Developer Debug Info expander), and confirming the hint now correctly told me to go lower rather than higher.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
**Incorrect/misleading AI suggestion — partial new-game reset:**
When I asked about the history board not clearing on new game, the AI initially suggested only resetting `st.session_state.history = []` in the `new_game` block. That seemed right at first — the history list did clear. However, the game immediately stopped working after clicking New Game because `st.session_state.status` was still set to `"won"` or `"lost"` from the previous game, which caused `st.stop()` to fire before any guesses could be made. The AI's suggestion was incomplete. I verified the real issue by checking the Developer Debug Info and noticing `status` still held the old value. The correct fix required also resetting `st.session_state.status = "playing"` and `st.session_state.score = 0` alongside the history reset.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
A bug was only considered fixed when I could reproduce the original broken behavior, apply the change, and then confirm the broken behavior was gone. For UI-level bugs I used the Developer Debug Info expander to watch session state values in real time while clicking through the game. For logic bugs I relied on pytest to give a pass/fail result I could trust across multiple inputs.

- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
I ran `pytest tests/test_game_logic.py` after fixing the swapped hint messages. The two new tests — `test_too_high_hint_directs_player_lower` and `test_too_low_hint_directs_player_higher` — both passed, confirming that `check_guess(80, 50)` now returns a message containing `"LOWER"` and `check_guess(20, 50)` returns one containing `"HIGHER"`. A third test, `test_swapped_hints_not_present`, explicitly checked that the old wrong behavior no longer occurred, which gave extra confidence the fix was complete and didn't just accidentally pass.

- Did AI help you design or understand any tests? How?
Yes. After fixing the hint bug I asked the AI to suggest tests that would catch the original problem if it ever came back. It recommended testing both the outcome label and the message string separately, and also adding a negative test (`test_swapped_hints_not_present`) that would fail if someone accidentally re-introduced the old swap. That pattern — pairing a positive assertion with a negative one — was something I hadn't thought to do on my own, and I reused it for the decimal-input tests as well.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
