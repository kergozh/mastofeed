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

        feed = feedparser.parse(self._actions.get("feed.url"))

        for entry in feed.entries:
            if self.check_entry(entry):
                self.post_toot (self.find_text(entry), "en")    
 
        super().run(botname = botname)


    def check_entry(self, entry) -> bool:

        valid = False

        # Control de data

        now        = datetime.now()
        time_range = timedelta(days=(self._actions.get("feed.days")))
        entry_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")

        if now - entry_date <= time_range:
 
            # Control de repeticions
            if not self.check_repetition (entry.link, self._actions.get("publish.repetitions")):
                valid = True
          
        return valid


    def find_text(self, entry):        
    
        text_list = []
        title  = entry.title                   
        link   = entry.link                
        sumary = entry.sumary 

        self._logger.debug("id      : %s", str(quote[0]))                    
        self._logger.debug("text    : %s", text)                    
        self._logger.debug("comments: %s", comments)                     
        self._logger.debug("source  : %s", source)   
         
        text_list.append(text)
        text_list.append("\n\n")

        if comments != "":
            text_list.append(comments)
            text_list.append("\n")

        text_list.append(source)
        text_list.append("\n\n")

        hashtag = "#GNUTerryPratchett, #SpeakHisName, #Discworld" 

        if len("".join(text_list)) + len(hashtag) < self._max_lenght:
            text_list.append(hashtag) 

        post_text  = "".join(text_list)

        post_text = (post_text[:self._max_lenght] + '... ') if len(post_text) > self._max_lenght else post_text
        self._logger.debug ("answer text\n%s", post_text)

        return post_text


# main

if __name__ == '__main__':
    Bot().run()
