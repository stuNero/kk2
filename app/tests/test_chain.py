import pytest
from app.llm.chain import PromptBuilder, PromptBuilderOutput, PromptBuilderInput

def test_promptbuilder_invoke():
    prompt_builder = PromptBuilder()
    data = {"age": {"mean": 25.0}}
    input = PromptBuilderInput(question="What is the average age?", dataset_stats=data)
    output = prompt_builder.invoke(input)
    assert type(output) == PromptBuilderOutput
    assert "What is the average age?" in output.prompt
    assert str(data) in output.prompt