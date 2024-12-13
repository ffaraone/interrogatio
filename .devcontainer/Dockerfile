FROM python:3.12

RUN apt update && apt install -y vim

COPY pyproject.toml /tmp/pyproject.toml

RUN bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"

RUN echo 'CASE_SENSITIVE="true"' >> /root/.bashrc

RUN pip install -U pip && pip install poetry && mkdir -p /root/.config/pypoetry \
    && echo "[virtualenvs]" > /root/.config/pypoetry/config.toml \ 
    && echo "create = false" >> /root/.config/pypoetry/config.toml \
    && cd /tmp && poetry install --no-root
