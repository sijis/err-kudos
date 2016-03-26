import kudos
from errbot.backends.test import testbot
from errbot import plugin_manager


class TestKudos(object):
    extra_plugin_dir = '.'

    def test_delete_kudos_list_empty(self, testbot):
        testbot.push_message('!kudos list')
        assert 'No users' in testbot.pop_message()

    def test_delete_kudos_user_empty(self, testbot):
        testbot.push_message('!kudos delete_entries sijis')
        assert 'User sijis has no entries' in testbot.pop_message()

    def test_give_kudos(self, testbot):
        testbot.push_message('!sijis++')
        assert 'kudos updated for sijis' in testbot.pop_message()

    def test_remove_kudos(self, testbot):
        testbot.push_message('!sijis--')
        assert 'Seriously...?' in testbot.pop_message()

    def test_delete_kudos_user(self, testbot):
        testbot.push_message('!sijis++')
        assert 'kudos updated for sijis' in testbot.pop_message()
        testbot.push_message('!kudos delete_entries sijis')
        assert 'Entries deleted for sijis user' in testbot.pop_message()

    def test_delete_kudos_list(self, testbot):
        testbot.push_message('!sijis++')
        assert 'kudos updated for sijis' in testbot.pop_message()
        testbot.push_message('!tom++')
        assert 'kudos updated for tom' in testbot.pop_message()
        testbot.push_message('!kudos list')
        assert 'sijis, tom' in testbot.pop_message()

    def test_kudos_stats(self, testbot):
        testbot.push_message('!sijis++')
        testbot.pop_message()
        testbot.push_message('!kudos sijis')
        assert 'sijis has 1 kudo points' in testbot.pop_message()

    def test_kudos_stats_empty(self, testbot):
        testbot.push_message('!kudos sijis_empty')
        assert 'sijis_empty has 0 kudo points' in testbot.pop_message()

    def test_kudos_blank_user(self, testbot):
        testbot.push_message('!kudos')
        assert 'Username is required.' in testbot.pop_message()
