FROM golang:1.15.7-alpine3.13

ENV GO111MODULE=on

WORKDIR /app/erupe

COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .

CMD [ "go", "run", "." ]