import uuid
from dataclasses import dataclass
from mmutils import Instance
from session_base import SessionBase


class TaskA(SessionBase, Instance):
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.raw = "AI startup"
        self.target = "AI startup"
        self.description = "a newly established company that focuses on developing and providing products, services, or technologies related to Artificial Intelligence (AI)"

    @property
    def dict(self):
        return dict(
            id=self.id,
            raw=self.raw,
            target=self.target,
            description=self.description
        )


class Task(SessionBase, Instance):
    def __init__(self, raw):
        self.id = str(uuid.uuid4())
        self.raw = raw
        self.target = None
        self.description = None

        self.indentify_target()
        self.identify_description()

    def load(self):
        raise NotImplementedError

    def indentify_target(self):
        prompt = f"""
        Role: You are tasked with preparing a task description for an AI research tool.

        You will be given a string representing a research target. 
        Typically, customers research specific market niches or types of businesses. 
        Your objective is to identify and narrow down the raw input to a particular search term.
        
        For example: If the raw input is "a startup developing AI solutions for health industry" you should narrow it down to "AI health startup".
        However, if the raw input contains specific niche information, such as "a startup developing AI solutions for the health industry," 
        you must include a reference to that market niche in the final target description to keep the target focused.
        
        Goal 1: Narrow the raw request to a particular search term wide enough to generate a substantial number of search results.

        Goal 2: Keep the final result as concise as possible, preferably within 10 words maximum, while ensuring it remains informative.
         
        Return the processed result in the following format:
        
        TARGET: <result>
        
        Raw input: {self.raw}
        """

        res = self.session.llm.query_with_error_callback(
            prompt=prompt,
            max_tokens=1000,
        )

        target = res.split("TARGET: ")[1].strip()

        self.target = target

    def identify_description(self):
        prompt = f"""
        Role: You are tasked with preparing a task description for an AI research tool.

        You will receive a research target consisting of 2-3 words. Typically, customers research specific market niches or types of businesses. 

        Goal 1: Create an up to 15-word description of the target that can be used for processing text articles by 
        Language Model Models (LLMs), such as OpenAI, to identify whether the article is about the given target.
        
        For example, if target is "AI startup" the description can be "a newly established company that focuses on developing and providing products, services, or technologies related to Artificial Intelligence (AI)"

        Return the processed result in the following format:

        DESCRIPTION: <result>

        Target: {self.target}
        """

        res = self.session.llm.query_with_error_callback(
            prompt=prompt,
            max_tokens=1000,
        )

        desc = res.split("DESCRIPTION: ")[1].strip()

        print(res)

        self.description = desc

    @property
    def dict(self):
        return dict(
            id=self.id,
            raw=self.raw,
            target=self.target,
            description=self.description
        )
