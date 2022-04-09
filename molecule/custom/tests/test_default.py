"""Role testing files using testinfra."""


def test_apt_sources_file(host):
    apt_sources = host.file("/etc/apt/sources.list")
    assert apt_sources.exists
    assert apt_sources.contains("nl.archive.ubuntu.com")
    assert apt_sources.user == "root"
    assert apt_sources.group == "root"
    assert apt_sources.mode == 0o644


def test_systemd_resolved_stopped_and_disabled(host):
    s = host.service("systemd-resolved")
    assert not s.is_running
    assert not s.is_enabled
    assert s.is_masked


def test_systemd_timesyncd_stopped_and_disabled(host):
    s = host.service("systemd-timesyncd")
    assert not s.is_running
    assert not s.is_enabled
    assert s.is_masked
