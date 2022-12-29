FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Expose the default port for the API (8000)
EXPOSE 8000

# Run the API server when the container launches
CMD ["python3", "main.py"]
