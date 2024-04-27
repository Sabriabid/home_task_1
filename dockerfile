# Set base image
FROM python:3.9-slim

# Define working directory
WORKDIR /app

# Copy dependency files and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other project files into the container
COPY . .
RUN chmod +x start.sh  # Assurez-vous que le script est exécutable
# Expose the port used by the API
EXPOSE 5000

# Command to start the application
CMD ["./start.sh"]


