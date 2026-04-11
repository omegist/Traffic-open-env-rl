FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -c "from graders import GRADERS; assert len(GRADERS)==3, f'Only {len(GRADERS)} graders found!'"
ENV PYTHONPATH=/app
ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]
