# Light - UserBot
# Copyright (C) 2021-2022 CodeByTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE/>.

FROM theteamultroid/ultroid:main

# set timezone
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY installer.sh .

RUN bash installer.sh

# changing workdir
WORKDIR "/root/TeamUltroid"

# start the bot.
CMD ["bash", "startup"]
