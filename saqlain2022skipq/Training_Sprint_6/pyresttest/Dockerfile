FROM thoom/pyresttest

WORKDIR /usr/src/app

COPY . /usr/src/app

ENTRYPOINT [ "pyresttest" ]

CMD ["https://0h8npgak0j.execute-api.us-east-2.amazonaws.com/","basic_api_test.yml"]