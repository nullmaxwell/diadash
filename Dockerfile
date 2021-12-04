FROM python:3.9.7
LABEL maintainer="nullmaxwell <nullmaxwell@protonmail.com>"

WORKDIR /diadash

COPY . .
RUN python3 -m pip install -U pip setuptools wheel
RUN	python3 -m pip install -r requirements.txt

EXPOSE 8050

RUN make clean
CMD [ "make", "dash" ]
