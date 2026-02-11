## Base image 
FROM python:3.11-slim

## Work directory
WORKDIR /app

## copy all the requirements in comtainer env
COPY requirements.txt .

## inatall requirement to the docker env
RUN pip install -r requirements.txt

## copy all the installed requirements to the docker container
COPY . .

## Expose port
EXPOSE 5000

# ## spacific command that cant be override via CMD
# ENTRYPOINT ["python"]

## for runing the application 
CMD ["python","app.py"]