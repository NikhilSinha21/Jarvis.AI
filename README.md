Jarvis AI

A Python-powered personal desktop assistant

Jarvis AI is a Python-powered desktop assistant that responds to natural voice commands.
It can perform web searches, open websites, launch desktop applications, control system functions, and even speak with a bit of human-like hesitation (umm, uhh, hmm) for more natural interaction.

Implemented Features (v0.3+)
✅ Web & Knowledge Search

Perform instant searches using DuckDuckGo Search API (DDGS)

Smart fallback to Wikipedia summaries

Automatic cleaning of queries (search, lookup, etc. removed)

Returns text + images, and can open results in a browser

Filters out useless text like “5 hours ago”

✅ Voice Output

Speaks responses naturally with small fillers (umm, uhh, hmm, you know)

Randomized pauses for human-like flow

Reads only first 2 lines, then says:
“Here’s more information about it” and prints the rest

✅ Website & App Control

Open websites by name or direct URL

Launch installed desktop applications:

Camera

File Explorer

VS Code

Calculator

Notepad

✅ System Power Commands

Shutdown, restart, lock, sleep, etc.

✅ Messaging

Send messages through WhatsApp

Planned Features (Upcoming 🚀)

Play the first video or open the first search result automatically

Hand gesture recognition to control the PC without mouse/keyboard

Improved NLP with spaCy custom training for better command recognition

Integration with MediaPipe / OpenCV for gesture & face recognition

More natural conversational memory

Update History

Update 0.1

Added website opening feature

Added search functionality
(Note: Chrome may show "being controlled by automated test software")

Update 0.2

Added ability to open local desktop applications

Expanded supported commands list

Added WhatsApp messaging

Update 0.3

Added power commands (shutdown, restart, etc.)

Improved search with DuckDuckGo + Wikipedia fallback

Image fetching support

Query cleaning (removes “search/lookup …”)

Smarter voice output (first 2 lines + fillers for natural speech)