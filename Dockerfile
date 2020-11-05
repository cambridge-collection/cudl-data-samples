FROM python:3.9-alpine as sampler

COPY cudl-data/json /usr/share/dl-data/json
COPY cudl-data/data /usr/share/dl-data/data

ARG RANDOM_SEED=a
ARG ITEM_COUNT=20

WORKDIR /opt/dl-data
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY random_lines.py .
COPY data_paths.py .
RUN chmod +x *.py
ENV PATH=/opt/dl-data:$PATH

RUN mkdir -p /usr/share/dl-data-samples && \
    cd /usr/share/dl-data && \
    find json -type f \
    | random_lines.py -s "${RANDOM_SEED}" -n "${ITEM_COUNT}" \
    | data_paths.py \
    | xargs -I {} install -D {} "../dl-data-samples/{}"

FROM tianon/true as main
COPY --from=sampler /usr/share/dl-data-samples /data
