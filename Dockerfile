FROM odoo:18.0

USER root

RUN apt-get update && apt-get install -y \
    git \
    vim \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    black \
    flake8 \
    isort \
    pytest \
    psycopg2-binary

USER odoo

WORKDIR /mnt/extra-addons

COPY --chown=odoo:odoo addons/ /mnt/extra-addons/

COPY --chown=odoo:odoo config/odoo.conf /etc/odoo/

EXPOSE 8069

CMD ["odoo"]
