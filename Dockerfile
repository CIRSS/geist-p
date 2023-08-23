ARG PARENT_IMAGE=cirss/repro-parent:latest

FROM ${PARENT_IMAGE}

COPY exports /repro/exports

ADD ${REPRO_DIST}/boot-setup /repro/dist/
RUN bash /repro/dist/boot-setup

USER repro

RUN repro.require shell-notebook master ${REPROS_DEV}
RUN repro.require graphviz-runtime master ${REPROS_DEV} --util
RUN repro.require geist-p exports --demo

RUN repro.env REPRO_DEMO_TMP_DIRNAME tmp

CMD  /bin/bash -il
