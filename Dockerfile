FROM multiarch/qemu-user-static:x86_64-aarch64 as qemu
FROM arm64v8/alpine
COPY --from=qemu /usr/bin/qemu-aarch64-static /usr/bin
COPY requirements.txt /
RUN apk add --no-cache python3 py3-pip
RUN pip3 install -r requirements.txt
COPY startup.py /
ENTRYPOINT python3 startup.py
