import re
import string

from app.transformers.base import BaseTransformer
from app.transformers.emoji_mappings import EMOJI_MAPPINGS

class EmojiTransformer(BaseTransformer):

    def __init__(self):
        super().__init__()
        self.pattern = r"<a?:([a-zA-Z0-9_-]{1,32}):[0-9]{17,21}>"
        self.mappings = EMOJI_MAPPINGS

    def transform(self, input):
        emojiReplacedInput = re.sub(self.pattern, r"\1", input)
        sentimentReplacedInput = self._replace(emojiReplacedInput)
        return sentimentReplacedInput

    def _replace(self, input):

        tokens = input.split(' ')
        transformedStr = []

        for word in tokens:
            wordWithNoPunctuation = word.translate(str.maketrans('', '', string.punctuation))

            if wordWithNoPunctuation in self.mappings:
                transformedStr.append(self.mappings[wordWithNoPunctuation])
            else:
                transformedStr.append(word)

        return ' '.join(transformedStr)

    def _isEmoji(self, word):
        return word[0] == ":" and word[-1] == ":"
