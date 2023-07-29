import asyncio
import json
import time
from mmproviders import HTTPConnectorBaseV2


class OpenAI(HTTPConnectorBaseV2):
    """
    https://platform.openai.com/docs/guides/gpt/function-calling
    """

    def __init__(self):
        super().__init__()
        self.key = "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"
        self.org = "org-01XS9nMNXSMGjG1xF3FDf1yU"
        self.uri = "https://api.openai.com"
        self.attempts = 0

        # asyncio.create_task(
        #     self.session.logger.push(
        #         service=self.__class__.__name__,
        #         function=self.__init__.__name__,
        #         info=f"{self.__class__.__name__} LLM Provider INITIALIZED"
        #     )
        # )

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.key}",
            "OpenAI-Organization": self.org

        }

    def query(self, prompt, max_tokens):
        """
        https://platform.openai.com/docs/api-reference/chat/create
        https://openai.com/blog/new-and-improved-embedding-model
        """
        uri = f"{self.uri}/v1/chat/completions"
        _json = {
            "model": "gpt-3.5-turbo-16k",
            # "model": "gpt-4",
            # "prompt": prompt,
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }

        res = self.post(uri, json=_json, headers=self.headers)
        return res

    def query_with_error_callback(self, prompt, max_tokens):
        res = self.query(
            prompt=prompt,
            max_tokens=max_tokens
        )

        if res.get("error"):
            print(f"{self.__class__.__name__} error:", res.get("error"))
            time.sleep(2)
            return self.query_with_error_callback(prompt, max_tokens)

        return res["choices"][0]["message"]["content"]

    async def aquery_with_error_callback(self, prompt, max_tokens):
        res = await self.aquery(
            prompt=prompt,
            max_tokens=max_tokens
        )

        if res.get("error"):
            print(f"{self.__class__.__name__} error:", res.get("error"))
            await asyncio.sleep(2)
            return await self.aquery_with_error_callback(prompt, max_tokens)

        return res

    async def aquery(self, prompt, max_tokens):
        """
        https://platform.openai.com/docs/api-reference/chat/create
        """
        uri = f"{self.uri}/v1/chat/completions"
        _json = {
            "model": "gpt-3.5-turbo-16k",
            # "prompt": prompt,
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }

        res = await self.apost(uri, json=_json, headers=self.headers)
        return res

    async def embeddings(self, text):
        """
        https://platform.openai.com/docs/guides/embeddings/what-are-embeddings

        An embedding is a vector (list) of floating point numbers.
        The distance between two vectors measures their relatedness.
        Small distances suggest high relatedness and large distances suggest low relatedness.

        https://www.youtube.com/watch?v=h0DHDp1FbmQ
        https://github.com/gkamradt/langchain-tutorials/blob/main/data_generation/Ask%20A%20Book%20Questions.ipynb
        """

        uri = f"{self.uri}/v1/embeddings"

        _json = dict(
            input=text,
            model="text-embedding-ada-002"
        )

        res = await self.apost(uri, json=_json, headers=self.headers)
        return res

    async def models(self):
        """
        https://platform.openai.com/docs/guides/embeddings/what-are-embeddings

        An embedding is a vector (list) of floating point numbers.
        The distance between two vectors measures their relatedness.
        Small distances suggest high relatedness and large distances suggest low relatedness.

        https://www.youtube.com/watch?v=h0DHDp1FbmQ
        https://github.com/gkamradt/langchain-tutorials/blob/main/data_generation/Ask%20A%20Book%20Questions.ipynb
        """

        uri = f"{self.uri}/v1/models"

        res = await self.aget(uri, headers=self.headers)

        print(json.dumps(res, indent=3))

        return res
