FROM thoom/pyresttest

WORKDIR /usr/app

COPY rest_tests/ ${WORKDIR}

# ENV url=https://kapjchmsw8.execute-api.us-east-2.amazonaws.com
# ENV file=restApi_test.yml

ENTRYPOINT [ "pyresttest"]

CMD ["https://kapjchmsw8.execute-api.us-east-2.amazonaws.com", "restApi_test.yml"]

# CMD ${url} ${file}

# -v D:/Docker/pyresttest/rest_tests