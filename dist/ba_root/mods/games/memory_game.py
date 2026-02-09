# ba_meta require api 9
from __future__ import annotations

from typing import TYPE_CHECKING
import random

import babase
import bascenev1 as bs
from bascenev1lib.actor.onscreentimer import OnScreenTimer
from bascenev1lib.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Type, List, Sequence, Optional


class Player(bs.Player['Team']):
    def __init__(self) -> None:
        super().__init__()
        self.death_time: Optional[float] = None


class Team(bs.Team[Player]):
    pass


# ba_meta export bascenev1.GameActivity
class MemoryGame(bs.TeamGameActivity[Player, Team]):
    name = 'Memory Game'
    description = 'Memorize tiles and survive!'

    available_settings = [
        bs.BoolSetting('Epic Mode', default=False),
        bs.BoolSetting('Enable Bottom Credits', True),
    ]
    scoreconfig = bs.ScoreConfig(
        label='Survived', scoretype=bs.ScoreType.MILLISECONDS, version='B'
    )

    announce_player_deaths = True

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[bs.Session]) -> List[str]:
        return ['Sky Tiles']

    @classmethod
    def supports_session_type(cls, sessiontype: Type[bs.Session]) -> bool:
        return (
            issubclass(sessiontype, bs.DualTeamSession)
            or issubclass(sessiontype, bs.FreeForAllSession)
            or issubclass(sessiontype, bs.CoopSession)
        )

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._epic_mode = bool(settings.get('Epic Mode', False))
        self._credits = bool(settings.get('Enable Bottom Credits', True))

        self._timer: OnScreenTimer | None = None
        self._last_player_death_time: Optional[float] = None
        self._level_stage = 0

        # Base overrides
        self.default_music = (
            bs.MusicType.EPIC if self._epic_mode else bs.MusicType.SURVIVAL
        )
        self.slow_motion = self._epic_mode

        shared = SharedObjects.get()
        self._stand_material = bs.Material()
        self._stand_material.add_actions(
            conditions=('we_are_older_than', 1),
            actions=(('modify_part_collision', 'collide', True),),
        )
        self._no_collide = bs.Material()
        self._no_collide.add_actions(
            conditions=('we_are_older_than', 1),
            actions=(('modify_part_collision', 'collide', False),),
        )

        # Assets
        self._tile_mesh = bs.getmesh('buttonSquareOpaque')
        self._default_tex = bs.gettexture('achievementOffYouGo')

        self._tex_pool = {
            # powerups
            'curse': bs.gettexture('powerupCurse'),
            'health': bs.gettexture('powerupHealth'),
            'ice': bs.gettexture('powerupIceBombs'),
            'impact': bs.gettexture('powerupImpactBombs'),
            'mines': bs.gettexture('powerupLandMines'),
            'punch': bs.gettexture('powerupPunch'),
            'shield': bs.gettexture('powerupShield'),
            'sticky': bs.gettexture('powerupStickyBombs'),
            # characters
            'spaz': bs.gettexture('neoSpazIcon'),
            'zoe': bs.gettexture('zoeIcon'),
            'ninja': bs.gettexture('ninjaIcon'),
            'kronk': bs.gettexture('kronkIcon'),
            'mel': bs.gettexture('melIcon'),
            'jack': bs.gettexture('jackIcon'),
            'santa': bs.gettexture('santaIcon'),
            'frosty': bs.gettexture('frostyIcon'),
            'bones': bs.gettexture('bonesIcon'),
            'bear': bs.gettexture('bearIcon'),
            'penguin': bs.gettexture('penguinIcon'),
            'ali': bs.gettexture('aliIcon'),
            'cyborg': bs.gettexture('cyborgIcon'),
            'agent': bs.gettexture('agentIcon'),
            'wizard': bs.gettexture('wizardIcon'),
            'pixie': bs.gettexture('pixieIcon'),
        }

        # UI
        self._bg_image = bs.newnode(
            'image',
            attrs={
                'texture': bs.gettexture('bg'),
                'position': (0, -100),
                'scale': (100, 100),
                'opacity': 0.0,
                'attach': 'topCenter',
            },
        )
        self._counter_text = bs.newnode(
            'text',
            attrs={
                'text': '10',
                'position': (0, -100),
                'scale': 2.3,
                'shadow': 1.0,
                'flatness': 1.0,
                'opacity': 0.0,
                'v_attach': 'top',
                'h_attach': 'center',
                'h_align': 'center',
                'v_align': 'center',
            },
        )
        self._level_text = bs.newnode(
            'text',
            attrs={
                'text': 'Level 0',
                'position': (0, -28),
                'scale': 1.3,
                'shadow': 1.0,
                'flatness': 1.0,
                'color': (1.0, 0.0, 1.0),
                'opacity': 0.0,
                'v_attach': 'top',
                'h_attach': 'center',
                'h_align': 'center',
                'v_align': 'center',
            },
        )

        # Tile grid structures
        self._tiles: list[dict[str, bs.Node]] = []
        self._selected_tex: bs.Texture | None = None

        # Sounds
        self._snd_bell_low = bs.getsound('bellLow')
        self._snd_bell_med = bs.getsound('bellMed')
        self._snd_bell_high = bs.getsound('bellHigh')
        self._snd_tick = bs.getsound('tick')
        self._snd_final = bs.getsound('powerup01')
        self._snd_score = bs.getsound('score')

        self._spawn_center = (-3.17358, 2.75764, -2.99124)

    def on_transition_in(self) -> None:
        super().on_transition_in()
        self._bg_image.opacity = 1.0
        self._counter_text.opacity = 1.0
        self._level_text.opacity = 1.0
        self._advance_level(initial=True)

    def on_begin(self) -> None:
        super().on_begin()
        self._timer = OnScreenTimer()
        self._timer.start()
        if self._credits:
            bs.newnode(
                'text',
                attrs={
                    'text': 'Memory Game by 1Freaku (orig. byANG3L)',
                    'scale': 0.7,
                    'position': (0, 0),
                    'shadow': 0.5,
                    'flatness': 1.2,
                    'color': (1, 1, 1),
                    'h_align': 'center',
                    'v_attach': 'bottom',
                },
            )
        self._spawn_all_tiles()
        self._hide_all_tiles(force_default=True)
        bs.timer(5.0, self._check_end_game)

    def _advance_level(self, initial: bool = False) -> None:
        self._level_stage += 1
        self._level_text.text = f'Level {self._level_stage}'
        start_delay = 6.0 if initial or self._level_stage == 1 else 2.0
        if not initial and self._level_stage > 1:
            self._snd_score.play()
            act = bs.getactivity()
            for p in act.players:
                if p.actor and p.actor.node.exists():
                    p.actor.node.handlemessage(bs.CelebrateMessage(2.0))
        bs.timer(start_delay, self._choose_pattern)
        bs.timer(start_delay, self._start_counter)

    def _start_counter(self) -> None:
        def seq(n: int) -> None:
            if n == 0:
                self._counter_text.text = ''
                self._snd_final.play()
                self._finalize_round()
                return
            self._counter_text.text = str(n)
            self._snd_tick.play()
            bs.timer(1.0, lambda: seq(n - 1))

        seq(10)

    def on_player_join(self, player: Player) -> None:
        if self.has_begun():
            bs.screenmessage(
                babase.Lstr(
                    resource='playerDelayedJoinText',
                    subs=[('${PLAYER}', player.getname(full=True))],
                ),
                color=(0, 1, 0),
            )
            assert self._timer is not None
            player.death_time = self._timer.getstarttime()
            return
        self.spawn_player(player)

    def on_player_leave(self, player: Player) -> None:
        super().on_player_leave(player)
        self._check_end_game()

    def spawn_player(self, player: Player) -> bs.Actor:
        spaz = self.spawn_player_spaz(player)
        pos = (
            self._spawn_center[0] + random.uniform(-1.5, 2.5),
            self._spawn_center[1],
            self._spawn_center[2] + random.uniform(-2.5, 1.5),
        )
        spaz.connect_controls_to_player(
            enable_punch=False, enable_bomb=False, enable_pickup=False
        )
        spaz.handlemessage(bs.StandMessage(pos))
        return spaz

    def _textures_for_level(self) -> list[bs.Texture]:
        if self._level_stage == 1:
            keys = ['mines', 'sticky']
        elif self._level_stage == 2:
            keys = ['ice', 'shield']
        elif self._level_stage in (3, 4, 5):
            keys = ['sticky', 'ice', 'impact', 'mines']
        elif self._level_stage in (6, 7, 8, 9):
            keys = ['curse', 'health', 'ice', 'impact', 'mines', 'punch', 'shield']
        else:
            keys = [
                'spaz', 'zoe', 'ninja', 'kronk', 'mel', 'jack', 'santa', 'frosty',
                'bones', 'bear', 'penguin', 'ali', 'cyborg', 'agent', 'wizard', 'pixie'
            ]
        return [self._tex_pool[k] for k in keys]

    def _choose_pattern(self) -> None:
        choices = random.sample(self._textures_for_level(), 16)
        self._selected_tex = choices[0]
        # Assign chosen textures to tiles.
        for i, t in enumerate(self._tiles):
            t['prop'].color_texture = choices[i]
        # Flash a few times, then leave shown briefly.
        def show_hide() -> None:
            self._show_all_tiles()
            bs.timer(2.0, self._hide_all_tiles)
        bs.timer(1.0, show_hide)
        bs.timer(4.0, show_hide)
        bs.timer(7.0, show_hide)
        bs.timer(13.2, self._show_all_tiles)

    def _finalize_round(self) -> None:
        # Delete wrong tiles.
        for t in self._tiles:
            if t['prop'].color_texture is not self._selected_tex:
                if t['prop'].exists():
                    t['prop'].delete()
                if t['region'].exists():
                    t['region'].delete()
        bs.timer(3.3, self._reset_after_round)

    def _reset_after_round(self) -> None:
        self._selected_tex = None
        self._hide_all_tiles(force_default=True)
        self._spawn_all_tiles()
        self._advance_level()

    def _spawn_all_tiles(self) -> None:
        shared = SharedObjects.get()
        if not self._tiles:
            self._tiles = [{'prop': None, 'region': None} for _ in range(16)]  # type: ignore
        positions = [
            (3, 1, -9), (3, 1, -6), (3, 1, -3), (3, 1, 0),
            (0, 1, -9), (0, 1, -6), (0, 1, -3), (0, 1, 0),
            (-3, 1, -9), (-3, 1, -6), (-3, 1, -3), (-3, 1, 0),
            (-6, 1, -9), (-6, 1, -6), (-6, 1, -3), (-6, 1, 0),
        ]
        for idx, pos in enumerate(positions):
            prop = bs.newnode(
                'prop',
                attrs={
                    'body': 'puck',
                    'position': pos,
                    'mesh': self._tile_mesh,
                    'mesh_scale': 3.8,
                    'body_scale': 3.8,
                    'shadow_size': 0.5,
                    'gravity_scale': 0.0,
                    'color_texture': self._default_tex,
                    'reflection': 'soft',
                    'reflection_scale': [1.0],
                    'is_area_of_interest': True,
                    'materials': [self._no_collide],
                },
            )
            region = bs.newnode(
                'region',
                attrs={
                    'position': pos,
                    'scale': (3.5, 0.1, 3.5),
                    'type': 'box',
                    'materials': (self._stand_material, shared.footing_material),
                },
            )
            self._tiles[idx]['prop'] = prop
            self._tiles[idx]['region'] = region

    def _hide_all_tiles(self, force_default: bool = False) -> None:
        for t in self._tiles:
            if t['prop'] and t['prop'].exists():
                t['prop'].color_texture = self._default_tex

    def _show_all_tiles(self) -> None:
        # textures already assigned
        pass

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PlayerDiedMessage):
            super().handlemessage(msg)
            curtime = bs.time()
            msg.getplayer(Player).death_time = curtime
            if isinstance(self.session, bs.CoopSession):
                babase.pushcall(self._check_end_game)
                self._last_player_death_time = curtime
            else:
                bs.timer(1.0, self._check_end_game)
        else:
            return super().handlemessage(msg)
        return None

    def _check_end_game(self) -> None:
        living = 0
        for team in self.teams:
            for p in team.players:
                if p.is_alive():
                    living += 1
                    break
        if isinstance(self.session, bs.CoopSession):
            if living <= 0:
                self.end_game()
        else:
            if living <= 1:
                self.end_game()

    def end_game(self) -> None:
        assert self._timer is not None
        start_time = self._timer.getstarttime()
        cur_time = bs.time()
        results = bs.GameResults()
        for team in self.teams:
            longest = 0.0
            for p in team.players:
                if p.death_time is None:
                    p.death_time = cur_time + 1
                assert p.death_time is not None
                longest = max(longest, p.death_time - start_time)
            results.set_team_score(team, int(1000.0 * longest))
        self.end(results=results)
