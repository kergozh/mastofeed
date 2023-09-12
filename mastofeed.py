###
# Mastefeed, bot para publicar datos en Mastodon a partir de un feed RSS
# Extiende de la clase Mastobot del paquete pybot
# Tiene los parámetros para la publicación en el fichero antions.yaml
# Tiene los parámetros internos de funcionamiento en el fichero config.yaml
###  

from pybot.mastobot import Mastobot
from datetime import datetime, timedelta
import feedparser

BOT_NAME = "D13"

class Bot(Mastobot):

    def __init__(self, botname: str = BOT_NAME) -> None:

        super().__init__(botname = botname)
        self.init_publish_bot()
        self.init_repetition_control()


    def run(self, botname: str = BOT_NAME) -> None:

        now        = datetime.now()
        time_range = timedelta(days=int((self._actions.get("feed.days"))))
 
        feed = feedparser.parse(self._actions.get("feed.url"))

        for entry in feed.entries:
            if self.check_entry(entry, now, time_range):
                self.post_toot (self.find_text(entry), "es")    
 
        super().run(botname = botname)


    def check_entry(self, entry, now, time_range) -> bool:

        valid = False

        # Control de data
        entry_date = (datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")).replace(tzinfo=None)

        if now - entry_date <= time_range:
 
            # Control de repeticions
            valid = self.check_repetition (entry.link, self._actions.get("feed.repetitions"))
          
        return valid


    def find_text(self, entry):        
    
        text_list = []
        title  = entry.title                   
        link   = entry.link                

        self._logger.debug("id      : %s", title)                    
        self._logger.debug("text    : %s", link)                    
         
        text_list.append(title)
        text_list.append("\n\n")

        text_list.append(link)
        text_list.append("\n\n")

        hashtag = "#webcomic, #rol, #elSistemaD13" 
        text_list.append(hashtag) 

        post_text  = "".join(text_list)

        post_text = (post_text[:self._max_lenght] + '... ') if len(post_text) > self._max_lenght else post_text
        self._logger.debug ("answer text\n%s", post_text)

        return post_text


# main

if __name__ == '__main__':
    Bot().run()
