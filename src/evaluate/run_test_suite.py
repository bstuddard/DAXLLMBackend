from src.evaluate.run_dax import *
from src.llm.anthropic_helpers import anthropic_stream_api_call


async def run_test_suites(scenario_data: dict):
    """
    Executes a suite of DAX query tests by generating queries through LLM and comparing results.

    Args:
        scenario_data (dict): A dictionary containing test scenarios with the following structure:
            {
                'test_scenarios': [
                    {
                        'scenario_name': str,
                        'scenario_prompt': str,
                        'expected_results': list[float]
                    },
                    ...
                ]
            }

    Returns:
        None

    Prints:
        - Individual test scenario results
        - Final summary with pass count, tested count, and pass percentage

    Raises:
        Exception: If LLM response is empty, DAX query execution fails, or result parsing fails
    """
    

    pass_count = 0
    tested_count = 0
    total_count = len(scenario_data['test_scenarios'])
    
    for scenario in scenario_data['test_scenarios']:
        print(f"\nTesting scenario: {scenario['scenario_name']}")
        
        # Get DAX query from LLM using streaming
        llm_response = ""
        async for chunk in anthropic_stream_api_call(scenario['scenario_prompt']):
            llm_response += chunk
        llm_response_orig = llm_response
        llm_response = llm_response.replace('\n', '')
        
        if not llm_response:
            raise Exception("Failed to get response from LLM")
        else:
            print(f"LLM response: {llm_response_orig}")
        
        # Run the generated DAX query
        llm_response = f"""EVALUATE ROW("new_measure", {llm_response})"""
        result = run_dax_query(llm_response)
        try:
            result = result[0]['[new_measure]']
        except:
            raise Exception("Failed to parse result.")
        
        if result is None:
            raise Exception("Failed to execute DAX query")
        
        # Loop through expected reslts array and see if any match the result
        for expected_result in scenario['expected_results']:
            if round(result, 3) == round(expected_result, 3):
                pass_count += 1
                break
        
        tested_count += 1
        print(f"Result: {result}, Expected: {scenario['expected_results']}")
    
    # Calculate percentage
    pass_percentage = (pass_count / tested_count * 100) if tested_count > 0 else 0
    print(f"Passed: {pass_count}, Tested: {tested_count}, Total: {total_count} ({pass_percentage:.1f}%)")
        



