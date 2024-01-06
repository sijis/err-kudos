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
            testbot.push_message("!kudos delete_entries {0}".format(username))
            assert "User {0} has no entries".format(username) in testbot.pop_message()

    def test_give_kudos(self, testbot):
        for username in USERNAMES:
            testbot.push_message("!{0}++".format(username))
            assert "kudos updated for {0}".format(username) in testbot.pop_message()

    def test_give_kudos_with_comment(self, testbot):
        for username in USERNAMES:
            testbot.push_message("!{0}++ This is super great!".format(username))
            assert "kudos updated for {0}".format(username) in testbot.pop_message()

    def test_give_kudos_at_end(self, testbot):
        for username in USERNAMES:
            testbot.push_message("This is super great! {0}++".format(username))
            assert "kudos updated for {0}".format(username) in testbot.pop_message()

    def test_remove_kudos(self, testbot):
        for username in USERNAMES:
            testbot.push_message("!{0}--".format(username))
            assert "Seriously...?" in testbot.pop_message()

    def test_delete_kudos_user(self, testbot):
        for username in USERNAMES:
            testbot.push_message("!{0}++".format(username))
            assert "kudos updated for {0}".format(username) in testbot.pop_message()
            testbot.push_message("!kudos delete_entries {0}".format(username))
            assert (
                "Entries deleted for {0} user".format(username) in testbot.pop_message()
            )

    def test_delete_kudos_list(self, testbot):
        testbot.push_message("!sijis++")
        assert "kudos updated for sijis" in testbot.pop_message()
        testbot.push_message("!tom++")
        assert "kudos updated for tom" in testbot.pop_message()
        testbot.push_message("!kudos list")
        assert "sijis, tom" in testbot.pop_message()

    def test_kudos_stats(self, testbot):
        for username in USERNAMES:
            testbot.push_message("!{0}++".format(username))
            testbot.pop_message()
            testbot.push_message("!kudos {0}".format(username))
            assert "{0} has 1 kudo points".format(username) in testbot.pop_message()

    def test_kudos_stats_empty(self, testbot):
        testbot.push_message("!kudos sijis_empty")
        assert "sijis_empty has 0 kudo points" in testbot.pop_message()

    def test_kudos_blank_user(self, testbot):
        testbot.push_message("!kudos")
        assert "Username is required." in testbot.pop_message()
