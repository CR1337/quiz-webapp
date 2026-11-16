# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Install: `python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`
- Run: `bin/run` (wraps `streamlit run app.py "$@"`; Windows: `bin\run`). Serves on port 8501.
- Load a different question file: append `?question_filename=<path>` to the app URL.

There is no test suite, linter, or build step. All paths are relative to the repo root, so always run the app and tools from there (e.g. `python tools/reindexer.py`).

## Architecture

Streamlit app; `app.py` reruns top to bottom on every interaction. It calls `render_main()` (`app/pages/main.py`), which loads `Localization` and `Config`, configures the page, and on first run (when `st.session_state["question_index"]` is `None`) validates the question file, selects questions, and initializes session state. `app.py` then dispatches on `st.session_state["state"]` (`QuizState`: `INIT → QUESTION ⇄ SOLUTION → RESULT`) to the render function in `app/pages/`. Page transitions happen by mutating `st.session_state` and calling `st.rerun()`; resetting `question_index` to `None` restarts the quiz.

Key session-state keys: `questions`, `question_index`, `state`, `score`, `max_points`, `last_score`, `answer`, `slider_moved`, `language`, `scroll_to_top`.

- **Question model** (`app/question_model/`): `Question` is an abstract dataclass with `get_max_points()` and `check(answer) -> (correct, points)`. `QuestionFactory` builds `MultipleChoiceQuestion` or `GuessQuestion` by passing the JSON dict as `**kwargs`, so JSON field names must match dataclass fields exactly. A new field means updating the dataclass, `data/questions-schema.json` and `data/questions.json` together.
- **Validation** (`app/validation.py`): JSON-schema validation plus extra checks (image files exist in `images/questions/` for both languages, `len(scores) == len(answers.de)`).
- **Question selection** (`app/question_selection.py`): driven by `data/config.json`, using one of the methods `all`, `list`, `random`, `random_set` or `exclude_list`, plus `group_coupled_questions` and `shuffle_questions`. Coupled questions (`coupled_question_indices`) are kept together when grouping is on.
- **Localization** (`app/localization.py`): everything user-facing is German/English (`{"de": ..., "en": ...}`), with German as the default. UI strings live in `data/static_localization.json` (app strings) and `data/dynamic_localization.json` (quiz-specific texts such as intro and thank-you); the two are merged. Question fields are localized inline in `questions.json`.
- **Colors**: `data/colors.json` (RGB tuples via `app/colors.py`), and the Streamlit theme lives in `.streamlit/config.toml`. The progress badges are rendered from `app/html/badge.html.template` inside an `st.iframe`.
- **Images**: the intro images are `images/title{N}_{lang}.png|jpg` (all consecutive N are shown), the result images are `images/result_{lang}.png`, and question images go in `images/questions/`.

## Data format notes (README is partly outdated)

- Multiple choice questions use `scores` (a list with one entry per answer, where max points = `max(scores)`), not a single `score`. `answers` is `{"de": [...], "en": [...]}`, not a list of localized objects.
- Guess questions also require `min_scoring_guess`, `max_scoring_guess` (answers outside the range score 0, with points decaying linearly toward the edges) and `is_hm_time` (shows the value as hours and minutes). The decimal places of the slider are derived from `answer`.

## Tools (`tools/`, one-off scripts)

- `question_exporter.py` bundles questions, config, dynamic localization and images into `quiz.zip`. `question_importer.py <zip>` extracts one into the repo, and the in-app uploader on the init page does the same when `config.json` has `"question_importer": true`.
- `reindexer.py` rewrites each `index` to its list position. `question_translator.py` fills `"TODO"` English fields via Google Translate. Both overwrite `data/questions.json` and ask whether it is committed first.
- `question_updater.py` migrates old-format questions to the current schema. `jpg_to_png.py <file>` converts an image and deletes the original.
