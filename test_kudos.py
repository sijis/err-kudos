from errbot import plugin_manager
from errbot.backends.test import testbot

import kudos

USERNAMES = [
    "sijis",
    "Sijis",
    "foo",
    "bar",
    "_baz",
    "Baz_",
    "_zo_o",
    "_f-o-o",
    "si-ji_s",
]


class TestKudos(object):
    extra_plugin_dir = "."

    def test_delete_kudos_list_empty(self, testbot):
        testbot.push_message("!kudos list")
        assert "No users" in testbot.pop_message()

    def test_delete_kudos_user_empty(self, testbot):
        for username in USERNAMES:
            testbot.push_message(f"!kudos delete_entries {username}")
            assert f"User {username} has no entries" in testbot.pop_message()

    def test_give_kudos(self, testbot):
        for username in USERNAMES:
            testbot.push_message(f"!{username}++")
            assert f"kudos updated for {username}" in testbot.pop_message()

    def test_give_kudos_with_comment(self, testbot):
        for username in USERNAMES:
            testbot.push_message(f"!{username}++ This is super great!")
            assert f"kudos updated for {username}" in testbot.pop_message()

    def test_give_kudos_at_end(self, testbot):
        for username in USERNAMES:
            testbot.push_message(f"This is super great! {username}++")
            assert f"kudos updated for {username}" in testbot.pop_message()

    def test_delete_kudos_user(self, testbot):
        for username in USERNAMES:
            testbot.push_message(f"!{username}++")
            assert f"kudos updated for {username}" in testbot.pop_message()
            testbot.push_message(f"!kudos delete_entries {username}")
            assert f"Entries deleted for {username} user" in testbot.pop_message()

    def test_delete_kudos_list(self, testbot):
        testbot.push_message("!sijis++")
        assert "kudos updated for sijis" in testbot.pop_message()
        testbot.push_message("!tom++")
        assert "kudos updated for tom" in testbot.pop_message()
        testbot.push_message("!kudos list")
        assert "sijis, tom" in testbot.pop_message()

    def test_kudos_stats(self, testbot):
        for username in USERNAMES:
            testbot.push_message(f"!{username}++")
            testbot.pop_message()
            testbot.push_message(f"!kudos {username}")
            assert f"{username} has 1 kudo points" in testbot.pop_message()

    def test_kudos_stats_empty(self, testbot):
        testbot.push_message("!kudos sijis_empty")
        assert "sijis_empty has 0 kudo points" in testbot.pop_message()

    def test_kudos_blank_user(self, testbot):
        testbot.push_message("!kudos")
        assert "Username is required." in testbot.pop_message()
