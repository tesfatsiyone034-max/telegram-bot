FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Run bot
CMD ["python", "bot.py"]