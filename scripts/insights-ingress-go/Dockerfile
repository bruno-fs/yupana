from python:3.9

ENV FLASK_APP=ingress_wrapper.py

RUN pip install -U pip -q &&\
    pip install 'flask<3' requests -q
ADD ingress_wrapper.py .
EXPOSE 5000
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]