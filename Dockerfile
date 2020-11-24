# Base os for continer, LINUX OS
FROM alpine:3.12

# Install curl with no cache arg, curl to used for bash testing, python3 for python tests
RUN  apk --no-cache add curl python3

# Specify WORKDIR, After the layer, PWD will be mentioned WORKDIR
WORKDIR /usr/local/app

# Copy binary and other modules to WORKDIR
COPY hello hello
COPY app app
COPY .env .env
COPY test.py test.py

# Set default ENV variables
ENV PORT "8080"
ENV IP_ADDR "0.0.0.0"

# Default contianer executable default
# `&> server.log` directs std output & std log to server.log
CMD ["sh", "-c", "./hello -addr ${IP_ADDR}:${PORT} &> server.log"]
