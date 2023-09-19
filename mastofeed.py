###
# Mastefeed, bot para publicar datos en Mastodon a partir de un feed RSS
# Extiende de la clase Mastobot del paquete pybot
# Tiene los parámetros para la publicación en el fichero antions.yaml
# Tiene los parámetros internos de funcionamiento en el fichero config.yaml
###  

from pybot.mastobot import Mastobot
from datetime import datetime, timedelta
import feedparser
import random

BOT_NAME = "D13"

class Bot(Mastobot):

    def __init__(self, botname: str = BOT_NAME) -> None:

        super().__init__(botname = botname)
        self.init_publish_bot()
        self.init_repetition_control()


    def run(self, botname: str = BOT_NAME) -> None:

        post       = 0
        max        = int(self._actions.get("feed.max"))
        now        = datetime.now()
        time_range = timedelta(days=int((self._actions.get("feed.days"))))
 
        feed = feedparser.parse(self._actions.get("feed.url"))

        if self._actions.get("feed.reverse"):
            sorted_entried  = sorted(feed.entries, reverse=True, key=lambda entry : entry.published_parsed)
        else:
            sorted_entried  = sorted(feed.entries, key=lambda entry : entry.published_parsed)
        
        for entry in sorted_entried:

            if self.check_entry(entry, now, time_range):
                self.post_toot (self.find_text(entry), "es")
                post = post + 1
            
            if max > 0 and post >= max:
                break        
 
        super().run(botname = botname)


    def check_entry(self, entry, now, time_range) -> bool:

        valid = False

        # Control de data
        entry_date = (datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")).replace(tzinfo=None)

        if now - entry_date <= time_range:
 
            # Control de repeticions
            indexes = [i for i, c in enumerate(entry.link) if c == "/"]
            valid = self.check_repetition (entry.link[indexes[2]:], self._actions.get("feed.repetitions"))
          
        return valid


    def find_text(self, entry):        
    
        text_list = []
        title  = entry.title                   
        link   = entry.link

        text_list.append(random.choice(self._actions.get("feed.announcement")))
        text_list.append("\n")

        text_list.append(str(entry.published_parsed[2]))
        text_list.append("/")
        text_list.append(str(entry.published_parsed[1]))
        text_list.append("/")
        text_list.append(str(entry.published_parsed[0]))
        text_list.append(": ")
        text_list.append(title)
        text_list.append("\n\n")

        text_list.append(link)
        text_list.append("\n\n")

        text_list.append(self._actions.get("feed.hashtags")) 

        post_text  = "".join(text_list)

        post_text = (post_text[:self._max_lenght] + '... ') if len(post_text) > self._max_lenght else post_text
        self._logger.debug ("answer text\n%s", post_text)

        return post_text


# main

if __name__ == '__main__':
    Bot().run()
