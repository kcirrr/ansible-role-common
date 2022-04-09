"""Role testing files using testinfra."""

import pytest


def test_systemd_resolved_file(host):
    filename = host.file("/etc/systemd/resolved.conf")
    assert filename.exists
    assert filename.contains("9.9.9.9")
    assert filename.user == "root"
    assert filename.group == "root"
    assert filename.mode == 0o644


def test_systemd_resolved_running_and_enabled(host):
    servicename = host.service("systemd-resolved")
    assert servicename.is_running
    assert servicename.is_enabled


@pytest.mark.parametrize(
    "name",
    [
        ("aptitude"),
        ("bash-completion"),
        ("bsd-mailx"),
        ("ca-certificates"),
        ("curl"),
        ("dnsutils"),
        ("haveged"),
        ("info"),
        ("locales"),
        ("lsof"),
        ("ncdu"),
        ("openssh-client"),
        ("python3-openssl"),
        ("python3-pip"),
        ("rsync"),
        ("ssl-cert"),
        ("strace"),
        ("telnet"),
        ("time"),
        ("vim"),
        ("wget"),
    ],
)
def test_packages(host, name):
    pkg = host.package(name)
    assert pkg.is_installed


def test_locales(host):
    cmd = host.run("locale -a")
    assert "nl_NL.utf8" in cmd.stdout
    assert "en_US.utf8" in cmd.stdout


def test_default_locales_file(host):
    default_locales = host.file("/etc/default/locale")
    assert default_locales.contains("LANG=en_US.UTF-8")
    assert default_locales.contains("LC_TIME=nl_NL.UTF-8")


def test_timezone_file(host):
    timezone_file = host.file("/etc/timezone")
    assert timezone_file.contains("Europe/Amsterdam")


def test_systemd_timesyncd_file(host):
    f = host.file("/etc/systemd/timesyncd.conf")
    assert f.exists
    assert f.contains("0.nl.pool.ntp.org")
    assert f.contains("1.nl.pool.ntp.org")
    assert f.contains("2.nl.pool.ntp.org")
    assert f.contains("3.nl.pool.ntp.org")
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644


def test_systemd_timesyncd_running_and_enabled(host):
    s = host.service("systemd-timesyncd")
    assert s.is_running
    assert s.is_enabled


def test_motd_file(host):
    f = host.file("/etc/default/motd-news")
    assert f.contains("ENABLED=0")


def test_motd_news_timer_stopped_and_disabled(host):
    s = host.service("motd-news.timer")
    assert not s.is_running
    assert not s.is_enabled
    assert s.is_masked


def test_motd_news_stopped_and_disabled(host):
    s = host.service("motd-news")
    assert not s.is_running
    assert not s.is_enabled
    assert s.is_masked


def test_editor_vim(host):
    cmd = host.run("update-alternatives --display editor")
    assert "link currently points to /usr/bin/vim.basic" in cmd.stdout


def test_dhparam_file(host):
    f = host.file("/etc/ssl/certs/dhparam.pem")
    assert f.exists
    assert f.contains("8CAQI")
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644
