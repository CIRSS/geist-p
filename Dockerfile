FROM cirss/repro-parent:latest

COPY exports /repro/exports

ADD ${REPRO_DIST}/boot-setup /repro/dist/
RUN bash /repro/dist/boot-setup

USER repro

RUN repro.require shell-notebook master ${REPROS_DEV}
RUN repro.require geist-p exports --demo

CMD  /bin/bash -il
