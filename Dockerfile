ARG PARENT_IMAGE=cirss/repro-parent:latest

FROM ${PARENT_IMAGE}

COPY exports /repro/exports

# geist's own source, plus the selector telling base-setup to install from it.
# Only set here, in geist-p's own image; requirers leave GEIST_INSTALL unset
# (-> PyPI) or set it to "git" to install from the repo. See base-setup.
COPY pyproject.toml README.md LICENSE /repro/
COPY src /repro/src
ENV GEIST_INSTALL=source

ADD ${REPRO_DIST}/boot-setup /repro/dist/
RUN bash /repro/dist/boot-setup

USER repro

RUN repro.require shell-notebook master ${REPROS_DEV}
# RUN repro.require graphviz-runtime master ${REPROS_DEV} --util
RUN repro.require geist-p exports --demo

RUN repro.env REPRO_DEMO_TMP_DIRNAME tmp

CMD  /bin/bash -il
