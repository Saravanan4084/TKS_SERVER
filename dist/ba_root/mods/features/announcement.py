import random

import babase
import setting

import bascenev1 as bs
from bascenev1lib.actor.text import Text

setti = setting.get_settings_data()


def showScoreScreenAnnouncement():
    if setti["ScoreScreenAnnouncement"]["enable"]:
        color = ((0 + random.random() * 1.0), (0 + random.random() * 1.0),
                 (0 + random.random() * 1.0))
        msgs = setti["ScoreScreenAnnouncement"]["msg"]
        bs.broadcastmessage(random.choice(msgs), color=color)


def show_mvp_and_most_violent(activity) -> None:
    """Show MVP and Most Violent on the same score screen background, visible during the whole announcement."""
    def _show(act):
        if not act or not act.exists():
            return
        try:
            stats = act.stats
            records = list(stats.get_records().values())
        except Exception:
            return
        if not records:
            return
        mvp = max(records, key=lambda r: r.accumscore)
        most_violent = max(records, key=lambda r: r.accum_kill_count)
        with act.context:
            mvp_name = mvp.getname(full=True)
            violent_name = most_violent.getname(full=True)
            # Same coordinate space as score screen (center 0,0); draw in front so they stay visible
            Text(
                babase.Lstr(value='${A} ${B}', subs=[('${A}', babase.Lstr(value='MVP:')), ('${B}', mvp_name)]),
                position=(0, 200),
                h_attach=Text.HAttach.CENTER,
                v_attach=Text.VAttach.CENTER,
                h_align=Text.HAlign.CENTER,
                scale=1.0,
                color=(1.0, 0.85, 0.4, 1.0),
                transition=Text.Transition.FADE_IN,
                transition_delay=0.0,
                front=True,
            ).autoretain()
            Text(
                babase.Lstr(value='${A} ${B}', subs=[('${A}', babase.Lstr(value='Most Violent:')), ('${B}', violent_name)]),
                position=(0, 165),
                h_attach=Text.HAttach.CENTER,
                v_attach=Text.VAttach.CENTER,
                h_align=Text.HAlign.CENTER,
                scale=1.0,
                color=(0.9, 0.35, 0.35, 1.0),
                transition=Text.Transition.FADE_IN,
                transition_delay=0.05,
                front=True,
            ).autoretain()

    bs.timer(0.05, bs.WeakCall(activity, _show))
