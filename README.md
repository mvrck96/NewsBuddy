# NewsBuddy

Sentiment analysis service for stock market news.

Main idea here is to perform sentiment analysis for wide spectrum of stock market news.
After understanding how to perform this type of analysis we can extract main entity from text.
Using extracted entity we can determine whether this news have a positive or negative impact on it.

## Architecture

Possible approach here is to use classic service configuration with front and backend.
Backend could utilize microservice architecture. And frontend could be designed as ordinary web interface. Alternatively we can use telegram bot as UI.   

## Tech stack

Possible technologies:
- Backend services - FastApi
- API validation - pydantic
- Logs - loguru
- UI - streamlit/telegram bot
- Tests - pytest
- Containerization Dockerfile + docker-compose
- Usage of pre-commiter

