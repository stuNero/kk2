import pytest
from app.llm.chain import (
                        PromptBuilder, 
                        PromptBuilderOutput, PromptBuilderInput,
                        LLMRunner,
                        LLMRunnerInput, LLMRunnerOutput,
                        ResponseParser,
                        AskResponse
                        )
from unittest.mock import MagicMock


def test_promptbuilder_invoke_returns_correct_data():
    prompt_builder = PromptBuilder()
    question = "What is the average age?"
    data = {"age": {"mean": 25.0}}
    
    input = PromptBuilderInput(question=question, dataset_stats=data)
    output = prompt_builder.invoke(input)
    
    assert type(output) == PromptBuilderOutput
    assert "What is the average age?" in output.prompt
    assert str(data) in output.prompt

def test_llmrunner_invoke_preserves_question_and_returns_llm_output():
    mock_llm = MagicMock()
    mock_llm.model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"
    runner = LLMRunner.model_construct(llm=mock_llm)
    
    input = PromptBuilderOutput(
        question="What is the average age?",
        prompt=""
    )
    mock_llm.invoke.return_value = "The average age is 25"
    output = runner.invoke(input)
    
    assert type(output) == LLMRunnerOutput
    assert output.question == input.question
    assert output.raw_output == "The average age is 25"

def test_responseparser_invoke_strips_whitespace():
    response_parser = ResponseParser()
    input = LLMRunnerOutput(
        question="What is the average age?",
        raw_output="  The average age is 25.  \n",
        model="HuggingFaceTB/SmolLM2-360M-Instruct")
    
    output = response_parser.invoke(input)
    
    assert type(output) == AskResponse
    assert output.answer == "The average age is 25."
    assert output.question == input.question
    assert output.model == input.model