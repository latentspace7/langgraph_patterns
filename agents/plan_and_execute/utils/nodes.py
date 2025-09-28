from pydantic import TypeAdapter
from agents.plan_and_execute.utils.plan import planner, Plan
from agents.plan_and_execute.utils.executor import executor as agent_executor
from agents.plan_and_execute.utils.replan import replanner, Response, Act
from agents.plan_and_execute.utils.state import PlanExecute


async def execute_step(state: PlanExecute):
    plan = state["plan"]
    plan_str = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(plan))
    task = plan[0]

    # Create task message with context
    task_formatted = f"""For the following plan:
{plan_str}

You are tasked with executing step {1}: {task}

Please complete this step building upon any previous work done."""

    # Include full conversation history + current task
    executor_messages = list(state["messages"]) + [("user", task_formatted)]

    agent_response = await agent_executor.ainvoke(
        {"messages": executor_messages}
    )

    # Extract clean content from response
    last_message = agent_response
    if hasattr(last_message, 'content'):
        if isinstance(last_message.content, list):
            result_content = ""
            for item in last_message.content:
                if isinstance(item, dict) and item.get('type') == 'text':
                    result_content += item.get('text', '')
        else:
            result_content = last_message.content
    else:
        result_content = str(last_message)

    # Add execution result to conversation
    execution_msg = {
        "role": "assistant",
        "content": f"Completed step {len(state.get('past_steps', [])) + 1}: {task}\n\n{result_content}"
    }

    return {
        "messages": [execution_msg],
        "past_steps": [(task, result_content)],
    }


async def plan_step(state: PlanExecute):
    # Ensure we have at least one message for the planner
    messages = state["messages"]
    if not messages:
        # If no messages, this shouldn't happen in MessagesState workflow
        # but handle gracefully
        raise ValueError("Plan step requires at least one message in state")

    plan_result = await planner.ainvoke({"messages": messages})
    plan = TypeAdapter(Plan).validate_python(plan_result)

    # Create an assistant message with the plan
    plan_msg = {
        "role": "assistant",
        "content": f"I've created a plan with {len(plan.steps)} steps:\n" +
        "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan.steps))
    }

    # Return partial state update following MessagesState pattern
    return {
        "messages": [plan_msg],
        "plan": plan.steps
    }


async def replan_step(state: PlanExecute):
    # Get the original user input and current context
    current_input = state["messages"][0].content if state["messages"] else ""
    plan_str = "\n".join(f"{i+1}. {step}" for i,
                         step in enumerate(state.get("plan", [])))
    past_steps_str = "\n".join(
        f"- {step[0]}: {step[1]}" for step in state.get("past_steps", []))

    # Call replanner with messages format
    output_result = await replanner.ainvoke({
        "input": current_input,
        "plan": plan_str,
        "past_steps": past_steps_str
    })
    output = TypeAdapter(Act).validate_python(output_result)

    if isinstance(output.action, Response):
        response_msg = {
            "role": "assistant",
            "content": output.action.response
        }
        return {
            "messages": [response_msg],
            "response": output.action.response
        }
    else:
        replan_msg = {
            "role": "assistant",
            "content": f"Updated plan with {len(output.action.steps)} steps:\n" +
            "\n".join(f"{i+1}. {step}" for i,
                      step in enumerate(output.action.steps))
        }
        return {
            "messages": [replan_msg],
            "plan": output.action.steps
        }