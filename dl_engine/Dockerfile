FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y \
gcc && \
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
chmod a+rx /usr/local/bin/yt-dlp && \
yum clean all && \
rm -rf /var/cache/yum


COPY requirements.txt  .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY app.py ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]
