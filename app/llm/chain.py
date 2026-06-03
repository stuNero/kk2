# Package imports
from pydantic   import BaseModel, ConfigDict, SerializeAsAny
from typing     import Any, Generic, TypeVar
# Project File imports
from .llm       import SmolLM
from ..schema   import AskResponse

I = TypeVar("I")
M = TypeVar("M")
O = TypeVar("O")

class Runnable(BaseModel, Generic[I,O]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def invoke(self, data: I) -> O:
        raise NotImplementedError
    
    def __or__(self, other: "Runnable") -> 'RunnableSequence':
        return RunnableSequence.model_construct(first=self, second=other)
    
    
class RunnableSequence(Runnable[I,O], Generic[I,M,O]):
    first: SerializeAsAny[Runnable[I,M]]
    second: SerializeAsAny[Runnable[M,O]]
    
    def invoke(self, data: I) -> O:
        return self.second.invoke(self.first.invoke(data))

class PromptBuilderInput(BaseModel):
    question: str
    dataset_stats: dict[str, dict[str, Any]]

class PromptBuilderOutput(BaseModel):
    question: str
    prompt: str

class PromptBuilder(Runnable[PromptBuilderInput, PromptBuilderOutput]):
    name: str = "prompt_builder"
    
    def invoke(self, data: PromptBuilderInput) -> PromptBuilderOutput:
        prompt = f"""
        You are an AI data analyst
        
        Dataset statistics:
        {data.dataset_stats}
        
        Question: 
        {data.question}
        
        You SHOULD answer briefly and concisely. 

        You SHOULD NOT answer questions about anything other than the 
        given dataset. 
        IF question is completely unrelated to dataset, direct them to ask 
        questions about the dataset instead. 
        
        """
        return PromptBuilderOutput(
            question=data.question,
            prompt=prompt
        )

class LLMRunnerInput(BaseModel):
    question: str
    prompt: str
class LLMRunnerOutput(BaseModel):
    question: str
    raw_output: str
    model: str

class LLMRunner(Runnable[PromptBuilderOutput, LLMRunnerOutput]):
    name: str = "llm_runner"
    llm: SmolLM
    
    def invoke(self, data: PromptBuilderOutput) -> LLMRunnerOutput:
        raw_output = self.llm.invoke(data.prompt)
        
        return LLMRunnerOutput(
            question=data.question,
            raw_output=raw_output,
            model=self.llm.model_name
        )

class ResponseParser(Runnable[LLMRunnerOutput, AskResponse]):
    name: str = "response_parser"
    
    def invoke(self, data: LLMRunnerOutput) -> AskResponse:
        answer = data.raw_output.strip()
        
        return AskResponse(
            question=data.question,
            answer=answer,
            model=data.model
        )
def build_chain():
    return PromptBuilder() | LLMRunner(llm=SmolLM()) | ResponseParser()
