import re
import string

from app.transformers.base import BaseTransformer

class UrlTransformer(BaseTransformer):

    def __init__(self):
        super().__init__()
        self.pattern = r"http\S+"

    def transform(self, input):
        inputCleanedUrls = re.sub(self.pattern, "", input)
        return inputCleanedUrls
