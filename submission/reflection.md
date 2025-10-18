# ✍️ Project Reflection

## AI Tools Used
For this project, I primarily used ChatGPT as my AI development assistant. It helped me plan the program’s structure, generate pseudocode, and refine code for modular design, error handling, and data visualization. I also used GitHub Copilot occasionally inside VS Code to autocomplete small snippets and improve docstring consistency. ChatGPT was most valuable during the design and debugging phases—it explained why certain issues occurred, proposed alternative approaches, and helped me reason about trade-offs between simplicity and flexibility. I found that AI guidance saved time while still letting me understand every part of the solution.

## Prompting Techniques
I applied several intentional prompting strategies throughout development:

Restating the problem to ensure the AI clearly understood my task before coding.

Requesting pseudocode first, then converting it into modular Python code.

Challenging edge cases such as missing weather fields, invalid inputs, and network failures.

Iterative improvement—I asked follow-up prompts to rewrite early code with better structure, docstrings, and safe defaults.

Asking for design comparisons when choosing between APIs and data-handling methods.
These strategies kept conversations focused and ensured the generated code aligned with my project goals rather than generic solutions.

## What Worked Well?
One aspect I’m proud of is the modular architecture I implemented. Splitting the code into separate files—weather_data.py, nlp.py, visuals.py, and ui.py—made the program cleaner, easier to debug, and simpler to maintain. The visualization functions for temperature and precipitation turned out especially well; they display clear, labeled charts that complement the text-based responses. I’m also satisfied with the test section that checks for empty locations and clamps forecast days correctly.

## What Would You Do Differently?
If I had more time, I would integrate an additional OpenWeatherMap API layer for extended data and caching. This would allow the app to show longer forecasts and earn bonus marks. I’d also improve the conversational interface by incorporating a small natural-language model for more flexible question parsing rather than relying solely on keyword detection. These features would make the user experience smoother and more adaptive.

## Final Thoughts
This project was my first experience combining Python programming and AI-assisted development in one workflow. It taught me that AI is most effective when used intentionally, not blindly. By learning to guide it with structured prompts, I improved both my technical and communication skills. The process helped me see AI as a collaborative tool that supports human reasoning rather than replaces it. Overall, this assignment deepened my confidence in coding, problem-solving, and reflective practice.
