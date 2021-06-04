# coding=utf-8

from typing import List


class CryptomarketSDKException(Exception):
    def __init__(self, message):
        self.message = message

        
class CryptomarketAPIException(CryptomarketSDKException):
    def __init__(self, response=None):
        self.code = 0
        if response is None:
            self.message = ""
            return
        
        try:
            json_res = response.json()
        except ValueError:
            self.message = 'Invalid JSON error message from Cryptomarket: {}'.format(response.text)
        else:
            error = json_res['error']
            self.code = error['code']
            self.message = error['message']
            if 'description' in error:
                self.message += '. ' + error['description']
        self.status_code = response.status_code
        self.response = response
    
    @classmethod
    def from_dict(cls, response):
        e = CryptomarketAPIException()
        e.status_code = None
        e.response = response
        e.code = response["error"]["code"]
        message = response["error"]["message"]
        if "description" in response["error"]:
            message += ". " + response["error"]["description"]
        e.message = message
        return e


    def __str__(self):
        return f'CryptomarketAPIError(code={self.code}): {self.message}'

class ArgumentFormatException(CryptomarketSDKException):
    def __init__(self, message, valid_options:List[str]=None):
        self.message = message
        if valid_options is not None:
            self.message += ' Valid options are:'
            for option in valid_options:
                self.message += f' {option},'
            if len(valid_options) > 0:
                self.message = self.message[0:-1]
    
    def __str__(self):
        return self.message
