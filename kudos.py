from errbot import BotPlugin, botcmd, re_botcmd
from datetime import datetime
import re


class Kudos(BotPlugin):
    """Plugin to give kudos to an individual"""

    def update_kudos(self, username, count=1):
        """Updates db with current count"""

        username = str(username)

        try:
            current_count = self.get(username).get('kudos', 0)
            new_count = current_count + count
        except AttributeError:
            self[username] = {}
            new_count = count

        self.log.debug('new kudo count is {}'.format(new_count))

        self[username] = {
            'time': datetime.now(),
            'kudos': new_count,
        }

    @re_botcmd(pattern=r'^[\w-]+\+\+', prefixed=False, flags=re.IGNORECASE)
    def give_kudos(self, msg, match):
        """This gives kudos"""
        if match:
            line = match.group(0)
            username = line.split(' ')[0].rstrip('++')
            self.update_kudos(username)

            self.send(msg.frm,
                      'kudos updated for {}'.format(username),
                      message_type=msg.type,
                      in_reply_to=msg,
                      groupchat_nick_reply=True)

    @re_botcmd(pattern=r'^[\w-]+--', prefixed=False, flags=re.IGNORECASE)
    def remove_kudos(self, msg, match):
        """This removes a kudo"""
        self.send(msg.frm,
                  'Seriously...?',
                  message_type=msg.type,
                  in_reply_to=msg,
                  groupchat_nick_reply=True)

    @botcmd(admin_only=True)
    def kudos_delete_entries(self, msg, args):
        """Deletes all entries for a user"""
        username = str(args)

        try:
            del self[username]
            text = 'Entries deleted for {} user'.format(username)
        except KeyError:
            text = 'User {} has no entries'.format(username)

        self.send(msg.frm,
                  text,
                  message_type=msg.type,
                  in_reply_to=msg,
                  groupchat_nick_reply=True)

    @botcmd
    def kudos_list(self, msg, args):
        """Returns a list of users that have a kudo"""
        user_list = []
        for user in self.keys():
            user_list.append(user)

        if user_list == []:
            response = 'No users'
        else:
            response = ', '.join(user_list)

        self.send(msg.frm,
                  response,
                  message_type=msg.type,
                  in_reply_to=msg,
                  groupchat_nick_reply=True)

    @botcmd
    def kudos(self, msg, args):
        """A way to see your kudos stats
            Example:
                !kudos <username>
        """
        username = str(args)

        if username == '':
            self.send(msg.frm,
                      'Username is required.',
                      message_type=msg.type,
                      in_reply_to=msg,
                      groupchat_nick_reply=True)
            return

        try:
            count = self.get(username).get('kudos')
        except (TypeError, NameError, AttributeError):
            count = 0

        self.send(msg.frm,
                  '{} has {} kudo points.'.format(username, count),
                  message_type=msg.type,
                  in_reply_to=msg,
                  groupchat_nick_reply=True)
