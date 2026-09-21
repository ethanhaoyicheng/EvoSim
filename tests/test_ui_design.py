from ui_design import Shell


def test_home_shell_defaults():
    shell = Shell("home")

    assert shell.music_volume == 0.5
    assert shell.sfx_volume == 0.5
    assert shell.music_muted is False
    assert shell.sfx_muted is False
    assert shell.running is True
    assert shell.brightness == 1
    assert shell.colorid == 0


def test_sim_shell_defaults():
    shell = Shell("sim")

    assert shell.music_volume == 0.5
    assert shell.sfx_volume == 0.5
    assert shell.ui_visible is True
    assert shell.sim_speed == 1
    assert shell.paused is False
    assert shell.running is True
    assert shell.brightness == 1
    assert shell.tutorial_index == 0
    assert shell.ctutorial_index == 0
    assert shell.anima_to_view is None
